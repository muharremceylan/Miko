"""Gerçek ücretli API çağrısı yapmadan hizmet sınırı ve doğrulama testleri."""
import base64
import io
import json
import unittest
import httpx
from PIL import Image
from .app import create_app,Settings,MAX_BODY
from .provider import ModelSolution,OpenAIProvider,ProviderError
from .verification import check_equation

class FakeProvider:
    def __init__(self):self.solve_calls=[];self.speech_calls=[]
    async def solve(self,question,image,topic):
        self.solve_calls.append((question,image,topic))
        return ModelSolution(transcribed_question=question or 'Görseldeki soru',assumptions=[],steps=[{'explanation':'İşlemi hesapla.','calculation':'3*7+5=26'}],final_answer='26',needs_clarification=False,clarification='')
    async def speak(self,text):self.speech_calls.append(text);return b'ID3test-only-audio'

class ApiTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.settings=Settings();self.settings.key='unit-test-placeholder';self.settings.access_code='unit-test-access-code'
        self.fake=FakeProvider();self.app=create_app(self.settings,self.fake)
        self.client=httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app),base_url='http://test')
    async def asyncTearDown(self):await self.client.aclose()
    async def auth(self):
        response=await self.client.post('/v1/session',json={'access_code':self.settings.access_code})
        self.assertEqual(response.status_code,200);return {'Authorization':'Bearer '+response.json()['access_token']}
    async def test_health_and_capabilities_do_not_expose_keys(self):
        response=await self.client.get('/health');self.assertEqual(response.json(),{'status':'ok'})
        response=await self.client.get('/v1/capabilities');self.assertTrue(response.json()['solver_ready'])
        self.assertNotIn(self.settings.key,response.text);self.assertNotIn(self.settings.access_code,response.text)
    async def test_unconfigured_service_never_pretends_to_generate(self):
        settings=Settings();settings.key='';settings.access_code=''
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=create_app(settings,self.fake)),base_url='http://test') as c:
            self.assertFalse((await c.get('/v1/capabilities')).json()['solver_ready'])
            self.assertEqual((await c.post('/v1/solve',json={'topic_id':'temel','question':'2+2?'})).status_code,503)
        self.assertEqual(self.fake.solve_calls,[])
    async def test_unauthenticated_and_wrong_access_codes_rejected(self):
        response=await self.client.post('/v1/solve',json={'topic_id':'temel','question':'2+2?'})
        self.assertEqual(response.status_code,401)
        self.assertEqual((await self.client.post('/v1/session',json={'access_code':'wrong'})).status_code,401)
        self.assertEqual(self.fake.solve_calls,[])
    async def test_text_solution_has_independent_partial_check_not_expert_claim(self):
        response=await self.client.post('/v1/solve',headers=await self.auth(),json={'topic_id':'temel','question':'3*7+5?'})
        self.assertEqual(response.status_code,200);data=response.json();self.assertEqual(data['source'],'ai')
        self.assertEqual(data['verification']['status'],'partial');self.assertFalse(data['verification']['expert_approved'])
        self.assertEqual(response.headers['cache-control'],'no-store')
    async def test_photo_is_decoded_and_normalized_not_forwarded_blindly(self):
        buf=io.BytesIO();Image.new('RGBA',(12,12),(255,255,255,255)).save(buf,format='PNG')
        image='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
        response=await self.client.post('/v1/solve',headers=await self.auth(),json={'topic_id':'temel','image_data_url':image})
        self.assertEqual(response.status_code,200);self.assertTrue(self.fake.solve_calls[0][1].startswith('data:image/jpeg;base64,'))
    async def test_invalid_image_and_unknown_topic_do_not_call_provider(self):
        headers=await self.auth()
        for data in [{'topic_id':'temel','image_data_url':'data:image/png;base64,broken'},{'topic_id':'unknown','question':'2+2?'},{'topic_id':'temel','question':''}]:
            response=await self.client.post('/v1/solve',headers=headers,json=data);self.assertEqual(response.status_code,422)
        self.assertEqual(self.fake.solve_calls,[])
    async def test_request_limit_checks_actual_body(self):
        response=await self.client.post('/v1/solve',content=json.dumps({'question':'x'*(MAX_BODY+1)}),headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code,413)
        self.assertEqual(self.fake.solve_calls,[])
    async def test_session_rate_limit(self):
        headers=await self.auth()
        for _ in range(6):self.assertEqual((await self.client.post('/v1/solve',headers=headers,json={'topic_id':'temel','question':'2+2?'})).status_code,200)
        self.assertEqual((await self.client.post('/v1/solve',headers=headers,json={'topic_id':'temel','question':'2+2?'})).status_code,429)
    async def test_speech_uses_server_script_and_caches_generated_bytes(self):
        headers=await self.auth()
        for _ in range(2):
            response=await self.client.post('/v1/speech',headers=headers,json={'topic_id':'temel','level':'quick'})
            self.assertEqual(response.status_code,200);self.assertTrue(response.headers['content-type'].startswith('audio/mpeg'))
        self.assertEqual(len(self.fake.speech_calls),1);self.assertIn('Temel kavramları',self.fake.speech_calls[0])
        self.assertEqual((await self.client.post('/v1/speech',headers=headers,json={'topic_id':'sayilar','level':'quick'})).status_code,422)
    async def test_cors_only_known_origins(self):
        good=await self.client.get('/health',headers={'Origin':'https://muharremceylan.github.io'})
        bad=await self.client.get('/health',headers={'Origin':'https://unknown.example'})
        self.assertEqual(good.headers.get('access-control-allow-origin'),'https://muharremceylan.github.io')
        self.assertNotIn('access-control-allow-origin',bad.headers)
    async def test_provider_failure_is_not_replaced_by_demo_solution(self):
        async def fail(*_):raise ProviderError('test-failure')
        self.fake.solve=fail
        response=await self.client.post('/v1/solve',headers=await self.auth(),json={'topic_id':'temel','question':'2+2?'})
        self.assertEqual(response.status_code,502);self.assertNotIn('solution',response.json())

class VerificationTests(unittest.TestCase):
    def test_arithmetic_and_contradictions(self):
        for value in ['3*7+5=26','(1/3)+(2/3)=1','(−3)²=9','0.1+0.2=0.3']:self.assertEqual(check_equation(value),'passed')
        self.assertEqual(check_equation('3*7+5=25'),'mismatch')
    def test_unsafe_or_unbounded_expressions_not_evaluated(self):
        for value in ['2**1000000=1','1/0=1','x+2=4','call(5)=5','[1][0]=1','2**(2**1000)=1']:self.assertEqual(check_equation(value),'not_checked')

class ProviderTests(unittest.IsolatedAsyncioTestCase):
    async def test_official_request_shape_and_actual_response_parsing(self):
        async def handler(request):
            data=json.loads(request.content);self.assertEqual(request.url.path,'/v1/responses');self.assertFalse(data['store']);self.assertEqual(data['text']['format']['type'],'json_schema')
            output={'transcribed_question':'3+4?','assumptions':[],'steps':[{'explanation':'Topla.','calculation':'3+4=7'}],'final_answer':'7','needs_clarification':False,'clarification':''}
            return httpx.Response(200,json={'status':'completed','output':[{'content':[{'type':'output_text','text':json.dumps(output)}]}]})
        provider=OpenAIProvider('unit-test-placeholder',transport=httpx.MockTransport(handler))
        solution=await provider.solve('3+4?',None,'Temel Kavramlar');self.assertEqual(solution.final_answer,'7')
    async def test_bad_upstream_response_does_not_generate_fake_solution(self):
        provider=OpenAIProvider('unit-test-placeholder',transport=httpx.MockTransport(lambda _:httpx.Response(200,json={'status':'incomplete','output':[]})))
        with self.assertRaises(ProviderError):await provider.solve('3+4?',None,'Temel Kavramlar')

    async def test_speech_request_uses_official_endpoint_and_audio_type(self):
        def handler(request):
            data=json.loads(request.content)
            self.assertEqual(request.url.path,'/v1/audio/speech')
            self.assertEqual(data['response_format'],'mp3')
            self.assertEqual(data['voice'],'coral')
            return httpx.Response(200,content=b'ID3test-only',headers={'content-type':'audio/mpeg'})
        provider=OpenAIProvider('unit-test-placeholder',transport=httpx.MockTransport(handler))
        self.assertEqual(await provider.speak('Test metni.'),b'ID3test-only')
    async def test_html_response_is_not_presented_as_generated_audio(self):
        provider=OpenAIProvider('unit-test-placeholder',transport=httpx.MockTransport(lambda _:httpx.Response(200,text='<html>unavailable</html>',headers={'content-type':'text/html'})))
        with self.assertRaises(ProviderError):await provider.speak('Test metni.')
