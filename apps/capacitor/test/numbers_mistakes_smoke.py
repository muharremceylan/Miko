"""Sayılar ve yanlış defterinde gerçek mobil web, kalıcılık ve konuya dönüş."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('AKADEMI_TEST_URL','http://127.0.0.1:4173')
KEY='akademi_math_v1_kpss_lisans'
PACKAGE=json.loads((Path(__file__).resolve().parents[3]/'akademi_ai_prototip/content/kpss/lisans/matematik/topics/sayilar.json').read_text())
passed=[]
def topic(page,tid,tab='lesson'):page.evaluate('([id,tab])=>AcademiMath.openTopic(id,tab)',[tid,tab])
def state(page):return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
def active(page):
 s=state(page)
 return next(a for a in s['attempts'] if a['id']==s['activeAttempt'])
def answer(page,correct):
 a=active(page);q=a['questions'][a['current']]
 page.locator('#mathAnswers button').nth(q['answer'] if correct else (q['answer']+1)%5).click()
 page.locator('[data-math-action="next"]').click()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 page.goto(BASE);page.locator('#exam-kpss').click();page.locator('#level-lisans').click();page.evaluate('AcademiMath.open()')
 page.locator('[data-math-action="mistakes"]').click();assert 'Henüz tekrar bekleyen yanlış yok' in page.locator('#mathMistakeCount').inner_text()
 topic(page,'temel');page.locator('[data-math-action="complete"]').click()
 for tid,lesson in PACKAGE['lessons'].items():
  topic(page,tid);assert page.locator('#mathTopicTitle').inner_text()==lesson['title']
  assert page.locator('.notebook-page').count()==4
  assert page.locator('.memory-key').first.inner_text()==lesson['memoryNotes'][0]['key']
  page.locator('[data-style="plain"]').click();assert lesson['sections'][0]['paragraphs'][0] in page.locator('#mathTopicPanel').inner_text()
  page.locator('[data-style="notebook"]').click();page.locator('#math-tab-summary').click()
  for level in ['quick','standard','detailed']:
   page.locator('#mathSummaryLevel').select_option(level);assert lesson['summaries'][level]['title'] in page.locator('#mathTopicPanel').inner_text()
  page.locator('#math-tab-formulas').click();assert page.locator('.math-formula').count()==len(lesson['formulas'])
  page.locator('#math-tab-examples').click();assert page.locator('.math-example').count()==2
  page.locator('#math-tab-audio').click();assert lesson['title']+' — seslendirme metni' in page.locator('#mathTopicPanel').inner_text()
  assert ' '.join(PACKAGE['audio'][tid]['summaries']['detailed'].split()) in ' '.join(page.locator('#mathTopicPanel').inner_text().split())
  page.locator('#math-tab-test').click();assert '10 uygun soru' in page.locator('#mathPoolCount').inner_text()
  assert page.locator('[data-count="20"]').is_disabled() and page.locator('[data-count="30"]').is_disabled()
  page.locator('#math-tab-lesson').click();page.locator('[data-math-action="complete"]').click()
 page.reload();page.evaluate('AcademiMath.open()');assert page.locator('#mathCompleted').inner_text()=='8'
 assert page.locator('#mathRemaining').inner_text()=='26';assert page.locator('#mathProgressPercent').inner_text()=='%24'
 assert 'Tamamlandı' in page.locator('[data-math-topic="sayilar"] summary').inner_text()
 passed.append('Yedi alt konu: renkli anlatım, üç özet, formüller, iki örnek, doğru ses metni ve 10 soruluk havuz; yenilemede tamamlama korunur')
 topic(page,'sayilar','test');assert '70 uygun soru' in page.locator('#mathPoolCount').inner_text()
 page.locator('[data-count="30"]').click();a=active(page)
 assert len(a['questions'])==len(set(q['id'] for q in a['questions']))==30
 assert len(set(q['topicId'] for q in a['questions']))>1
 for i in range(30):answer(page,i>=3)
 assert '27 doğru, 3 yanlış, 0 boş' in page.locator('#mathResultSummary').inner_text()
 page.locator('#mathTestResult [data-math-action="mistakes"]').click();assert page.locator('.math-mistake').count()==3
 first=page.locator('.math-mistake').first
 qid=first.locator('[data-math-action="review-one"]').get_attribute('data-question')
 tid=first.locator('[data-math-action="topic"]').get_attribute('data-topic')
 first.locator('[data-math-action="topic"]').click();assert page.locator('#mathTopicTitle').inner_text()==PACKAGE['lessons'][tid]['title']
 page.evaluate('AcademiMath.openMistakes()');page.locator('#mathMistakeTopic').select_option(tid)
 assert all(PACKAGE['lessons'][tid]['title'] in item.inner_text() for item in page.locator('.math-mistake').all())
 page.locator('#mathMistakeTopic').select_option('');page.locator(f'[data-question="{qid}"]').click()
 assert active(page)['questions'][0]['id']==qid
 page.reload();page.evaluate('AcademiMath.open()');page.locator('[data-math-action="resume-test"]').click()
 assert active(page)['questions'][0]['id']==qid
 answer(page,True);page.locator('#mathTestResult [data-math-action="mistakes"]').click()
 assert page.locator('.math-mistake').count()==2 and page.locator(f'[data-question="{qid}"]').count()==0
 assert len(state(page)['attempts'])==2
 assert page.evaluate('AcademiMath.back()') is True
 passed.append('30 soruluk karma test, yanlış defteri, konuya dönüş, filtre, tek soru tekrarı; doğru çözülünce defterden çıkar, geçmiş korunur')
 topic(page,'sayilar-bolme','test');page.locator('#mathTestMode').select_option('assessment');page.locator('[data-count="10"]').click()
 q=active(page)['questions'][0];page.locator('#mathAnswers button').nth((q['answer']+1)%5).click()
 page.evaluate('AcademiMath.openMistakes()');assert page.locator('.math-mistake').count()==2
 assert page.locator('[data-math-action="review-one"]:disabled').count()==2
 page.locator('[data-math-action="resume-test"]').click();page.locator('[data-math-action="finish"]').click()
 page.locator('#mathTestResult [data-math-action="mistakes"]').click();assert page.locator(f'[data-question="{q["id"]}"]').count()==1
 passed.append('Yarım test varken ikinci test engellenir; değerlendirme cevapları ancak bitince deftere eklenir')
 for width in [320,390,412]:
  page.set_viewport_size({'width':width,'height':844})
  for theme in ['light','dark']:
   if page.locator('html').get_attribute('data-theme')!=theme:page.locator('#themeToggle').click()
   page.evaluate('AcademiMath.openMistakes()');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   for tid in PACKAGE['lessons']:
    topic(page,tid);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('#math-tab-summary').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.set_viewport_size({'width':390,'height':844});topic(page,'sayilar-bolunebilme-kurallari')
 Path('test-artifacts').mkdir(exist_ok=True);page.screenshot(path='test-artifacts/sayilar-defter.png',full_page=True)
 page.evaluate("selectKpssLevel('onlisans');AcademiMath.openMistakes()")
 assert not page.locator('#mathMistakesTitle').is_visible()
 assert state(page)['topics']['temel']['completed'] is True
 passed.append('Yeni ekranlar 320/390/412 piksel ve iki temada taşmaz; düzey değişince Lisans defteri açılmaz')
 assert not errors,errors
 browser.close()
print(json.dumps({'passed':passed,'page_errors':errors},ensure_ascii=False,indent=2))
