from playwright.sync_api import sync_playwright
import json, base64, os
from pathlib import Path
URL=os.environ.get('AKADEMI_TEST_URL','http://127.0.0.1:8001')
passed=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 context=b.new_context(viewport={'width':390,'height':844},timezone_id='Europe/Istanbul')
 page=context.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.clock.install(time=__import__('datetime').datetime.fromisoformat('2026-10-14T12:00:00+03:00'))
 page.goto(URL);page.locator('#exam-kpss').click();assert page.locator('.subject').count()==4
 for topic in ['tarih','matematik','vatandaslik','cografya']:
  page.evaluate(f"openLesson('{topic}')");page.locator('#shortTab').click();assert page.locator('#lessonBody li').count()
  page.evaluate('startTopicQuiz()');assert page.locator('#quizTopic').input_value()==topic
 passed.append('4 ders, özet ve filtre akışı')
 page.locator('#quizTopic').select_option('all')
 assert page.evaluate('new Set(qOrder).size')==10
 page.evaluate('nextQuestion()');assert page.evaluate('qIndex')==0
 for i in range(10):
  c=page.evaluate('questions[qOrder[qIndex]].c');page.locator('#options button').nth(c if i%2==0 else (c+1)%4).click()
  page.evaluate('chooseAnswer(0)');assert page.evaluate('stats.solved')==i+1
  assert page.locator('#options button:disabled').count()==4
  page.locator('#nextBtn').click()
 assert page.locator('#quizResult').is_visible()
 assert '5 doğru, 5 yanlış' in page.locator('#resultSummary').inner_text()
 assert page.locator('#homeProgress').evaluate('(e)=>e.style.width')=='100%'
 assert page.locator('#successTag').inner_text()=='Hedef tamamlandı ✓'
 page.evaluate('nextQuestion();chooseAnswer(0)');assert page.evaluate('stats.solved')==10
 passed.append('10 benzersiz soru, çift cevabı engelleme, %100 hedef, 5/5 sonuç, oturum bitişi')
 page.get_by_role('button',name='Yeni test başlat').click();assert page.locator('#quizCard').is_visible()
 page.locator('#options button').nth(0).click();assert page.locator('#homeProgress').evaluate('(e)=>e.style.width')=='100%'
 page.reload();assert page.evaluate('stats.solved')==11;assert page.locator('#qCount').inner_text()=='11'
 passed.append('Yeni oturum, 11 soruda dolu hedef, kayıt kalıcılığı')
 page.clock.set_system_time(__import__('datetime').datetime.fromisoformat('2026-10-15T12:00:00+03:00'))
 page.evaluate('drawHome()');assert page.locator('#qCount').inner_text()=='0'
 page.evaluate("navTo('analytics')");assert page.locator('#aCount').inner_text()=='11'
 page.evaluate("navTo('quiz')");page.locator('#options button').nth(0).click();assert page.evaluate('stats.daily.solved')==1;assert page.evaluate('stats.solved')==12
 page.reload();assert page.locator('#qCount').inner_text()=='1'
 passed.append('İstanbul saat diliminde gün değişimi; toplamları koruma ve yeni gün kaydı')
 legacy={'solved':2,'correct':1,'topics':{'tarih':{'solved':2,'correct':1}}}
 page.evaluate('(s)=>localStorage.setItem("akademi_stats_v1",JSON.stringify(s))',legacy);page.reload()
 assert page.evaluate('stats.solved')==2;assert page.evaluate('stats.daily.solved')==0
 assert page.locator('#storageNotice').is_visible()
 passed.append('Önceki kayıt biçiminden toplamları kaybetmeden geçiş')
 for bad in ['broken',json.dumps({'solved':-1,'correct':5,'topics':{}}),json.dumps({'solved':1,'correct':0,'topics':{'unknown':{'solved':1,'correct':0}}}), 'null']:
  page.evaluate('(v)=>localStorage.setItem("akademi_stats_v1",v)',bad);page.reload()
  assert page.locator('.subject').count()==4;assert page.evaluate('stats.solved')==0
  assert page.evaluate('localStorage.getItem("akademi_stats_v1")')==bad
 passed.append('Bozuk JSON/şema/konu/null: çökmeden açılma, başlangıçta eski kaydı koruma')
 page.evaluate("navTo('quiz')");page.locator('#options button').nth(0).click();page.reload();assert page.evaluate('stats.solved')==1
 passed.append('Bozuk kayıttan yeni cevapla sağlıklı kayda dönüş')
 page.evaluate("navTo('camera')")
 png=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/a9sAAAAASUVORK5CYII=')
 page.locator('#fileInput').set_input_files({'name':'sample.png','mimeType':'image/png','buffer':png})
 page.wait_for_function('document.querySelector("#preview").naturalWidth>0');assert page.locator('#preview').is_visible()
 page.get_by_role('button',name='Çözüm akışını göster →').click();assert page.locator('#photoSolution').is_visible()
 page.locator('#fileInput').set_input_files({'name':'bad.txt','mimeType':'text/plain','buffer':b'bad'})
 assert 'Lütfen' in page.locator('#photoStatus').inner_text()
 page.locator('#fileInput').set_input_files({'name':'large.png','mimeType':'image/png','buffer':b'0'*(10*1024*1024+1)})
 assert 'Lütfen' in page.locator('#photoStatus').inner_text()
 page.locator('#fileInput').set_input_files({'name':'broken.png','mimeType':'image/png','buffer':b'broken'})
 page.wait_for_function('document.querySelector("#photoStatus").textContent.includes("açılamadı")')
 passed.append('PNG önizleme/demo; yanlış tür, 10 MB üstü ve bozuk görsel hata yönetimi')
 page.evaluate("navTo('audio')");page.get_by_role('button',name='▶ Dinle').click();page.get_by_role('button',name='■ Durdur').click();page.wait_for_timeout(300)
 assert page.locator('#speechStatus').inner_text()=='Seslendirme durduruldu.'
 page.evaluate("navTo('home')");assert page.locator('#speechStatus').inner_text()=='Seslendirme durduruldu.'
 passed.append('Ses durdurma ve sekme değişimi; geç gelen olay durumu bozmuyor')
 page.on('dialog',lambda d:d.accept());page.evaluate("navTo('analytics')");page.get_by_role('button',name='Demo verilerini sıfırla').click();assert page.evaluate('stats.solved')==0
 for width in [320,390,768]:
  page.set_viewport_size({'width':width,'height':844})
  for tab in ['home','lessons','quiz','audio','camera','analytics']:
   page.evaluate(f"navTo('{tab}')");assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,tab)
 passed.append('Sıfırlama ve 320/390/768 genişliklerde tüm ana ekranlarda taşma kontrolü')
 for mode in ['read','write']:
  c=b.new_context();c.add_init_script("Object.defineProperty(Storage.prototype,'"+('getItem' if mode=='read' else 'setItem')+"',{value(){throw new DOMException('blocked','SecurityError')}})")
  pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(URL);pg.locator('#exam-kpss').click();pg.evaluate("navTo('quiz')");pg.locator('#options button').nth(0).click();assert pg.evaluate('stats.solved')==1;assert pg.locator('#storageNotice').is_visible();c.close()
 passed.append('Depolama okuma/yazma engelinde kullanılabilir oturum ve uyarı')
 assert not errors,errors
 page.evaluate("navTo('home')");page.set_viewport_size({'width':390,'height':844});Path('test-artifacts').mkdir(exist_ok=True); page.screenshot(path='test-artifacts/home-fixed.png',full_page=True)
 context.close();b.close()
print(json.dumps({'passed':passed,'page_errors':errors,'sound':'Türkçe işitilebilir çıktı cihaz testi gerektiriyor'},ensure_ascii=False,indent=2))
