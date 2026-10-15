"""Tek süreçli, erişim koduyla korunan AI pilotu. Kimlik/anahtarlar istemciye gömülmez."""
import base64
import hashlib
import io
import json
import os
import secrets
import time
from collections import deque
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, ConfigDict, Field, model_validator
from .provider import OpenAIProvider, ProviderError
from .verification import verify

ROOT=Path(__file__).resolve().parents[2]
CONTENT=ROOT/'akademi_ai_prototip/content/kpss/lisans/matematik'
TOPICS={t['id']:t['title'] for t in json.loads((CONTENT/'curriculum.json').read_text())['topics']}
LESSON=json.loads((CONTENT/'topics/temel.json').read_text())
AUDIO=json.loads((CONTENT/'topics/temel-audio.json').read_text())
MAX_BODY=6*1024*1024

class Settings:
    def __init__(self):
        self.key=os.getenv('OPENAI_API_KEY','')
        self.access_code=os.getenv('AKADEMI_ACCESS_CODE','')
        self.origins=[x.strip() for x in os.getenv('AKADEMI_ALLOWED_ORIGINS','https://muharremceylan.github.io,http://127.0.0.1:4173').split(',') if x.strip()]
        self.solver_model=os.getenv('OPENAI_SOLVER_MODEL','gpt-4.1-mini')
        self.speech_model=os.getenv('OPENAI_SPEECH_MODEL','gpt-4o-mini-tts')
    @property
    def ready(self):return bool(self.key and len(self.access_code)>=12)

class BodyLimit:
    def __init__(self,app):self.app=app
    async def __call__(self,scope,receive,send):
        if scope['type']!='http':return await self.app(scope,receive,send)
        parts=[];total=0
        while True:
            message=await receive()
            if message['type']=='http.disconnect':return
            chunk=message.get('body',b'');total+=len(chunk)
            if total>MAX_BODY:
                await JSONResponse({'detail':'Görsel çok büyük. En fazla 4 MB görsel seç.'},status_code=413)(scope,receive,send)
                return
            parts.append(chunk)
            if not message.get('more_body',False):break
        payload=b''.join(parts);del parts
        delivered=False
        async def replay():
            nonlocal delivered
            if not delivered:
                delivered=True
                return {'type':'http.request','body':payload,'more_body':False}
            return await receive()
        await self.app(scope,replay,send)

class Login(BaseModel):
    model_config=ConfigDict(extra='forbid')
    access_code:str=Field(min_length=1,max_length=200)
class Solve(BaseModel):
    model_config=ConfigDict(extra='forbid')
    topic_id:str=Field(max_length=100)
    question:str=Field(default='',max_length=3000)
    image_data_url:str|None=Field(default=None,max_length=5_600_000)
    @model_validator(mode='after')
    def nonempty(self):
        if not self.question.strip() and not self.image_data_url:raise ValueError('Bir soru veya görsel gerekli.')
        return self
class Speech(BaseModel):
    model_config=ConfigDict(extra='forbid')
    topic_id:str
    level:str

def normalize_image(data):
    if not data:return None
    try:
        header,payload=data.split(',',1)
        formats={'data:image/jpeg;base64':'JPEG','data:image/png;base64':'PNG','data:image/webp;base64':'WEBP'}
        if header not in formats:raise ValueError()
        binary=base64.b64decode(payload,validate=True)
        if len(binary)>4*1024*1024:raise ValueError()
        with Image.open(io.BytesIO(binary)) as image:
            if image.format!=formats[header] or image.width*image.height>16_000_000:raise ValueError()
            image.load();image.thumbnail((2048,2048))
            clean=Image.new('RGB',image.size,'white')
            if image.mode in ('RGBA','LA') or (image.mode=='P' and 'transparency' in image.info):
                rgba=image.convert('RGBA');clean.paste(rgba,mask=rgba.getchannel('A'))
            else:clean.paste(image.convert('RGB'))
            out=io.BytesIO();clean.save(out,format='JPEG',quality=88)
        return 'data:image/jpeg;base64,'+base64.b64encode(out.getvalue()).decode()
    except (ValueError,UnidentifiedImageError,OSError,Image.DecompressionBombError) as exc:
        raise HTTPException(422,'Görsel açılamadı. En fazla 4 MB ve 16 megapiksel PNG, JPEG veya WebP seç.') from exc

def create_app(settings=None,provider=None):
    settings=settings or Settings()
    provider=provider or OpenAIProvider(settings.key,settings.solver_model,settings.speech_model)
    app=FastAPI(title='Akademi AI',docs_url=None,redoc_url=None)
    app.add_middleware(BodyLimit)
    app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_methods=['GET','POST'],allow_headers=['Authorization','Content-Type'])
    sessions={};rate={};budget={'date':date.today(),'solve':0,'speech':0};speech_cache={}
    def limit(key,max_count,seconds=60):
        now=time.monotonic()
        if key not in rate and len(rate)>=1000:
            for old in [k for k,v in rate.items() if not v or v[-1]<now-3600]:rate.pop(old,None)
            if len(rate)>=1000:raise HTTPException(503,'Hizmet geçici olarak yoğun.')
        q=rate.setdefault(key,deque())
        while q and q[0]<now-seconds:q.popleft()
        if len(q)>=max_count:raise HTTPException(429,'Çok sık istek gönderildi. Biraz bekleyip tekrar dene.',headers={'Retry-After':str(seconds)})
        q.append(now)
    def authorize(request):
        if not settings.ready:raise HTTPException(503,'AI hizmeti henüz etkinleştirilmedi.')
        authorization=request.headers.get('authorization','')
        if not authorization.startswith('Bearer '):raise HTTPException(401,'Devam etmek için davet koduyla oturum aç.')
        key=hashlib.sha256(authorization[7:].encode()).hexdigest()
        if sessions.get(key,0)<=time.monotonic():raise HTTPException(401,'Oturum süresi doldu. Davet koduyla yeniden giriş yap.')
        limit('request:'+key,6)
        return key
    def use_budget(kind):
        if budget['date']!=date.today():budget.update(date=date.today(),solve=0,speech=0)
        maximum=50 if kind=='solve' else 20
        if budget[kind]>=maximum:raise HTTPException(429,'Pilot için günlük hizmet sınırına ulaşıldı.')
        budget[kind]+=1
    @app.get('/health')
    async def health():return {'status':'ok'}
    @app.get('/v1/capabilities')
    async def capabilities():return {'solver_ready':settings.ready,'speech_ready':settings.ready,'requires_access_code':True,'session_minutes':20}
    @app.post('/v1/session')
    async def login(body:Login,request:Request):
        if not settings.ready:raise HTTPException(503,'AI hizmeti henüz etkinleştirilmedi.')
        limit('login:'+(request.client.host if request.client else 'local'),5)
        if not secrets.compare_digest(body.access_code.encode(),settings.access_code.encode()):raise HTTPException(401,'Davet kodu geçerli değil.')
        now=time.monotonic()
        for key in list(sessions):
            if sessions[key]<=now:sessions.pop(key)
        if len(sessions)>=100:raise HTTPException(503,'Pilot oturum kapasitesi dolu.')
        token=secrets.token_urlsafe(32);sessions[hashlib.sha256(token.encode()).hexdigest()]=now+1200
        return JSONResponse({'access_token':token,'expires_in':1200},headers={'Cache-Control':'no-store'})
    @app.post('/v1/solve')
    async def solve(body:Solve,request:Request):
        authorize(request)
        if body.topic_id not in TOPICS:raise HTTPException(422,'Konu bulunamadı.')
        image=normalize_image(body.image_data_url);use_budget('solve')
        try:solution=await provider.solve(body.question.strip(),image,TOPICS[body.topic_id])
        except ProviderError as exc:raise HTTPException(502,'AI yanıtı alınamadı. Sorunu tekrar kontrol edip daha sonra dene.') from exc
        return JSONResponse({'source':'ai','solution':solution.model_dump(),'verification':verify(solution)},headers={'Cache-Control':'no-store'})
    @app.post('/v1/speech')
    async def speech(body:Speech,request:Request):
        authorize(request)
        if body.topic_id!='temel' or body.level not in LESSON['summaries']:raise HTTPException(422,'Bu özetin ses metni henüz hazır değil.')
        cache_key=(AUDIO['version'],body.level)
        if cache_key not in speech_cache:
            # Yalnız sunucudaki eğitim metni seslendirilir; sınırsız serbest metin üretimi yok.
            text=AUDIO['summaries'][body.level]
            if len(text)>4096:raise HTTPException(422,'Bu özetin ses üretimi için daha kısa bir metin hazırlanmalı.')
            use_budget('speech')
            try:speech_cache[cache_key]=await provider.speak(text)
            except ProviderError as exc:raise HTTPException(502,'Ses üretilemedi. Cihaz sesiyle dinlemeyi veya daha sonra denemeyi seçebilirsin.') from exc
        return Response(speech_cache[cache_key],media_type='audio/mpeg',headers={'Cache-Control':'private, max-age=3600','X-Akademi-Audio':'ai-generated'})
    return app

app=create_app()
