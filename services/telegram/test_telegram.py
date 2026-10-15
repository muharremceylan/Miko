"""Gerçek Telegram bağlantısı/anahtarı kullanmadan erişim ve PDF işleme kontrolleri."""
import asyncio
import dataclasses
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, DecodedStreamObject, DictionaryObject,
                          NameObject, NumberObject, TextStringObject)
from .config import Settings, ConfigurationError
from .core import Incoming, PDFService, process_in_subprocess
from .pdf import PDFError, process_pdf
from .setup import write_config
from .store import Store

# Yalnız test biçimindeki sahte değerler; Telegram hesabına ait değildir.
ENV={'TELEGRAM_API_ID':'12345','TELEGRAM_API_HASH':'a'*32,
     'TELEGRAM_BOT_TOKEN':'123456:'+('x'*32),'BOT_PAIRING_CODE':'p'*32}

def make_pdf(path,pages=4,payload_bytes=0,actions=False):
    writer=PdfWriter()
    font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
    for i in range(pages):
        page=writer.add_blank_page(width=612,height=792)
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
        content=DecodedStreamObject();content.set_data(f'BT /F1 18 Tf 40 700 Td (Page {i+1}: original test lesson with sufficient text for extraction.) Tj ET'.encode())
        page[NameObject('/Contents')]=writer._add_object(content)
        if payload_bytes:
            payload=DecodedStreamObject();payload.set_data(bytes([i%256])*payload_bytes)
            page[NameObject('/TestPayload')]=writer._add_object(payload)
        if actions:
            action=DictionaryObject({NameObject('/S'):NameObject('/JavaScript'),NameObject('/JS'):TextStringObject('test-only')})
            page[NameObject('/AA')]=DictionaryObject({NameObject('/O'):writer._add_object(action)})
            annotation=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Link'),NameObject('/Rect'):ArrayObject([NumberObject(0)]*4),NameObject('/A'):writer._add_object(action)})
            page[NameObject('/Annots')]=ArrayObject([writer._add_object(annotation)])
    writer.write(path)

class PDFTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.source=self.root/'source.pdf';self.output=self.root/'out'
    def tearDown(self):self.temp.cleanup()
    def test_halves_keep_original_page_numbers_and_unreviewed_state(self):
        make_pdf(self.source,5);result=process_pdf(self.source,self.output)
        self.assertEqual([p['sourcePages'] for p in result['parts']],[[1,3],[4,5]])
        self.assertEqual([len(PdfReader(self.output/p['file']).pages) for p in result['parts']],[3,2])
        text=(self.output/result['textFile']).read_text()
        for i in range(1,6):self.assertIn(f'PDF SAYFASI {i}',text);self.assertIn(f'Page {i}:',text)
        self.assertFalse(result['automaticPublication']);self.assertFalse(result['expertApproved'])
        self.assertEqual(result['status'],'needs-review')
    def test_pdf_over_32_mib_is_split_below_25_mib(self):
        make_pdf(self.source,2,17*1024*1024)
        self.assertGreater(self.source.stat().st_size,32*1024*1024)
        result=process_pdf(self.source,self.output)
        self.assertEqual(len(result['parts']),2)
        self.assertTrue(all(p['bytes']<=25*1024*1024 for p in result['parts']))
        self.assertEqual([p['sourcePages'] for p in result['parts']],[[1,1],[2,2]])
    def test_oversize_halves_recursively_split_without_page_loss(self):
        make_pdf(self.source,8,2048);result=process_pdf(self.source,self.output,part_bytes=7500)
        pages=[i for p in result['parts'] for i in range(p['sourcePages'][0],p['sourcePages'][1]+1)]
        self.assertEqual(pages,list(range(1,9)));self.assertGreater(len(result['parts']),2)
        self.assertTrue(all(p['bytes']<=7500 for p in result['parts']))
    def test_oversize_single_page_fails_and_cleans_only_own_output(self):
        make_pdf(self.source,1,4096)
        with self.assertRaisesRegex(PDFError,'single_page_too_large'):process_pdf(self.source,self.output,part_bytes=1500)
        self.assertFalse(self.output.exists());self.assertTrue(self.source.exists())
    def test_existing_output_never_deleted_even_by_cli(self):
        make_pdf(self.source);self.output.mkdir();sentinel=self.output/'keep.txt';sentinel.write_text('keep')
        result=subprocess.run([sys.executable,'-m','services.telegram.pdf','--source',str(self.source),'--output',str(self.output)],capture_output=True,text=True)
        self.assertEqual(result.returncode,1);self.assertEqual(json.loads(result.stdout)['error'],'output_exists');self.assertEqual(sentinel.read_text(),'keep')
    def test_encrypted_pdf_is_rejected(self):
        writer=PdfWriter();writer.add_blank_page(100,100);writer.encrypt('private');writer.write(self.source)
        with self.assertRaisesRegex(PDFError,'encrypted_pdf'):process_pdf(self.source,self.output)
    def test_fake_pdf_and_malformed_pdf_are_rejected(self):
        for data,code in [(b'not a pdf','not_pdf'),(b'%PDF-1.7\nnot valid','invalid_pdf')]:
            with self.subTest(code=code):
                self.source.write_bytes(data)
                with self.assertRaisesRegex(PDFError,code):process_pdf(self.source,self.output)
                self.assertFalse(self.output.exists())
    def test_page_limit_and_output_quota(self):
        make_pdf(self.source,4)
        with self.assertRaisesRegex(PDFError,'page_limit'):process_pdf(self.source,self.output,max_pages=3)
        with self.assertRaisesRegex(PDFError,'output_quota'):process_pdf(self.source,self.output,max_output_bytes=1)
        self.assertFalse(self.output.exists())
    def test_known_active_actions_removed_from_written_pages(self):
        make_pdf(self.source,1,actions=True);result=process_pdf(self.source,self.output)
        page=PdfReader(self.output/result['parts'][0]['file']).pages[0]
        self.assertNotIn('/AA',page);self.assertNotIn('/A',page['/Annots'][0].get_object())
    def test_image_only_pages_explicitly_need_ocr(self):
        writer=PdfWriter();writer.add_blank_page(100,100);writer.write(self.source)
        result=process_pdf(self.source,self.output)
        self.assertEqual(result['pageRecords'][0]['extraction'],'ocr-pending')
    @unittest.skipUnless(shutil.which('tesseract') and shutil.which('pdftoppm'),'OCR araçları gerekli')
    def test_real_turkish_ocr_from_original_raster_fixture(self):
        # 5x7 harflerden özgün raster: üçüncü taraf ders notu veya görüntü içermez.
        glyphs={'T':['11111','00100','00100','00100','00100','00100','00100'],
                'A':['01110','10001','10001','11111','10001','10001','10001'],
                'R':['11110','10001','10001','11110','10100','10010','10001'],
                'I':['11111','00100','00100','00100','00100','00100','11111'],
                'H':['10001','10001','10001','11111','10001','10001','10001']}
        width,height,scale=520,180,12;pixels=bytearray([255])*(width*height)
        for n,char in enumerate('TARIH'):
            for y,row in enumerate(glyphs[char]):
                for x,value in enumerate(row):
                    if value=='1':
                        for dy in range(scale):
                            start=(40+y*scale+dy)*width+40+(n*6+x)*scale
                            pixels[start:start+scale]=bytes(scale)
        writer=PdfWriter();page=writer.add_blank_page(width,height)
        image=DecodedStreamObject();image.set_data(bytes(pixels));image.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Image'),NameObject('/Width'):NumberObject(width),NameObject('/Height'):NumberObject(height),NameObject('/ColorSpace'):NameObject('/DeviceGray'),NameObject('/BitsPerComponent'):NumberObject(8)})
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/XObject'):DictionaryObject({NameObject('/Im0'):writer._add_object(image)})})
        stream=DecodedStreamObject();stream.set_data(f'q {width} 0 0 {height} 0 0 cm /Im0 Do Q'.encode());page[NameObject('/Contents')]=writer._add_object(stream);writer.write(self.source)
        result=process_pdf(self.source,self.output,enable_ocr=True)
        self.assertEqual(result['pageRecords'][0]['extraction'],'ocr-unreviewed')
        self.assertIn('TAR',(self.output/result['textFile']).read_text().upper())
        self.assertFalse((self.output/'ocr-page.png').exists())

class SettingsTests(unittest.TestCase):
    def test_missing_configuration_fails_closed(self):
        with self.assertRaisesRegex(ConfigurationError,'Eksik ayarlar'):Settings.from_environment({})
    def test_limits_and_repr_do_not_expose_secrets(self):
        settings=Settings.from_environment(ENV)
        for key in ('TELEGRAM_API_HASH','TELEGRAM_BOT_TOKEN','BOT_PAIRING_CODE'):self.assertNotIn(ENV[key],repr(settings))
        for key,value in [('BOT_PART_MB','26'),('BOT_QUOTA_MB','50'),('BOT_RETENTION_DAYS','100'),('BOT_ENABLE_OCR','yes'),('TELEGRAM_API_HASH','bad\nvalue')]:
            with self.subTest(key=key),self.assertRaises(ConfigurationError):Settings.from_environment({**ENV,key:value})
    def test_config_written_private_and_existing_files_preserved(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'.env';link=write_config(path,'akademi_test_bot',ENV['TELEGRAM_API_ID'],ENV['TELEGRAM_API_HASH'],ENV['TELEGRAM_BOT_TOKEN'])
            self.assertEqual(stat.S_IMODE(path.stat().st_mode),0o600);self.assertEqual(stat.S_IMODE(link.stat().st_mode),0o600)
            self.assertTrue(link.read_text().startswith('https://t.me/akademi_test_bot?start='))
            before=path.read_bytes()
            with self.assertRaises(FileExistsError):write_config(path,'akademi_test_bot',ENV['TELEGRAM_API_ID'],ENV['TELEGRAM_API_HASH'],ENV['TELEGRAM_BOT_TOKEN'])
            self.assertEqual(path.read_bytes(),before)
    def test_missing_config_check_and_healthcheck_fail_closed(self):
        env={k:v for k,v in os.environ.items() if k not in ENV}
        result=subprocess.run([sys.executable,'-m','services.telegram.bot','--check'],capture_output=True,text=True,env=env)
        self.assertEqual(result.returncode,2);self.assertFalse(json.loads(result.stdout)['configured'])
        with tempfile.TemporaryDirectory() as root:
            env['BOT_DATA_DIR']=root
            command=[sys.executable,'-m','services.telegram.bot','--healthcheck']
            self.assertEqual(subprocess.run(command,env=env).returncode,1)
            (Path(root)/'heartbeat').write_text(str(time.time()))
            self.assertEqual(subprocess.run(command,env=env).returncode,0)
            (Path(root)/'heartbeat').write_text(str(time.time()-100))
            self.assertEqual(subprocess.run(command,env=env).returncode,1)

class BotAuthenticationTests(unittest.IsolatedAsyncioTestCase):
    async def test_personal_or_other_bot_session_is_rejected_and_disconnected(self):
        from types import SimpleNamespace
        from . import bot
        for bot_flag,identity in [(False,123456),(True,999999)]:
            with self.subTest(bot=bot_flag,id=identity),tempfile.TemporaryDirectory() as root:
                client=SimpleNamespace(connect=AsyncMock(),is_user_authorized=AsyncMock(return_value=True),get_me=AsyncMock(return_value=SimpleNamespace(bot=bot_flag,id=identity)),disconnect=AsyncMock(),sign_in=AsyncMock())
                settings=Settings.from_environment({**ENV,'BOT_DATA_DIR':root})
                with patch.object(bot,'TelegramClient',return_value=client),self.assertRaises(ConfigurationError):await bot.run(settings)
                client.sign_in.assert_not_awaited();client.disconnect.assert_awaited_once()
    async def test_new_session_uses_only_bot_token_and_never_phone_login(self):
        from types import SimpleNamespace
        from . import bot
        with tempfile.TemporaryDirectory() as root:
            client=SimpleNamespace(connect=AsyncMock(),is_user_authorized=AsyncMock(return_value=False),get_me=AsyncMock(return_value=None),disconnect=AsyncMock(),sign_in=AsyncMock())
            settings=Settings.from_environment({**ENV,'BOT_DATA_DIR':root})
            with patch.object(bot,'TelegramClient',return_value=client),self.assertRaises(ConfigurationError):await bot.run(settings)
            client.sign_in.assert_awaited_once_with(bot_token=ENV['TELEGRAM_BOT_TOKEN']);client.disconnect.assert_awaited_once()

class FakeTransport:
    def __init__(self):self.messages=[];self.files=[];self.downloads=[];self.send_fails=False
    async def message(self,user,text):self.messages.append((user,text))
    async def file(self,user,path,caption):
        if self.send_fails:raise RuntimeError('must-never-leak-secret')
        self.files.append((user,Path(path).name,Path(path).read_bytes()))
    async def download(self,document,path,progress):
        self.downloads.append(path);data=document if isinstance(document,bytes) else b'%PDF-invalid'
        progress(len(data),len(data));path.write_bytes(data)

class ServiceTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.settings=Settings.from_environment({**ENV,'BOT_DATA_DIR':str(self.root)})
        self.transport=FakeTransport();self.service=PDFService(self.settings,self.transport)
    async def asyncTearDown(self):self.service.store.db.close();self.temp.cleanup()
    async def pair(self,user=10):await self.service.handle(Incoming(user,user,1,True,text='/start '+ENV['BOT_PAIRING_CODE']))
    async def test_owner_binding_is_persistent_and_second_user_cannot_take_over(self):
        await self.pair();await self.pair(11);self.assertEqual(self.service.store.owner(),10)
        other=Store(self.root/'bot.sqlite3');self.assertEqual(other.owner(),10);other.db.close()
    async def test_wrong_pairing_code_and_groups_cannot_bind(self):
        await self.service.handle(Incoming(10,10,1,True,text='/start wrong'))
        await self.service.handle(Incoming(10,-100,2,False,text='/start '+ENV['BOT_PAIRING_CODE']))
        self.assertIsNone(self.service.store.owner())
    async def test_forwarded_text_and_document_captions_never_execute_commands(self):
        await self.service.handle(Incoming(10,10,1,True,text='/start '+ENV['BOT_PAIRING_CODE'],forwarded=True))
        self.assertIsNone(self.service.store.owner());await self.pair()
        await self.service.handle(Incoming(10,10,2,True,text='/ders tarih',forwarded=True))
        await self.service.handle(Incoming(10,10,3,True,text='/ders tarih',document=b'x',filename='a.pdf',size=1,mime='application/pdf'))
        self.assertEqual(self.service.store.subject(10),'belirsiz')
    async def test_pairing_rate_limit_prevents_code_after_five_failures(self):
        for i in range(5):await self.service.handle(Incoming(10,10,i,True,text='/start bad'))
        await self.pair();self.assertIsNone(self.service.store.owner())
    async def test_unauthorized_user_never_downloads_or_receives_files(self):
        await self.pair();await self.service.handle(Incoming(11,11,1,True,document=b'x',filename='a.pdf',size=1,mime='application/pdf'))
        self.assertTrue(self.service.queue.empty());self.assertFalse(self.transport.downloads);self.assertFalse(self.transport.files)
    async def test_ders_validates_and_job_captures_subject(self):
        await self.pair();await self.service.handle(Incoming(10,10,2,True,text='/ders Türkçe'))
        self.assertEqual(self.service.store.subject(10),'turkce')
        await self.service.handle(Incoming(10,10,3,True,text='/ders ../../other'))
        job,_=self.service.store.create(10,4);self.assertEqual(job['subject'],'turkce')
    async def test_queue_backpressure_and_message_idempotency(self):
        await self.pair()
        msg=Incoming(10,10,2,True,document=b'x',filename='../../escape.pdf',size=1,mime='application/pdf')
        await self.service.handle(msg);await self.service.handle(msg);self.assertEqual(self.service.queue.qsize(),1)
        for i in range(3,7):await self.service.handle(dataclasses.replace(msg,message_id=i))
        self.assertEqual(self.service.queue.qsize(),3);self.assertFalse((self.root.parent/'escape.pdf').exists())
    async def test_mime_and_declared_size_are_checked_before_enqueue(self):
        await self.pair()
        for mime,size,name in [('text/plain',1,'a.pdf'),('application/pdf',0,'a.pdf'),('application/pdf',self.settings.max_file_bytes+1,'a.pdf'),('application/octet-stream',1,'a.exe')]:
            await self.service.handle(Incoming(10,10,2,True,document=b'x',filename=name,size=size,mime=mime))
        self.assertTrue(self.service.queue.empty())
    async def test_real_subprocess_pipeline_and_owner_only_deletion(self):
        await self.pair();source=self.root/'fixture.pdf';make_pdf(source,3)
        job,_=self.service.store.create(10,2);await self.service.run_job(job,source.read_bytes())
        ready=self.service.store.get(10,job['id']);self.assertEqual(ready['state'],'ready')
        self.assertEqual(len(self.transport.files),2);self.assertTrue(all(f[0]==10 for f in self.transport.files))
        await self.service.handle(Incoming(11,11,3,True,text='/sil '+job['id']))
        self.assertTrue(self.service.job_dir(job['id']).exists())
        await self.service.handle(Incoming(10,10,4,True,text='/metin '+job['id']))
        self.assertEqual(self.transport.files[-1][1],'text-unreviewed.txt')
        await self.service.handle(Incoming(10,10,5,True,text='/sil '+job['id']))
        self.assertFalse(self.service.job_dir(job['id']).exists());self.assertEqual(self.service.store.get(10,job['id'])['state'],'deleted')
        self.assertIsNone(self.service.store.get(10,job['id'])['source_sha'])
    async def test_download_actual_size_enforced_and_partial_removed(self):
        await self.pair();self.service.settings=dataclasses.replace(self.settings,max_file_bytes=8)
        job,_=self.service.store.create(10,2);await self.service.run_job(job,b'x'*9)
        self.assertEqual(self.service.store.get(10,job['id'])['state'],'failed')
        self.assertFalse((self.service.job_dir(job['id'])/'download.part').exists());self.assertFalse(self.transport.files)
    async def test_failure_does_not_stop_next_queued_job_or_expose_exception(self):
        await self.pair();calls=0
        async def processor(source,output,settings):
            nonlocal calls
            calls+=1
            if calls==1:raise RuntimeError('must-never-leak-secret')
            return await process_in_subprocess(source,output,settings)
        self.service.processor=processor;source=self.root/'fixture.pdf';make_pdf(source,1)
        jobs=[self.service.store.create(10,i)[0] for i in (2,3)]
        for job in jobs:self.service.queue.put_nowait((job,source.read_bytes()))
        worker=asyncio.create_task(self.service.worker())
        try:await asyncio.wait_for(self.service.queue.join(),10)
        finally:
            worker.cancel()
            with self.assertRaises(asyncio.CancelledError):await worker
        self.assertEqual([self.service.store.get(10,j['id'])['state'] for j in jobs],['failed','ready'])
        self.assertNotIn('must-never-leak-secret',str(self.transport.messages))
    async def test_restart_marks_incomplete_job_and_cleans_partial(self):
        await self.pair();job,_=self.service.store.create(10,2);folder=self.service.job_dir(job['id']);folder.mkdir();(folder/'download.part').write_bytes(b'partial')
        self.service.recover();self.assertEqual(self.service.store.get(10,job['id'])['error'],'restarted');self.assertFalse((folder/'download.part').exists())
    async def test_retention_removes_private_files_and_clears_content_metadata(self):
        await self.pair();job,_=self.service.store.create(10,2);folder=self.service.job_dir(job['id']);folder.mkdir();(folder/'original.pdf').write_bytes(b'private')
        self.service.store.update(job['id'],'ready',source_sha='secret',result='{}')
        with self.service.store.db:self.service.store.db.execute('UPDATE jobs SET updated=? WHERE id=?',(time.time()-8*86400,job['id']))
        self.service.cleanup();record=self.service.store.get(10,job['id'])
        self.assertFalse(folder.exists());self.assertEqual(record['state'],'expired');self.assertIsNone(record['result']);self.assertIsNone(record['source_sha'])
    async def test_delivery_failure_keeps_ready_files_for_retry(self):
        await self.pair();source=self.root/'fixture.pdf';make_pdf(source,1)
        job,_=self.service.store.create(10,2);self.transport.send_fails=True;await self.service.run_job(job,source.read_bytes())
        self.assertEqual(self.service.store.get(10,job['id'])['state'],'ready')
        self.assertNotIn('must-never-leak-secret',str(self.transport.messages));self.transport.send_fails=False
        await self.service.handle(Incoming(10,10,3,True,text='/parcalar '+job['id']))
        self.assertEqual(len(self.transport.files),1)
    async def test_delivery_rejects_path_escape_and_symlink(self):
        await self.pair();job,_=self.service.store.create(10,2);folder=self.service.job_dir(job['id'])/'processed';folder.mkdir(parents=True);outside=self.root/'private.txt';outside.write_text('private')
        for filename in ('../../../private.txt','link.txt'):
            if filename=='link.txt':(folder/filename).symlink_to(outside)
            self.service.store.update(job['id'],'ready',result=json.dumps({'parts':[{'file':filename}]}))
            await self.service.deliver(self.service.store.get(10,job['id']))
        self.assertFalse(self.transport.files)

if __name__=='__main__':unittest.main()
