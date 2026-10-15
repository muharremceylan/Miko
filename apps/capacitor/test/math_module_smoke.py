"""Matematik: gerçek mobil web akışı, kalıcı kayıtlar ve içerik durumları."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('AKADEMI_TEST_URL','http://127.0.0.1:4173')
KEY='akademi_math_v1_kpss_lisans'
passed=[]
def record(page): return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
def active(page):
 s=record(page)
 return next(a for a in s['attempts'] if a['id']==s['activeAttempt'])
def tab(page,name): page.locator('#math-tab-'+name).click()
def math_home(page): page.evaluate("openLesson('matematik')")
def topic(page,name='temel'): page.evaluate('(id)=>AcademiMath.openTopic(id)',name)
def answer(page,correct=True):
 a=active(page);q=a['questions'][a['current']]
 page.locator('#mathAnswers button').nth(q['answer'] if correct else (q['answer']+1)%5).click()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':390,'height':844},timezone_id='Europe/Istanbul')
 legacy=json.dumps({'solved':2,'correct':1,'topics':{'matematik':{'solved':2,'correct':1}}})
 context.add_init_script("if(!localStorage.getItem('akademi_stats_v1'))localStorage.setItem('akademi_stats_v1',"+json.dumps(legacy)+")")
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 page.goto(BASE);page.locator('#exam-kpss').click();page.locator('#level-lisans').click()
 math_home(page)
 assert page.locator('#mathSolved').inner_text()=='2'
 assert page.locator('#mathAccuracy').inner_text()=='%50'
 assert page.locator('#mathCompleted').inner_text()=='0'
 assert page.locator('#mathRemaining').inner_text()=='34'
 assert page.locator('#mathProgressPercent').inner_text()=='%0'
 assert page.locator('[data-math-topic]').count()==17
 page.locator('[data-math-topic="temel"] [data-math-action="topic"]').click()
 assert page.locator('#mathTopicTitle').inner_text()=='Temel Kavramlar'
 assert page.get_by_role('tab').count()==7
 assert page.locator('#mathTopicPanel h3').count()==10
 passed.append('Matematik ana ekranı: önceki matematik sayaçları korunur, ilerleme ayrı ve 34 konuya bağlıdır')

 tab(page,'summary')
 for level,title in [('quick','1 dakikalık hızlı tekrar'),('standard','5 dakikalık standart özet'),('detailed','Ayrıntılı tekrar notları')]:
  page.locator('#mathSummaryLevel').select_option(level)
  assert page.locator('#mathTopicPanel h3').inner_text()==title
 tab(page,'formulas');assert page.locator('.math-formula').count()==8
 tab(page,'examples');assert page.locator('.math-example').count()==3
 assert page.locator('.math-example ol[type="A"] li').count()==15
 page.locator('.math-example details summary').first.click()
 assert 'Alternatif yöntem' in page.locator('.math-example').first.inner_text()
 tab(page,'audio');assert 'henüz hazırlanmadı' in page.locator('#mathTopicPanel').inner_text()
 assert page.locator('#mathTopicPanel button:visible').count()==0
 assert 'seslendirme metni' in page.locator('#mathTopicPanel h3').inner_text()
 tab(page,'ai');assert 'henüz bağlı değil' in page.locator('#mathTopicPanel').inner_text()
 assert page.locator('#mathTopicPanel button, #mathTopicPanel input').count()==0
 passed.append('Üç özet, sekiz formül, üç beş seçenekli örnek; gerçek ses/AI olmadan açık durum ve kullanılmayan kontrol yok')

 tab(page,'test');assert '30 uygun soru' in page.locator('#mathPoolCount').inner_text()
 page.locator('[data-math-action="start"][data-count="30"]').click()
 first=active(page);assert len(set(q['id'] for q in first['questions']))==30
 assert page.locator('#mathAnswers button').count()==5
 for i in range(2):
  answer(page);page.locator('[data-math-action="next"]').click()
 page.locator('#themeToggle').click()
 assert active(page)['id']==first['id'] and active(page)['current']==2
 page.reload();math_home(page);page.locator('[data-math-action="resume-test"]').click()
 assert active(page)['id']==first['id'] and active(page)['questions']==first['questions']
 assert 'Soru 3 / 30' in page.locator('#mathTestQuestion').inner_text()
 for i in range(2,29):
  answer(page,correct=i<15)
  assert page.locator('#mathAnswers button:disabled').count()==5
  page.locator('[data-math-action="next"]').click()
 page.locator('[data-math-action="skip"]').click()
 assert '15 doğru, 14 yanlış, 1 boş' in page.locator('#mathResultSummary').inner_text()
 assert '%52' in page.locator('#mathResultSummary').inner_text()
 assert page.locator('.math-review').count()==30
 assert page.evaluate("localStorage.getItem('akademi_stats_v1')")==legacy
 page.evaluate("navTo('analytics')")
 assert page.locator('#aCount').inner_text()=='31'
 assert page.locator('#aCorrect').inner_text()=='16'
 page.evaluate("navTo('home')");assert page.locator('#qCount').inner_text()=='29'
 page.locator('#level-onlisans').click();assert page.locator('#qCount').inner_text()=='0'
 page.locator('#level-lisans').click();assert page.locator('#qCount').inner_text()=='29'
 math_home(page);assert page.locator('#mathSolved').inner_text()=='31'
 assert page.locator('#mathProgressPercent').inner_text()=='%0'
 passed.append('30 farklı soru; tema/yenilemede sürdürme; 15 doğru/14 yanlış/1 boş; genel sayaçlara tek ekleme ve düzey ayrımı')

 topic(page);tab(page,'test')
 page.locator('#mathTestFilter').select_option('wrong')
 assert '14 uygun soru' in page.locator('#mathPoolCount').inner_text()
 assert page.locator('[data-math-action="start"][data-count="20"]').is_disabled()
 page.locator('[data-math-action="start"][data-count="10"]').click()
 for _ in range(10):answer(page);page.locator('[data-math-action="next"]').click()
 assert '4 uygun soru' in page.locator('#mathPoolCount').inner_text()
 page.locator('#mathTestFilter').select_option('unseen')
 assert '1 uygun soru' in page.locator('#mathPoolCount').inner_text()
 page.get_by_role('button',name='Rastgele bir soru çöz',exact=True).click();answer(page);page.locator('[data-math-action="next"]').click()
 assert '0 uygun soru' in page.locator('#mathPoolCount').inner_text()
 assert page.get_by_role('button',name='Rastgele bir soru çöz',exact=True).is_disabled()
 page.locator('#mathTestFilter').select_option('all');page.locator('#mathTestMode').select_option('assessment')
 page.locator('[data-math-action="start"][data-count="20"]').click()
 assert len(active(page)['questions'])==20
 answer(page);assert page.locator('#mathAnswers .correct').count()==0
 assert 'Doğru cevap:' not in page.locator('#mathTopicPanel').inner_text()
 page.locator('[data-math-action="finish"]').click()
 assert '1 doğru, 0 yanlış, 19 boş' in page.locator('#mathResultSummary').inner_text()
 page.locator('.math-review summary').first.click();assert 'Doğru cevap:' in page.locator('.math-review').first.inner_text()
 passed.append('10/20/30, rastgele, yanlış, çözülmemiş ve yetersiz havuz; değerlendirme modunda çözümler bitişte açılır')

 tab(page,'lesson');page.locator('[data-math-action="complete"]').click()
 math_home(page);assert page.locator('#mathProgressPercent').inner_text()=='%3'
 assert page.locator('#mathCompleted').inner_text()=='1'
 assert page.locator('#mathRemaining').inner_text()=='33'
 page.locator('[data-math-action="resume"]').click();assert page.locator('#mathTopicTitle').inner_text()=='Temel Kavramlar'
 tab(page,'formulas');page.locator('#math-tab-formulas').focus();page.keyboard.press('ArrowRight')
 assert page.get_by_role('tab',name='Çözümlü Örnekler').get_attribute('aria-selected')=='true'
 page.keyboard.press('End');assert page.get_by_role('tab',name='Yapay Zekâya Sor').get_attribute('aria-selected')=='true'
 # Every main and subtopic opens without inventing missing content.
 curriculum=json.loads((Path(__file__).resolve().parents[3]/'akademi_ai_prototip/content/kpss/lisans/matematik/curriculum.json').read_text())
 for node in curriculum['topics']:
  topic(page,node['id']);assert page.locator('#mathTopicTitle').inner_text()==node['title']
  assert page.get_by_role('tab').count()==7
  if node['id']!='temel':assert 'hazırlanıyor' in page.locator('#mathTopicPanel').inner_text()
 passed.append('Tamamlama %3; son konu/sekme, klavye sekmeleri ve 39 ana/alt konu ekranı çalışır')

 topic(page)
 for width in [320,360,390,412,768]:
  page.set_viewport_size({'width':width,'height':844})
  for theme in ['light','dark']:
   if page.locator('html').get_attribute('data-theme')!=theme:page.locator('#themeToggle').click()
   for name in ['lesson','summary','formulas','examples','test','audio','ai']:
    tab(page,name);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme,name)
   math_home(page);page.locator('#mathAnnualTab').click()
   assert page.locator('#mathYear').input_value()=='2024'
   assert page.locator('#annualComputedTotal').inner_text()=='28'
   topic(page)
 passed.append('Yedi sekme: 320–768 piksel ve iki tema; kaynak dağılımı ve tutarsızlık uyarısı korunur')

 before=record(page);page.evaluate("navTo('analytics')");page.get_by_role('button',name='Demo verilerini sıfırla').click()
 assert record(page)['attempts']==[]
 assert record(page)['topics']['temel']['completed'] is True
 assert page.locator('#aCount').inner_text()=='0'
 passed.append('Soru verilerini sıfırlama yeni/eski cevapları temizler, konu tamamlama ve tema korunur')

 for method in ['getItem','setItem']:
  blocked=browser.new_context(viewport={'width':390,'height':844})
  blocked.add_init_script("Object.defineProperty(Storage.prototype,'"+method+"',{value(){throw new DOMException('blocked','SecurityError')}})")
  other=blocked.new_page();other.on('pageerror',lambda e:errors.append(str(e)));other.goto(BASE)
  other.locator('#exam-kpss').click();other.locator('#level-lisans').click();topic(other);tab(other,'test')
  other.locator('[data-math-action="start"][data-count="10"]').click();other.locator('#mathAnswers button').first.click()
  assert other.locator('#mathAnswers button:disabled').count()==5
  if method=='setItem':assert other.locator('#mathTopicNotice').is_visible()
  blocked.close()
 corrupt=browser.new_context();corrupt.add_init_script("localStorage.setItem('"+KEY+"','broken')")
 bad=corrupt.new_page();bad.on('pageerror',lambda e:errors.append(str(e)));bad.goto(BASE);bad.locator('#exam-kpss').click();bad.locator('#level-lisans').click();math_home(bad)
 assert bad.locator('#mathSaveNotice').is_visible();assert bad.evaluate('(key)=>localStorage.getItem(key)',KEY)=='broken'
 corrupt.close();passed.append('Engelli okuma/yazma ve bozuk Matematik kaydında çökme yok; kayıt sorunları görünür')

 assert not errors,errors
 context.close();browser.close()
print(json.dumps({'passed':passed,'page_errors':errors},ensure_ascii=False,indent=2))
