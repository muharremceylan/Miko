"""Defter görünümü ve servis entegrasyonu. Ses/API yanıtları bu testte taklittir."""
import base64
import io
import json
import os
import wave
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('AKADEMI_TEST_URL','http://127.0.0.1:4173')
passed=[]
VOICE="""
window.__spoken=[];window.__voiceActions={pause:0,resume:0,cancel:0};
Object.defineProperty(window,'speechSynthesis',{value:{getVoices(){return [{lang:'tr-TR',name:'TEST ONLY'}]},addEventListener(){},speak(u){window.__spoken.push(u)},cancel(){window.__voiceActions.cancel++},pause(){window.__voiceActions.pause++},resume(){window.__voiceActions.resume++}}});
window.SpeechSynthesisUtterance=class{constructor(text){this.text=text}};
"""
def start(page):
 page.goto(BASE);page.locator('#exam-kpss').click();page.locator('#level-lisans').click();page.evaluate("AcademiMath.openTopic('temel')")
def tab(page,name):page.locator('#math-tab-'+name).click()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':390,'height':844});page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));start(page)
 menu=page.locator('.math-topic-tabs');assert page.get_by_role('tab').count()==7
 assert menu.evaluate('(e)=>e.scrollWidth<=e.clientWidth')
 assert menu.evaluate('(e)=>getComputedStyle(e).display')=='grid'
 assert all(b.is_visible() for b in page.get_by_role('tab').all())
 assert page.locator('.notebook-page').count()==9
 page.evaluate('document.fonts.ready');assert page.evaluate("document.fonts.check('24px AkademiNotes')")
 assert 'AkademiNotes' in page.locator('.notebook-page h3').first.evaluate('(e)=>getComputedStyle(e).fontFamily')
 assert len(set(page.locator('.notebook-page').nth(i).evaluate('(e)=>getComputedStyle(e).backgroundColor') for i in range(4)))==4
 detail=page.locator('.notebook-original').first;detail.locator('summary').click();assert 'Matematikte bir sorunun' in detail.inner_text()
 recall=page.locator('.recall-card').first;assert not recall.locator('p').is_visible();recall.locator('summary').click();assert recall.locator('p').is_visible()
 page.locator('[data-math-action="note-style"][data-style="plain"]').click();assert page.locator('.notebook-page').count()==0
 page.reload();page.evaluate("AcademiMath.openTopic('temel')");assert page.locator('[data-style="plain"]').get_attribute('aria-pressed')=='true'
 page.locator('[data-style="notebook"]').click();assert page.locator('.notebook-page').count()==9
 passed.append('Yatay kaydırmasız yedi bölüm; gömülü Türkçe el yazısı, dört renk, tam anlatım, hatırlama ve kalıcı düz yazı seçimi')

 tab(page,'summary');assert page.locator('.memory-card').count()==4
 assert page.locator('.memory-card .recall-card').count()==4
 for level in ['standard','detailed']:
  page.locator('#mathSummaryLevel').select_option(level);assert page.locator('.summary-sheet').count()>=9
  assert page.locator('.summary-sheet .recall-card').count()>=3
 for width in [320,360,390,412,768]:
  page.set_viewport_size({'width':width,'height':844})
  for theme in ['light','dark']:
   if page.locator('html').get_attribute('data-theme')!=theme:page.locator('#themeToggle').click()
   for name in ['lesson','summary','formulas','examples','test','audio','ai']:
    tab(page,name);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme,name)
    assert menu.evaluate('(e)=>e.scrollWidth<=e.clientWidth')
 tab(page,'test');page.locator('[data-math-action="start"][data-count="10"]').click()
 page.wait_for_function('document.querySelector("#mathTestQuestion .question-card").getBoundingClientRect().top < innerHeight-100')
 assert page.locator('#mathAnswers button').count()==5
 passed.append('Üç görsel özet, iki tema ve 320–768 piksel; bölüm/test seçimi içeriğe götürür')

 voiced=browser.new_context(viewport={'width':390,'height':844});voiced.add_init_script(VOICE);v=voiced.new_page();v.on('pageerror',lambda e:errors.append(str(e)));start(v);tab(v,'audio')
 assert v.locator('#deviceSpeechControls').is_visible();v.locator('#deviceSpeechRate').select_option('0.75');v.locator('#deviceSpeechPlay').click()
 v.wait_for_function('window.__spoken.length===1');assert v.evaluate('__spoken[0].rate')==0.75
 assert v.locator('#deviceSpeechProgress').get_attribute('value')=='0'
 v.evaluate('__spoken[0].onboundary({charIndex:50})');assert float(v.locator('#deviceSpeechProgress').get_attribute('value'))>0
 v.locator('#deviceSpeechPause').click();assert v.locator('#deviceSpeechResume').is_visible();v.locator('#deviceSpeechResume').click()
 assert v.evaluate('__voiceActions.pause')==1 and v.evaluate('__voiceActions.resume')==1
 v.locator('#deviceSpeechStop').click();assert v.locator('#deviceSpeechPlay').is_visible()
 v.locator('#audioSummaryLevel').select_option('detailed');v.locator('#deviceSpeechPlay').click();v.wait_for_function('window.__spoken.length===2')
 tab(v,'formulas');v.evaluate('__spoken[1].onend()');assert v.evaluate('__spoken.length')==2
 assert v.locator('.math-formula').count()==8
 voiced.close();passed.append('Taklit Türkçe ses motoruyla oynat/duraklat/devam/hız/ilerleme; ayrılınca geç ses başlamaz')

 # Gerçek sağlayıcı çağrısı veya ücretli ses üretimi yapılmaz.
 output=io.BytesIO()
 with wave.open(output,'wb') as audio:audio.setnchannels(1);audio.setsampwidth(2);audio.setframerate(8000);audio.writeframes(b'\0\0'*16000)
 requests=[];mode={'fail':False}
 def route_handler(route):
  req=route.request;headers={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'Authorization,Content-Type','Access-Control-Allow-Methods':'GET,POST,OPTIONS'}
  if req.method=='OPTIONS':route.fulfill(status=204,headers=headers);return
  path=req.url.rsplit('/',1)[-1]
  if path=='capabilities':data={'solver_ready':True,'speech_ready':True,'requires_access_code':True}
  elif path=='session':data={'access_token':'TEST-SESSION-ONLY','expires_in':1200}
  elif path=='speech':
   requests.append(('speech',req.post_data_json,req.headers.get('authorization')));route.fulfill(status=200,headers={**headers,'Content-Type':'audio/wav'},body=output.getvalue());return
  elif path=='solve':
   requests.append(('solve',req.post_data_json,req.headers.get('authorization')))
   if mode['fail']:route.fulfill(status=502,headers=headers,json={'detail':'Test hizmeti geçici olarak kullanılamıyor.'});return
   data={'source':'ai','solution':{'transcribed_question':'3 + 4? <img src=x onerror=alert(1)>','assumptions':[],'steps':[{'explanation':'İki sayıyı topla.','calculation':'3+4=7'}],'final_answer':'7','needs_clarification':False,'clarification':''},'verification':{'status':'partial','expert_approved':False,'checks':[{'step':1,'status':'passed'}]}}
  else:raise AssertionError(req.url)
  route.fulfill(status=200,headers=headers,json=data)
 remote=browser.new_context(viewport={'width':390,'height':844});remote.add_init_script("window.AkademiConfig={apiBase:'https://akademi-services.test'}")
 remote.route('https://akademi-services.test/**',route_handler)
 r=remote.new_page();r.on('pageerror',lambda e:errors.append(str(e)));start(r);tab(r,'ai')
 r.locator('#aiAccessCode').fill('TEST-ACCESS-CODE');r.locator('[data-math-action="service-login"]').click();r.locator('#aiQuestion').fill('3 + 4 kaçtır?')
 png=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/a9sAAAAASUVORK5CYII=')
 r.locator('#aiQuestionImage').set_input_files({'name':'sample.png','mimeType':'image/png','buffer':png})
 r.locator('.ai-question-image').wait_for();r.locator('[data-math-action="ai-solve"]').click();r.locator('.ai-result').wait_for()
 assert 'uzman onaylı değildir' in r.locator('.ai-result').inner_text()
 assert r.locator('.ai-result img').count()==0
 assert requests[0][0]=='solve' and requests[0][1]['image_data_url'].startswith('data:image/png;base64,')
 assert requests[0][2]=='Bearer TEST-SESSION-ONLY'
 assert r.evaluate("!JSON.stringify(localStorage).includes('TEST-SESSION-ONLY')")
 mode['fail']=True;r.locator('[data-math-action="ai-solve"]').click();r.get_by_role('alert').wait_for();assert r.locator('.ai-result').count()==0
 passed.append('Taklit API ile davet oturumu, metin/fotoğraf çözümü, doğrulama etiketi, XSS engeli ve hatada sahte sonuç üretmeme')

 tab(r,'audio');r.locator('[data-math-action="server-speech"]').click();player=r.locator('#summaryAudioPlayer');player.wait_for()
 r.wait_for_function('document.querySelector("#summaryAudioPlayer").duration===2')
 player.evaluate('(e)=>{e.currentTime=0.75;e.pause()}');r.locator('#summaryAudioRate').select_option('1.5')
 assert player.evaluate('(e)=>e.playbackRate')==1.5
 assert abs(player.evaluate('(e)=>e.currentTime')-0.75)<0.1
 assert any(entry[0]=='speech' for entry in requests)
 assert 'AI sağlayıcısına' not in json.dumps(requests[-1][1],ensure_ascii=False)
 remote.close();passed.append('Taklit iki saniyelik ses dosyasıyla gerçek medya süresi, sarma ve hız kontrolü')

 actual=browser.new_context();actual.add_init_script("window.AkademiConfig={apiBase:'http://127.0.0.1:8010'}")
 a=actual.new_page();a.on('pageerror',lambda e:errors.append(str(e)));start(a);tab(a,'ai')
 a.get_by_text('AI hizmeti henüz etkinleştirilmedi.',exact=False).wait_for()
 assert a.locator('#aiQuestion').count()==0
 actual.close();passed.append('Anahtarsız çalışan gerçek FastAPI sunucusu hazır olmayan hizmeti doğru bildirir')

 assert not errors,errors
 context.close();browser.close()
print(json.dumps({'passed':passed,'page_errors':errors,'note':'Cihaz sesi ve uzak AI/medya yanıtları test taklitleridir; gerçek sağlayıcı veya fiziksel ses testi değildir.'},ensure_ascii=False,indent=2))
