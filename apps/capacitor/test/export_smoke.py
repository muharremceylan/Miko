from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit, parse_qs
import hashlib
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1] / 'web-release'
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(root)))
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f'http://127.0.0.1:{server.server_port}'
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1280, 'height': 1024})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(base + '/index.html')
        frame = page.frame_locator('#appFrame')
        assert frame.locator('#exam-kpss').is_visible()
        assert 'v=' in page.locator('#appFrame').get_attribute('src')
        frame.locator('#exam-kpss').click()
        frame.locator('#themeToggle').click()
        assert frame.locator('html').get_attribute('data-theme') == 'dark'
        for element, attr, filename in [
            ('script[src^="app.js"]', 'src', 'app.js'),
            ('script[src^="native.js"]', 'src', 'native.js'),
            ('link[href^="mobile.css"]', 'href', 'mobile.css')]:
            url = frame.locator(element).get_attribute(attr)
            assert parse_qs(urlsplit(url).query)['v'][0] == hashlib.sha256((root / filename).read_bytes()).hexdigest()[:12]
        page.reload()
        assert page.frame_locator('#appFrame').locator('#examTag').inner_text() == 'KPSS'
        assert page.frame_locator('#appFrame').locator('html').get_attribute('data-theme') == 'dark'
        page.goto(base + '/standalone.html')
        assert page.locator('script[src]').count() == 0
        assert page.locator('#examTag').inner_text() == 'KPSS'
        assert page.locator('html').get_attribute('data-theme') == 'dark'
        page.locator('.nav [data-tab="quiz"]').click()
        page.locator('#options button').first.click()
        assert page.locator('#explanation').is_visible()
        assert not errors, errors
        browser.close()
finally:
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)
print('Yayın paketi: telefon önizlemesi, tema/seçim kalıcılığı, içerik hashleri ve tek HTML soru akışı geçti.')
