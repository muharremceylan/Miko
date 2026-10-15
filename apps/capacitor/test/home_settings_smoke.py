import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get('AKADEMI_TEST_URL', 'http://127.0.0.1:4173')
passed = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 390, 'height': 844})
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(BASE)
    assert page.locator('#examStatusTitle').inner_text() == 'Önce sınavını seç'
    assert page.locator('#examTag').inner_text() == 'Sınavını seç'
    assert not page.locator('[data-study-content]').is_visible()
    assert page.locator('.nav [data-tab="quiz"]').is_disabled()
    assert page.locator('html').get_attribute('data-theme') == 'light'
    assert page.locator('.app').evaluate('(e)=>getComputedStyle(e).backgroundColor') == 'rgb(255, 255, 255)'
    passed.append('İlk açılış: sınav seçimi zorunlu, gündüz görünümü beyaz')

    page.get_by_role('button', name='Gece moduna geç').click()
    assert page.locator('html').get_attribute('data-theme') == 'dark'
    assert page.locator('.app').evaluate('(e)=>getComputedStyle(e).backgroundColor') == 'rgb(11, 13, 18)'
    assert page.locator('#themeToggle').get_attribute('aria-pressed') == 'true'
    page.locator('#exam-kpss').click();page.locator('#level-lisans').click()
    assert page.locator('#exam-kpss').get_attribute('aria-pressed') == 'true'
    assert page.locator('#examTag').inner_text() == 'KPSS Lisans'
    assert page.locator('[data-study-content]').is_visible()
    assert page.locator('.subject').count() == 6
    page.reload()
    assert page.locator('#examTag').inner_text() == 'KPSS Lisans'
    assert page.locator('html').get_attribute('data-theme') == 'dark'
    assert page.locator('#preferencesNotice').is_hidden()
    passed.append('KPSS ve gece modu seçimi yenileme sonrası korunuyor')

    page.locator('.nav [data-tab="quiz"]').click()
    question = page.locator('#question').inner_text()
    correct = page.evaluate('questions[qOrder[qIndex]].c')
    page.locator('#options button').nth(correct).click()
    count = page.evaluate('stats.solved')
    page.get_by_role('button', name='Gündüz moduna geç').click()
    assert page.locator('#question').inner_text() == question
    assert page.locator('#explanation').is_visible()
    assert page.locator('#options button:disabled').count() == 4
    assert page.evaluate('stats.solved') == count == 1
    passed.append('Soru cevabı ve test oturumu tema değişiminde korunuyor')

    page.locator('.nav [data-tab="home"]').click()
    page.locator('#exam-ags').click()
    assert page.locator('#examTag').inner_text() == 'AGS'
    assert page.locator('#examStatusTitle').inner_text() == 'AGS hazırlık aşamasında'
    assert not page.locator('[data-study-content]').is_visible()
    assert page.locator('#returnToKpss').is_visible()
    assert page.locator('.subject').count() == 0
    assert page.locator('#audioSelect option').count() == 0
    assert page.locator('.nav [data-tab="quiz"]').is_disabled()
    legacy = page.evaluate("localStorage.getItem('akademi_stats_v1')")
    page.evaluate("navTo('quiz');chooseAnswer(0);openLesson('tarih');startTopicQuiz()")
    assert page.locator('#home').is_visible()
    assert page.evaluate("localStorage.getItem('akademi_stats_v1')") == legacy
    page.reload()
    assert page.locator('#examTag').inner_text() == 'AGS'
    assert not page.locator('[data-study-content]').is_visible()
    page.locator('#returnToKpss').click()
    assert page.locator('#qCount').inner_text() == '1'
    page.locator('.nav [data-tab="analytics"]').click()
    assert page.locator('#aCount').inner_text() == '1'
    passed.append('AGS seçiliyor; KPSS ders/veri/cevapları AGS alanına taşınmıyor; dönüşte ilerleme korunuyor')

    # Check every existing screen under both themes, including inline-styled selects.
    for theme in ['light', 'dark']:
        if page.locator('html').get_attribute('data-theme') != theme:
            page.locator('#themeToggle').click()
        for tab in ['home', 'lessons', 'quiz', 'audio', 'camera', 'analytics']:
            page.evaluate('(tab)=>navTo(tab)', tab)
            assert page.locator('html').evaluate('(e)=>getComputedStyle(e).colorScheme') == theme
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            if theme == 'dark':
                for selector in [f'#{tab} .card', f'#{tab} select']:
                    for node in page.locator(selector).all():
                        assert node.evaluate('(e)=>getComputedStyle(e).backgroundColor') != 'rgb(255, 255, 255)', selector
    page.evaluate("navTo('lessons');openLesson('tarih')")
    assert page.locator('#lessonBody').is_visible()
    assert page.locator('#lessonBody').evaluate('(e)=>getComputedStyle(e).color') == 'rgb(241, 244, 252)'
    passed.append('Gündüz/gece: altı ekran, konu detayı ve seçim kutuları tema uyumlu')

    page.on('dialog', lambda dialog: dialog.accept())
    page.evaluate("navTo('analytics')")
    page.get_by_role('button', name='Demo verilerini sıfırla').click()
    page.reload()
    assert page.locator('#examTag').inner_text() == 'KPSS Lisans'
    assert page.locator('html').get_attribute('data-theme') == 'dark'
    assert page.evaluate('stats.solved') == 0
    passed.append('İlerlemeyi sıfırlamak sınav ve tema tercihini silmiyor')

    for value in ['broken', 'null', '[]', json.dumps({'version': 1, 'exam': '__proto__', 'theme': 'dark'}),
                  json.dumps({'version': 1, 'exam': 'kpss', 'theme': 'invalid'})]:
        page.evaluate('(value)=>localStorage.setItem("akademi_preferences_v1",value)', value)
        page.reload()
        assert page.locator('#examStatusTitle').inner_text() == 'Önce sınavını seç'
        assert page.locator('html').get_attribute('data-theme') == 'light'
        assert page.locator('#preferencesNotice').is_visible()
    page.locator('#exam-kpss').click();page.locator('#level-lisans').click()
    assert page.locator('#preferencesNotice').is_hidden()
    saved = page.evaluate("localStorage.getItem('akademi_preferences_v1')")
    page.evaluate("selectExam('__proto__');selectExam('unknown')")
    assert page.evaluate("localStorage.getItem('akademi_preferences_v1')") == saved
    passed.append('Bozuk/uyumsuz tercihler güvenli varsayılana dönüyor, geçersiz sınavlar reddediliyor')

    for method in ['getItem', 'setItem']:
        blocked = browser.new_context(viewport={'width': 390, 'height': 844})
        blocked.add_init_script("Object.defineProperty(Storage.prototype,'" + method + "',{value(){throw new DOMException('blocked','SecurityError')}})")
        other = blocked.new_page()
        other.on('pageerror', lambda error: errors.append(str(error)))
        other.goto(BASE)
        if method == 'getItem':
            assert other.locator('#preferencesNotice').is_visible()
        other.locator('#exam-kpss').click();other.locator('#level-lisans').click()
        other.locator('#themeToggle').click()
        assert other.locator('#examTag').inner_text() == 'KPSS Lisans'
        assert other.locator('html').get_attribute('data-theme') == 'dark'
        if method == 'setItem':
            assert other.locator('#preferencesNotice').is_visible()
        other.locator('.nav [data-tab="quiz"]').click()
        other.locator('#options button').first.click()
        assert other.locator('#explanation').is_visible()
        blocked.close()
    passed.append('Depolama engelinde sınav/tema ve soru akışları oturum içinde çalışıyor')

    page.evaluate("navTo('home')")
    for width in [320, 360, 390, 412, 768]:
        page.set_viewport_size({'width': width, 'height': 844})
        for theme in ['light', 'dark']:
            if page.locator('html').get_attribute('data-theme') != theme:
                page.locator('#themeToggle').click()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, theme)
    passed.append('320–768 piksel genişliklerde iki temada ana ekran taşmıyor')

    Path('test-artifacts').mkdir(exist_ok=True)
    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('#exam-kpss').click();page.locator('#level-lisans').click()
    for theme in ['light', 'dark']:
        if page.locator('html').get_attribute('data-theme') != theme:
            page.locator('#themeToggle').click()
        page.screenshot(path=f'test-artifacts/home-{theme}.png', full_page=False)
    assert not errors, errors
    context.close()
    browser.close()
print(json.dumps({'passed': passed, 'page_errors': errors}, ensure_ascii=False, indent=2))
