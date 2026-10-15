"""Kullanıcının PDF notlarından oluşturulan ilk taslakların mobil akışı."""
import json,os
from playwright.sync_api import sync_playwright
BASE=os.environ.get('AKADEMI_TEST_URL','http://127.0.0.1:4173')
passed=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE);assert not page.locator('[data-notes-action="library"]').first.is_visible()
 page.locator('#exam-kpss').click();page.locator('#level-lisans').click()
 page.locator('#home [data-notes-action="library"]').click()
 assert page.locator('#pdfNotesTitle').inner_text()=='PDF ders notların'
 assert page.locator('[data-pdf-source]').count()==4
 assert '109 sayfa' in page.locator('[data-pdf-source="pdf-turkce-20261015"]').inner_text()
 assert '264 sayfa' in page.locator('[data-pdf-source="pdf-tarih-20261015"]').inner_text()
 for id in ['vatandaslik','cografya']:
  source=page.locator(f'[data-pdf-source="pdf-{id}-20261015"]');assert '32 MiB' in source.inner_text();assert source.locator('button,a').count()==0
 passed.append('Dört kaynak: Türkçe/Tarih sayfa sayısı ve kısmi inceleme; açılamayan iki dosyada doğru sınır ve çalışmayan kontrol yok')
 legacy=page.evaluate("localStorage.getItem('akademi_stats_v1')")
 for id,count,source in [('turkce-sozcukte-anlam',6,'PDF sayfası 1, 2'),('tarih-asya-hun',4,'PDF sayfası 3')]:
  page.evaluate('(id)=>AcademiNotes.openTopic(id)',id)
  assert source in page.locator('#pdfNotesScreen').inner_text()
  assert page.locator('#pdfNotesScreen .notebook-page').count()==count
  assert page.locator('#pdfNotesScreen .math-example').count()==2
  assert page.locator('#pdfNotesScreen .math-example ol[type=A] li').count()==10
  page.locator('#pdfNotesScreen .math-example details summary').first.click();assert 'Doğru cevap:' in page.locator('#pdfNotesScreen .math-example').first.inner_text()
  page.locator('#pdfNotesScreen [data-notes-action="note-style"][data-style="plain"]').click();assert page.locator('#pdfNotesScreen .notebook-page').count()==0
  page.locator('#pdfNotesScreen [data-style="notebook"]').click()
  page.locator('#pdfNotesScreen [data-section="summary"]').click()
  for level in ['quick','standard','detailed']:
   page.locator('#pdfNoteSummary').select_option(level);assert page.locator('#pdfNoteBody h3').count()==1
  assert page.evaluate('AcademiMath.back()') is True;assert page.locator('#pdfNotesTitle').is_visible()
 assert page.evaluate("localStorage.getItem('akademi_stats_v1')")==legacy
 passed.append('İki kaynaklı ders taslağı: renkli kartlar, tam metin, üç özet ve dört özgün beş seçenekli örnek; eski sayaçlar değişmez')
 page.evaluate("AcademiNotes.openTopic('turkce-sozcukte-anlam')");page.evaluate("openLesson('matematik')")
 assert page.locator('#pdfNotesScreen').is_hidden();assert page.locator('#mathProgressPercent').is_visible()
 page.evaluate("AcademiNotes.openTopic('tarih-asya-hun');navTo('home');navTo('lessons')")
 assert page.locator('#pdfNotesScreen').is_hidden();assert page.locator('#subjectList').is_visible()
 passed.append('PDF/Matematik, ana sayfa ve geri tuşu geçişlerinde ekran çakışmaz')
 for width in [320,390,412,768]:
  page.set_viewport_size({'width':width,'height':844})
  for theme in ['light','dark']:
   if page.locator('html').get_attribute('data-theme')!=theme:page.locator('#themeToggle').click()
   page.evaluate('AcademiNotes.open()');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   for id in ['turkce-sozcukte-anlam','tarih-asya-hun']:
    page.evaluate('(id)=>AcademiNotes.openTopic(id)',id);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('#pdfNotesScreen [data-section="summary"]').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.evaluate("selectKpssLevel('onlisans');AcademiNotes.open()")
 assert page.locator('#pdfNotesScreen').is_hidden()
 assert page.locator('#lessonList [data-notes-action="library"]').is_hidden()
 assert not errors,errors
 passed.append('320–768 piksel ve iki tema; Lisans dışındaki alanlarda PDF taslakları açılmaz')
 browser.close()
print(json.dumps({'passed':passed,'page_errors':errors},ensure_ascii=False,indent=2))
