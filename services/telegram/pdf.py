"""PDF ayrıştırma ayrı süreçte yapılır. Ham OCR kaynak veridir; komut veya AI sonucu değildir."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

class PDFError(Exception):pass

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def ocr_page(source,page,work):
    prefix=work/'ocr-page'
    try:
        subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-r','135','-scale-to','1800','-singlefile','-png',str(source),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=35)
        output=subprocess.run(['tesseract',str(prefix)+'.png','stdout','-l','tur','--psm','11'],check=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=40,env={**os.environ,'OMP_THREAD_LIMIT':'1'})
        if len(output.stdout)>200000:raise PDFError('ocr_output_limit')
        return output.stdout.decode('utf-8',errors='replace')[:20000]
    except (subprocess.SubprocessError,OSError):raise PDFError('ocr_failed') from None
    finally:Path(str(prefix)+'.png').unlink(missing_ok=True)

def process_pdf(source,output,*,part_bytes=25*1024*1024,max_pages=1000,enable_ocr=False,max_output_bytes=1024*1024*1024):
    source=Path(source);output=Path(output)
    created=False
    try:
        if output.exists():raise PDFError('output_exists')
        with source.open('rb') as f:
            if not f.read(1024).lstrip().startswith(b'%PDF-'):raise PDFError('not_pdf')
        reader=PdfReader(source,strict=False)
        if reader.is_encrypted:raise PDFError('encrypted_pdf')
        count=len(reader.pages)
        if count<1 or count>max_pages:raise PDFError('page_limit')
        output.mkdir(parents=True,exist_ok=False,mode=0o700);created=True;parts=[]
        def split(start,stop):
            if len(parts)>=128:raise PDFError('part_count_limit')
            path=output/f'part-{len(parts)+1:03}.pdf';writer=PdfWriter()
            for index in range(start,stop):
                page=writer.add_page(reader.pages[index],excluded_keys=['/AA'])
                for reference in page.get('/Annots',[]):
                    annotation=reference.get_object();action=annotation.get('/A')
                    if action and action.get_object().get('/S') in ['/JavaScript','/Launch','/SubmitForm','/ImportData']:annotation.pop('/A',None)
                    annotation.pop('/AA',None)
            with path.open('wb') as f:writer.write(f)
            size=path.stat().st_size
            if size>part_bytes:
                path.unlink()
                if stop-start==1:raise PDFError('single_page_too_large')
                middle=(start+stop)//2;split(start,middle);split(middle,stop)
            else:
                if sum(p['bytes'] for p in parts)+size>max_output_bytes:raise PDFError('output_quota')
                parts.append({'file':path.name,'sourcePages':[start+1,stop],'bytes':size,'sha256':digest(path)})
        if count>1:middle=(count+1)//2;split(0,middle);split(middle,count)
        else:split(0,count)
        page_records=[];text_path=output/'text-unreviewed.txt'
        with text_path.open('w',encoding='utf-8') as f:
            for number,page in enumerate(reader.pages,1):
                text=(page.extract_text(extraction_mode='plain') or '')[:20000];kind='text-layer'
                if len(text.strip())<40:
                    if enable_ocr:text=ocr_page(source,number,output);kind='ocr-unreviewed' if text.strip() else 'empty'
                    else:kind='ocr-pending'
                page_records.append({'sourcePage':number,'extraction':kind,'characters':len(text)})
                block=f'\n=== PDF SAYFASI {number} ===\n{text}\n'
                if f.tell()+len(block.encode())+sum(p['bytes'] for p in parts)>max_output_bytes:raise PDFError('output_quota')
                f.write(block)
        manifest={'schemaVersion':1,'status':'needs-review','sourceSha256':digest(source),'sourcePages':count,'expertApproved':False,'automaticPublication':False,'parts':parts,'textFile':text_path.name,'pageRecords':page_records,'activeActionsRemoved':True}
        (output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        return manifest
    except PDFError:
        if created:shutil.rmtree(output,ignore_errors=True)
        raise
    except Exception:
        if created:shutil.rmtree(output,ignore_errors=True)
        raise PDFError('invalid_pdf') from None

ERRORS={
 'output_quota':'İşlenmiş dosyalar için ayrılan disk sınırı aşıldı.', 'output_exists':'Çıktı klasörü zaten var; mevcut dosyalar değiştirilmedi.', 'not_pdf':'Dosyanın içeriği PDF değil.', 'encrypted_pdf':'PDF şifreli. Parola koruması kaldırılmış bir kopya gerekiyor.',
 'page_limit':'PDF boş veya sayfa sınırını aşıyor.', 'single_page_too_large':'Tek bir sayfa bile parça sınırını aşıyor; görüntü sıkıştırması gerekiyor.',
 'part_count_limit':'Çok fazla parça oluşuyor; dosya daha küçük bir kaynakla yeniden denenmeli.', 'invalid_pdf':'PDF güvenle işlenemedi.',
 'ocr_failed':'Türkçe OCR tamamlanamadı. Sunucudaki OCR araçlarını veya dosyayı kontrol et.', 'ocr_output_limit':'OCR metni işlem sınırını aştı.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--output',required=True);parser.add_argument('--part-bytes',type=int,default=25*1024*1024);parser.add_argument('--max-pages',type=int,default=1000);parser.add_argument('--max-output-bytes',type=int,default=1024*1024*1024);parser.add_argument('--ocr',action='store_true');args=parser.parse_args()
    os.umask(0o077)
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_AS,(768*1024*1024,768*1024*1024))
        resource.setrlimit(resource.RLIMIT_CPU,(300,300))
    except ImportError:pass
    try:
        if args.part_bytes<1024 or not 1<=args.max_pages<=2000:raise PDFError('invalid_limits')
        result=process_pdf(args.source,args.output,part_bytes=args.part_bytes,max_pages=args.max_pages,enable_ocr=args.ocr,max_output_bytes=args.max_output_bytes)
        print(json.dumps({'status':result['status'],'partCount':len(result['parts'])}))
    except PDFError as error:
        print(json.dumps({'error':str(error) if str(error) in ERRORS else 'invalid_pdf'}));sys.exit(1)
if __name__=='__main__':main()
