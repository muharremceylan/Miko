"""Aday kaynaklar ve otomatik alıştırmalar: gerçek mobil tarayıcı akışı."""
import os,json
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('AKADEMI_TEST_URL','http://127.0.0.1:4173')
KEY='akademi_math_v1_kpss_lisans'
passed=[]
def record(page):return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
def active(page):
 s=record(page);return next(a for a in s['attempts'] if a['id']==s['activeAttempt'])
def topic(page,id='temel'):page.evaluate('(id)=>AcademiMath.openTopic(id,"test")',id)
def auto(page):page.locator('#mathQuestionSource').select_option('generated')
def answer(page,correct=True):
 a=active(page);q=a['questions'][a['current']]
 page.locator('#mathAnswers button').nth(q['answer'] if correct else (q['answer']+1)%5).click()
 page.locator('[data-math-action="next"]').click()
def start(page):page.goto(BASE);page.locator('#exam-kpss').click();page.locator('#level-lisans').click()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 start(page);page.evaluate('AcademiMath.open()');page.locator('[data-math-action="sources"]').click()
 assert page.locator('#mathSourcesTitle').inner_text()=='Kaynak kütüphanesi'
 assert page.locator('.math-source').count()==6
 assert 'incelenemedi' in page.locator('#mathTopicScreen').inner_text()
 for link in page.locator('.source-external').all():
  assert link.get_attribute('href').startswith('https://')
  assert link.get_attribute('target')=='_blank'
  assert 'noopener' in link.get_attribute('rel')
 for use,count in [('questions',4),('lesson',3),('exam',1),('scope',1),('all',6)]:
  page.locator('#mathSourceUse').select_option(use);assert page.locator('.math-source').count()==count
 assert page.evaluate('AcademiMath.back()') is True
 topic(page,'sayilar-bolme');page.locator('#mathTopicScreen [data-math-action="sources"]').click();assert 'Çalıştığın konu: Bölme' in page.locator('#mathTopicScreen').inner_text()
 page.locator('#mathTopicScreen [data-math-action="topic"]').click();assert page.locator('#math-tab-test').get_attribute('aria-selected')=='true'
 passed.append('Altı aday kaynak, amaç filtresi, güvenli dış bağlantı ve konu/geri dönüş akışı; içerik incelenmiş veya izinli gibi gösterilmez')

 topic(page,'sayilar');auto(page);assert '14 özgün soru kalıbı' in page.locator('#mathGenerateSettings').inner_text()
 page.locator('[data-math-action="generate"][data-count="30"]').click()
 first=active(page);assert len(first['questions'])==len({q['id'] for q in first['questions']})==30
 assert len({q['topicId'] for q in first['questions']})==7
 assert 'Otomatik alıştırma' in page.locator('#mathTestQuestion').inner_text()
 assert page.locator('#mathAnswers button').count()==5
 for _ in range(2):answer(page)
 page.reload();page.evaluate('AcademiMath.open()');page.locator('[data-math-action="resume-test"]').click()
 assert active(page)['id']==first['id'] and active(page)['questions']==first['questions']
 for i in range(2,29):answer(page,i<15)
 page.locator('[data-math-action="skip"]').click()
 assert '15 doğru, 14 yanlış, 1 boş' in page.locator('#mathResultSummary').inner_text()
 page.locator('#mathTestResult [data-math-action="review-wrong"]').click()
 assert '14 uygun soru' in page.locator('#mathPoolCount').inner_text()
 page.locator('#mathTestResult [data-math-action="mistakes"]').click();assert page.locator('.math-mistake').count()==14
 assert page.locator('.math-mistake .note').count()==14
 qid=page.locator('[data-math-action="review-one"]').first.get_attribute('data-question')
 page.locator('[data-math-action="review-one"]').first.click();assert active(page)['questions'][0]['id']==qid
 answer(page);page.locator('#mathTestResult [data-math-action="mistakes"]').click();assert page.locator('.math-mistake').count()==13
 passed.append('30 yeni otomatik soru yedi alt konuyu kapsar; yenilemede aynı sırayla sürer, sonuç/yanlış filtresi/defter ve aynı sürümle tekrar çözme çalışır')

 topic(page,'temel');auto(page);page.locator('#mathGenerateDifficulty').select_option('Orta');page.locator('#mathGeneratedMode').select_option('assessment')
 page.locator('[data-math-action="generate"][data-count="20"]').click()
 assert all(q['difficulty']=='Orta' for q in active(page)['questions'])
 q=active(page)['questions'][0];page.locator('#mathAnswers button').nth((q['answer']+1)%5).click()
 assert page.locator('#mathAnswers .correct').count()==0 and 'Doğru cevap:' not in page.locator('#mathTopicPanel').inner_text()
 page.evaluate('AcademiMath.openMistakes()');assert page.locator('.math-mistake').count()==13
 assert page.locator('[data-math-action="review-one"]:disabled').count()==13
 page.locator('#mathTopicScreen [data-math-action="resume-test"]').click();page.locator('[data-math-action="finish"]').click()
 page.locator('#mathTestResult [data-math-action="mistakes"]').click();assert page.locator('.math-mistake').count()==14
 passed.append('Düzey ve 20 soruluk değerlendirme; çözüm test bitmeden açılmaz, yarım testte ikinci test engellenir')

 for tid in ['temel','sayilar-sayi-kumeleri','sayilar-dogal-sayilar','sayilar-tam-sayilar','sayilar-faktoriyel','sayilar-sayma-sistemleri','sayilar-bolme','sayilar-bolunebilme-kurallari']:
  topic(page,tid);auto(page);page.locator('#mathGenerateDifficulty').select_option('mixed');page.locator('#mathGeneratedMode').select_option('learn')
  used={q['id'] for a in record(page)['attempts'] for q in a['questions']}
  page.locator('[data-math-action="generate"][data-count="10"]').click()
  assert all(q['topicId']==tid and q['id'] not in used for q in active(page)['questions'])
  answer(page);page.locator('[data-math-action="finish"]').click()
 passed.append('Sekiz desteklenen konuda 10 soruluk üretim; önceki otomatik varyasyonlar yeniden seçilmez')

 # Sonlu havuz bittiğinde soru uydurulmaz veya yinelenmez.
 limited=browser.new_page(viewport={'width':390,'height':844});limited.on('pageerror',lambda e:errors.append(str(e)));limited.on('dialog',lambda d:d.accept());start(limited)
 topic(limited,'sayilar-dogal-sayilar');auto(limited);limited.locator('#mathGenerateDifficulty').select_option('Kolay')
 assert '57 yeni varyasyon' in limited.locator('#mathGenerateCount').inner_text()
 for count in [30,20,7]:
  limited.locator(f'[data-math-action="generate"][data-count="{count}"]').click();limited.locator('[data-math-action="finish"]').click()
 assert '0 yeni varyasyon' in limited.locator('#mathGenerateCount').inner_text()
 assert limited.locator('[data-math-action="generate"]:disabled').count()==3
 assert len({q['id'] for a in record(limited)['attempts'] for q in a['questions']})==57
 limited.close();passed.append('30/20/7 ile 57 varyasyon tüketildiğinde boş durum ve pasif düğmeler gösterilir; sahte sınırsız havuz yok')

 for width in [320,390,412,768]:
  page.set_viewport_size({'width':width,'height':844})
  for theme in ['light','dark']:
   if page.locator('html').get_attribute('data-theme')!=theme:page.locator('#themeToggle').click()
   page.evaluate('AcademiMath.openSources()');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   topic(page,'sayilar-bolunebilme-kurallari');auto(page);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 Path('test-artifacts').mkdir(exist_ok=True);page.set_viewport_size({'width':390,'height':844});page.screenshot(path='test-artifacts/otomatik-alistirma.png',full_page=True)
 page.evaluate("selectKpssLevel('onlisans');AcademiMath.openSources()")
 assert not page.locator('#mathSourcesTitle').is_visible()
 assert not errors,errors
 passed.append('Kaynaklar ve üretici 320–768 pikselde iki tema ile taşmaz; Ön Lisans alanına Lisans ekranı sızmaz')
 browser.close()
print(json.dumps({'passed':passed,'page_errors':errors},ensure_ascii=False,indent=2))
