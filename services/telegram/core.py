import asyncio
import contextlib
import json
import os
import signal
import re
import secrets
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from .pdf import digest,ERRORS
from .store import Store,SUBJECTS

@dataclass
class Incoming:
    sender:int
    chat:int
    message_id:int
    private:bool
    text:str=''
    forwarded:bool=False
    document:object=None
    filename:str=''
    size:int=0
    mime:str=''

async def process_in_subprocess(source,output,settings):
    args=[sys.executable,'-m','services.telegram.pdf','--source',str(source),'--output',str(output),'--part-bytes',str(settings.part_bytes),'--max-pages',str(settings.max_pages)]
    used=sum(p.stat().st_size for p in (settings.data_dir/'jobs').rglob('*') if p.is_file() and not p.is_symlink())
    args.extend(['--max-output-bytes',str(max(0,settings.quota_bytes-used))])
    if settings.enable_ocr:args.append('--ocr')
    process=await asyncio.create_subprocess_exec(*args,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.DEVNULL,start_new_session=True)
    try:stdout,_=await asyncio.wait_for(process.communicate(),settings.job_timeout)
    except (asyncio.TimeoutError,asyncio.CancelledError):
        with contextlib.suppress(ProcessLookupError):os.killpg(process.pid,signal.SIGKILL)
        await process.wait();raise
    if process.returncode:
        try:code=json.loads(stdout)['error']
        except Exception:code='invalid_pdf'
        raise ValueError(code if code in ERRORS else 'invalid_pdf')
    return json.loads((output/'manifest.json').read_text())

class PDFService:
    def __init__(self,settings,transport,processor=process_in_subprocess):
        self.settings=settings;self.transport=transport;self.processor=processor
        self.root=settings.data_dir;self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
        (self.root/'jobs').mkdir(exist_ok=True,mode=0o700)
        self.store=Store(self.root/'bot.sqlite3');self.queue=asyncio.Queue(maxsize=3);self.pair_failures={};self.busy=set()
    def job_dir(self,id):
        if not re.fullmatch(r'[a-f0-9]{12}',id):raise ValueError('invalid-job')
        return self.root/'jobs'/id
    async def message(self,user,text):
        try:await self.transport.message(user,text)
        except Exception:pass # Hata nesnesi URL/oturum/anahtar içerebilir; içerik loglanmaz.
    def pairing_allowed(self,user):
        now=time.monotonic();self.pair_failures={u:[t for t in times if now-t<900] for u,times in self.pair_failures.items() if times and now-times[-1]<900}
        if len(self.pair_failures)>=1000 and user not in self.pair_failures:return False
        times=self.pair_failures.setdefault(user,[])
        if len(times)>=5:return False
        times.append(now);return True
    async def handle(self,m):
        if not m.private or m.sender!=m.chat or m.sender<=0:return
        # İletilen metinler ve belge açıklamaları komut olarak yorumlanmaz.
        command=m.text.strip() if not m.forwarded and m.document is None else ''
        if self.store.owner()!=m.sender:
            if command.startswith('/start '):
                if not self.pairing_allowed(m.sender):return
                code=command.partition(' ')[2]
                if secrets.compare_digest(code.encode(),self.settings.pairing_code.encode()) and self.store.claim(m.sender):
                    await self.message(m.sender,'Eşleştirme tamamlandı. /ders tarih gibi bir ders seçip PDF’yi bu özel sohbete iletebilirsin. /yardim komutları gösterir.');return
            await self.message(m.sender,'Bu bot kişisel kullanım içindir. Kurulumdaki özel eşleştirme bağlantısını kullan.');return
        if command in ('/start','/yardim','/help'):
            await self.message(m.sender,'PDF’yi bu özel sohbete ilet veya dosya olarak ekle.\n/ders turkce | tarih | vatandaslik | cografya | matematik\n/durum\n/parcalar İŞ_KODU\n/metin İŞ_KODU\n/sil İŞ_KODU\nDosyalar varsayılan 7 gün saklanır. Metinler inceleme taslağıdır; uygulamaya otomatik yayımlanmaz.');return
        if command.startswith('/ders '):
            subject=command.partition(' ')[2].casefold().translate(str.maketrans('çğıöşü','cgiosu'))
            if subject in SUBJECTS:self.store.subject(m.sender,subject);await self.message(m.sender,'Sonraki PDF’lerin dersi: '+SUBJECTS[subject])
            else:await self.message(m.sender,'Ders seçimi: /ders turkce, tarih, vatandaslik, cografya veya matematik')
            return
        if command=='/durum':
            jobs=self.store.recent(m.sender)
            labels={'queued':'Sırada','downloading':'İndiriliyor','processing':'İşleniyor','ready':'İncelemeye hazır','failed':'Başarısız','deleted':'Silindi','expired':'Saklama süresi doldu'}
            await self.message(m.sender,'\n'.join(f"{j['id']} · {SUBJECTS[j['subject']]} · {labels.get(j['state'],'Bekliyor')}" for j in jobs) if jobs else 'Henüz dosya yok.');return
        if command.split(' ',1)[0] in ('/parcalar','/metin','/sil'):
            action,_,id=command.partition(' ');job=self.store.get(m.sender,id)
            if not job:await self.message(m.sender,'İş bulunamadı. /durum ile kendi dosyalarını görebilirsin.');return
            if id in self.busy or job['state'] in ('queued','downloading','processing'):await self.message(m.sender,'Bu dosya şu anda işleniyor veya gönderiliyor. /durum ile kontrol et.');return
            if action=='/sil':
                shutil.rmtree(self.job_dir(id),ignore_errors=True);self.store.forget(id);await self.message(m.sender,'Dosya, parçalar ve metin taslağı sunucudan silindi. Telegram’a daha önce gönderilen kopyaları sohbetten ayrıca silebilirsin.');return
            if job['state']!='ready':await self.message(m.sender,'Dosya hazır değil. Gerekirse PDF’yi yeniden ilet.');return
            await self.deliver(job,text_only=action=='/metin');return
        if m.document is None:return
        if m.mime not in ('application/pdf','application/octet-stream') or (m.mime=='application/octet-stream' and not m.filename.lower().endswith('.pdf')):
            await self.message(m.sender,'Yalnız PDF dosyası ilet.');return
        if not 0<m.size<=self.settings.max_file_bytes:await self.message(m.sender,'PDF dosya boyutu sınırını aşıyor veya boyutu okunamadı.');return
        if self.queue.full():await self.message(m.sender,'Dosya sırası dolu. İşlemler bitince yeniden ilet.');return
        used=sum(p.stat().st_size for p in (self.root/'jobs').rglob('*') if p.is_file() and not p.is_symlink())
        if used+4*m.size>self.settings.quota_bytes or shutil.disk_usage(self.root).free<4*m.size+256*1024*1024:
            await self.message(m.sender,'Sunucuda dosya alanı yetersiz. /sil ile eski işleri temizle.');return
        job,created=self.store.create(m.sender,m.message_id)
        if not created:await self.message(m.sender,'Bu mesaj zaten kaydedildi. İş: '+job['id']);return
        self.queue.put_nowait((job,m.document))
        await self.message(m.sender,'PDF sıraya alındı. İş: '+job['id']+' · Sonucu /durum ile kontrol edebilirsin.')
    async def run_job(self,job,document):
        id=job['id'];user=job['user_id'];folder=self.job_dir(id);source=folder/'original.pdf';part=folder/'download.part';output=folder/'processed';self.busy.add(id)
        try:
            folder.mkdir(exist_ok=True,mode=0o700)
            used=sum(p.stat().st_size for p in (self.root/'jobs').rglob('*') if p.is_file() and not p.is_symlink())
            if used+self.settings.max_file_bytes>self.settings.quota_bytes:raise ValueError('output_quota')
            self.store.update(id,'downloading')
            def progress(current,total):
                if current>self.settings.max_file_bytes or total>self.settings.max_file_bytes:raise ValueError('download_limit')
            await asyncio.wait_for(self.transport.download(document,part,progress),900)
            if part.stat().st_size<1 or part.stat().st_size>self.settings.max_file_bytes:raise ValueError('download_limit')
            part.rename(source);sha=await asyncio.to_thread(digest,source);self.store.update(id,'processing',source_sha=sha)
            result=await self.processor(source,output,self.settings)
            self.store.update(id,'ready',result=json.dumps(result,ensure_ascii=False))
            pending=sum(p['extraction']=='ocr-pending' for p in result['pageRecords'])
            await self.message(user,f"İş {id}: {result['sourcePages']} sayfa, {len(result['parts'])} parça hazır. "+('Metin katmanı olmayan sayfalar için OCR kapalı; sunucuda etkinleştirilmeli. ' if pending else 'Metin taslağı çıkarıldı; doğruluk incelemesi gerekiyor. ')+f"Metin: /metin {id}. Uygulamaya otomatik yayın yapılmadı.")
        except asyncio.CancelledError:
            self.store.update(id,'failed',error='interrupted');raise
        except Exception as error:
            code=str(error) if isinstance(error,ValueError) and str(error) in ERRORS else 'download_or_process_failed'
            self.store.update(id,'failed',error=code)
            await self.message(user,f'İş {id} tamamlanamadı. '+ERRORS.get(code,'İndirme/işlem tamamlanamadı; /durum ile kontrol edip dosyayı yeniden iletebilirsin.'))
        finally:
            self.busy.discard(id);part.unlink(missing_ok=True)
        ready=self.store.get(user,id)
        if ready['state']=='ready':await self.deliver(ready)
    async def deliver(self,job,text_only=False):
        id=job['id'];self.busy.add(id)
        try:
            result=json.loads(job['result']);folder=self.job_dir(id)/'processed'
            names=[result['textFile']] if text_only else [p['file'] for p in result['parts']]
            for name in names:
                path=folder/name
                if path.parent.resolve()!=folder.resolve() or path.is_symlink() or not path.is_file():raise ValueError('missing-file')
                await self.transport.file(job['user_id'],path,'İnceleme taslağı · İş '+id)
        except Exception:await self.message(job['user_id'],'Dosyalar sunucuda kayıtlı. Gönderim tamamlanamadı; /parcalar '+id+' veya /metin '+id+' ile yeniden dene.')
        finally:self.busy.discard(id)
    async def worker(self):
        while True:
            job,document=await self.queue.get()
            try:await self.run_job(job,document)
            except Exception:
                with contextlib.suppress(Exception):self.store.update(job['id'],'failed',error='worker_error')
            finally:self.queue.task_done()
    def recover(self):
        for job in self.store.pending():
            (self.job_dir(job['id'])/'download.part').unlink(missing_ok=True)
            self.store.update(job['id'],'failed',error='restarted')
    def cleanup(self):
        for job in self.store.expiring(self.settings.retention_days):
            if job['id'] in self.busy:continue
            shutil.rmtree(self.job_dir(job['id']),ignore_errors=True);self.store.forget(job['id'],'expired')
