"""MTProto bot hesabı; kişisel Telegram oturumu veya telefon giriş kodu istemez."""
import argparse
import asyncio
import contextlib
import json
import logging
import os
import time
from pathlib import Path
from telethon import TelegramClient,events
from .config import Settings,ConfigurationError
from .core import PDFService,Incoming

class TelegramTransport:
    def __init__(self,client):self.client=client
    async def message(self,user,text):await asyncio.wait_for(self.client.send_message(user,text,parse_mode=None),30)
    async def file(self,user,path,caption):await asyncio.wait_for(self.client.send_file(user,str(path),caption=caption,force_document=True,parse_mode=None),300)
    async def download(self,document,path,progress):
        with path.open('xb') as output:await self.client.download_media(document,file=output,progress_callback=progress)

async def run(settings):
    os.umask(0o077);settings.data_dir.mkdir(parents=True,exist_ok=True,mode=0o700)
    client=TelegramClient(str(settings.data_dir/'telegram'),settings.api_id,settings.api_hash,connection_retries=3,retry_delay=2,timeout=20,flood_sleep_threshold=0)
    service=PDFService(settings,TelegramTransport(client));service.recover();service.cleanup()
    worker=None;maintenance=None
    try:
        await client.connect()
        if not await client.is_user_authorized():await client.sign_in(bot_token=settings.bot_token)
        me=await client.get_me()
        if not me or not me.bot or me.id!=int(settings.bot_token.split(':',1)[0]):raise ConfigurationError('Oturum beklenen bot hesabına ait değil. Kişisel oturum kullanılmadı.')
        @client.on(events.NewMessage(incoming=True))
        async def receive(event):
            try:
                message=event.message
                incoming=Incoming(sender=event.sender_id or 0,chat=event.chat_id or 0,message_id=message.id,private=bool(event.is_private),text=event.raw_text or '',forwarded=message.fwd_from is not None,document=message if event.document else None,filename=event.file.name or '' if event.file else '',size=event.document.size if event.document else 0,mime=event.document.mime_type if event.document else '')
                await service.handle(incoming)
            except Exception:print('Bir ileti işlenemedi; özel içerik günlüğe yazılmadı.',flush=True)
        worker=asyncio.create_task(service.worker())
        async def maintain():
            cycles=0
            while True:
                if worker.done():raise RuntimeError('worker-stopped')
                (settings.data_dir/'heartbeat').write_text(str(time.time()))
                if cycles%120==0:service.cleanup()
                cycles+=1;await asyncio.sleep(30)
        maintenance=asyncio.create_task(maintain())
        print('Bot bağlandı; yalnız eşleştirilmiş kullanıcının özel PDF iletileri işlenir.',flush=True)
        done,_=await asyncio.wait([client.disconnected,maintenance],return_when=asyncio.FIRST_COMPLETED)
        if maintenance in done:await maintenance
    finally:
        for task in [worker,maintenance]:
            if task:
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError,Exception):await task
        await client.disconnect();(settings.data_dir/'heartbeat').unlink(missing_ok=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--healthcheck',action='store_true');args=parser.parse_args()
    logging.getLogger('telethon').setLevel(logging.CRITICAL);logging.getLogger('pypdf').setLevel(logging.CRITICAL)
    if args.healthcheck:
        try:healthy=0<=time.time()-float((Path(os.environ.get('BOT_DATA_DIR','/data'))/'heartbeat').read_text())<90
        except (OSError,ValueError):healthy=False
        return 0 if healthy else 1
    try:settings=Settings.from_environment()
    except ConfigurationError as error:
        print(json.dumps({'configured':False,'message':str(error)},ensure_ascii=False));return 2
    if args.check:
        print(json.dumps({'configured':True,'telegram_connection_tested':False,'transport':'MTProto-bot','ocr_enabled':settings.enable_ocr}));return 0
    try:asyncio.run(run(settings));return 0
    except KeyboardInterrupt:return 0
    except Exception:
        print('Bot başlatılamadı veya bağlantı kesildi. Sunucu ayarlarını ve Telegram ağ erişimini kontrol et; gizli değerler günlüğe yazılmadı.',flush=True);return 1
if __name__=='__main__':raise SystemExit(main())
