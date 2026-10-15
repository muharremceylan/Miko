from pathlib import Path
import os
from playwright.sync_api import sync_playwright

base = os.environ.get('AKADEMI_TEST_URL', 'http://127.0.0.1:4173')
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1040})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    response = page.goto(base + '/preview.html')
    assert response.status == 200
    app = page.frame_locator('#appFrame')
    assert app.locator('#welcome').inner_text() == 'Merhaba! 👋'
    assert page.frames[1].evaluate('innerWidth') == 390
    app.locator('#exam-kpss').click();app.locator('#level-lisans').click()
    app.locator('.nav [data-tab="lessons"]').click()
    app.locator('.subject').first.click()
    app.locator('#shortTab').click()
    assert app.locator('#lessonBody li').count() > 0
    app.get_by_role('button', name='Bu konudan soru çöz →').click()
    correct = page.frames[1].evaluate('questions[qOrder[qIndex]].c')
    app.locator('#options button').nth(correct).click()
    assert app.locator('#explanation').is_visible()
    assert app.locator('#qCount').inner_text() == '1'
    page.locator('#device').select_option('412x915')
    assert page.frames[1].evaluate('innerWidth') == 412
    assert app.locator('#qCount').inner_text() == '1'
    page.locator('#scaleToggle').click()
    assert page.locator('#scaleToggle').get_attribute('aria-pressed') == 'true'
    page.locator('#scaleToggle').click()
    for width in [360, 390, 768, 1440]:
        page.set_viewport_size({'width': width, 'height': 1040})
        page.wait_for_timeout(50)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.set_viewport_size({'width': 1440, 'height': 1040})
    page.locator('#device').select_option('390x844')
    app.locator('.nav [data-tab="home"]').click()
    page.wait_for_timeout(100)
    Path('test-artifacts').mkdir(exist_ok=True)
    page.screenshot(path='test-artifacts/mobile-web-preview.png')
    assert not errors, errors
    # Static server must never expose repository or filesystem files.
    assert page.request.get(base + '/package.json').status == 404
    assert page.request.get(base + '/%2e%2e/package.json').status == 404
    assert page.request.post(base + '/index.html').status == 405
    assert page.request.head(base + '/index.html').status == 200
    browser.close()
print('Mobil önizleme, ekran boyutu geçişi, iframe içi ders/test ve sunucu erişim kontrolleri geçti.')
