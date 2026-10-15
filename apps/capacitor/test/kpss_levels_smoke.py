"""KPSS düzeylerinin ayrımı ve kullanıcı tarafından sağlanan müfredat verileri."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get('AKADEMI_TEST_URL', 'http://127.0.0.1:4173')
passed = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 390, 'height': 844})
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(BASE)
    page.locator('#exam-kpss').click()
    assert page.locator('#kpssLevelChoices button').count() == 3
    assert page.locator('#examStatusTitle').inner_text() == 'KPSS düzeyini seç'
    assert page.locator('.nav [data-tab="lessons"]').is_disabled()
    page.locator('#level-lisans').click()
    assert page.locator('#examTag').inner_text() == 'KPSS Lisans'
    page.locator('.nav [data-tab="quiz"]').click()
    page.locator('#options button').first.click()
    lisans_record = page.evaluate("localStorage.getItem('akademi_stats_v1')")
    for level, name in [('onlisans', 'Ön Lisans'), ('ortaogretim', 'Ortaöğretim')]:
        page.evaluate("navTo('home')")
        page.locator('#level-' + level).click()
        assert page.locator('#examTag').inner_text() == 'KPSS ' + name
        assert page.locator('#qCount').inner_text() == '0'
        assert page.evaluate('stats.solved') == 0
        assert 'ortak demo' in page.locator('#examStatusDescription').inner_text()
        page.evaluate("navTo('quiz')")
        page.locator('#options button').first.click()
        assert page.evaluate("localStorage.getItem('akademi_stats_v1')") == lisans_record
    page.reload()
    assert page.locator('#examTag').inner_text() == 'KPSS Ortaöğretim'
    assert page.locator('#qCount').inner_text() == '1'
    page.locator('#level-lisans').click()
    assert page.locator('#qCount').inner_text() == '1'
    passed.append('Üç KPSS düzeyi; zorunlu seçim, ayrı sayaçlar, yenileme ve dönüşte kalıcılık')

    page.evaluate("navTo('lessons')")
    assert page.locator('.subject b').all_text_contents() == ['Tarih', 'Matematik', 'Geometri', 'Vatandaşlık', 'Coğrafya', 'Güncel Bilgiler']
    for subject, name in [('geometri', 'Geometri'), ('guncel', 'Güncel Bilgiler')]:
        page.evaluate('(topic)=>openLesson(topic)', subject)
        assert page.locator('#overviewTitle').inner_text() == name
        assert 'İçerik hazırlanıyor' in page.locator('#overviewBody').inner_text()
        assert page.locator('#lessonDetail').is_hidden()
        assert page.locator('#overviewBody button').count() == 0
        assert page.locator(f'#audioSelect option[value="{subject}"]').count() == 0
        page.evaluate("navTo('quiz')")
        page.locator('#quizTopic').select_option(subject)
        assert page.locator('#resultTitle').inner_text() == 'Henüz soru yok'
        assert page.evaluate('stats.solved') == 1
    passed.append('Altı ders; yeni derslerin hazırlık/boş soru durumu ve ses filtresi')

    page.evaluate("openLesson('matematik')")
    topics = page.locator('[data-math-topic]')
    assert topics.count() == 17
    assert topics.nth(0).locator('summary').inner_text() == '1. Temel Kavramlar'
    assert topics.nth(16).locator('summary').inner_text() == '17. Sayısal Mantık'
    assert page.locator('[data-math-topic="sayilar"] li').all_text_contents() == ['Sayı Kümeleri', 'Doğal Sayılar', 'Tam Sayılar', 'Faktöriyel', 'Sayma Sistemleri', 'Bölme', 'Bölünebilme Kuralları']
    assert page.locator('[data-math-topic="problemler"] li').count() == 9
    page.locator('#mathExample').click()
    assert 'Birinci Dereceden Denklemler' in page.locator('#lessonName').inner_text()
    page.locator('#shortTab').click()
    assert page.locator('#lessonBody li').count() == 4
    page.get_by_role('button', name='Bu konudan soru çöz →').click()
    assert page.evaluate('qOrder.length') == 3
    page.evaluate("openLesson('matematik',true)")
    page.locator('#lessonBack').click()
    assert page.locator('#mathTopicsPanel').is_visible()
    passed.append('17 ana konu ve alt başlıklar; örnek denklem anlatımı, özeti ve üç soru akışı')

    page.locator('#mathDistributionTab').click()
    assert page.locator('#mathDistributionTotal').inner_text() == '26'
    assert page.locator('#mathDistributionPanel tbody tr').count() == 16
    assert 'Bağıntı ve Fonksiyon' in page.locator('#mathDistributionPanel').inner_text()
    assert 'kesin soru sayısı değildir' in page.locator('#mathDistributionPanel').inner_text()
    assert page.locator('#mathDistributionPanel').get_by_text('Sayısal Mantık', exact=True).locator('..').locator('td').inner_text() == '6'
    passed.append('Genel dağılım: 16 satır, toplam 26, kaynak/kapsam farkı ve resmî veri ayrımı')

    page.locator('#mathAnnualTab').click()
    assert page.locator('#mathYear option').all_text_contents() == [str(y) for y in range(2015, 2025)]
    expected_sums = [36, 26, 26, 26, 26, 26, 25, 27, 27, 28]
    source_sums = [27, 27, 27, 26, 26, 26, 26, 27, 28, 26]
    for i, year in enumerate(range(2015, 2025)):
        page.locator('#mathYear').select_option(str(year))
        assert page.locator('#mathAnnualYearTable tbody tr').count() == 16
        assert page.locator('#annualComputedTotal').inner_text() == str(expected_sums[i])
        assert page.locator('#annualSourceTotal').inner_text() == str(source_sums[i])
        assert ('tutarsızlık' in page.locator('#annualTotalNotice').inner_text()) == (expected_sums[i] != source_sums[i])
    rows = page.locator('#mathAnnualYearTable tbody tr')
    assert rows.nth(1).locator('td').inner_text() == '5'
    assert rows.nth(4).locator('td').inner_text() == '–'
    assert rows.nth(9).locator('td').inner_text() == '8'
    assert rows.nth(15).locator('td').inner_text() == '4'
    passed.append('2015–2024 görsel verileri; yıl seçimi, çizgiler, toplam farkları ve 2024 değerleri')

    page.locator('#mathAnnualPanel details summary').click()
    for width in [320, 360, 390, 412, 768]:
        page.set_viewport_size({'width': width, 'height': 844})
        for theme in ['light', 'dark']:
            if page.locator('html').get_attribute('data-theme') != theme:
                page.locator('#themeToggle').click()
            for tab in ['mathTopicsTab', 'mathDistributionTab', 'mathAnnualTab']:
                page.locator('#' + tab).click()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, theme, tab)
    passed.append('Konu/genel/yıllık ekranları ve tam tablo: iki tema, 320–768 pikselde taşma yok')

    page.evaluate("localStorage.setItem('akademi_preferences_v1',JSON.stringify({version:1,exam:'kpss',theme:'dark'}))")
    page.reload()
    assert page.locator('#examStatusTitle').inner_text() == 'KPSS düzeyini seç'
    assert page.locator('html').get_attribute('data-theme') == 'dark'
    assert page.evaluate("localStorage.getItem('akademi_stats_v1')") == lisans_record
    page.locator('#level-lisans').click()
    for bad in ['__proto__', 'unknown', {}, 3]:
        record = page.evaluate("localStorage.getItem('akademi_preferences_v1')")
        page.evaluate('(bad)=>selectKpssLevel(bad)', bad)
        assert page.evaluate("localStorage.getItem('akademi_preferences_v1')") == record
    page.evaluate("localStorage.setItem('akademi_preferences_v1',JSON.stringify({version:1,exam:'kpss',theme:'dark',kpssLevel:'__proto__'}))")
    page.reload()
    assert page.locator('#preferencesNotice').is_visible()
    assert page.locator('#examStatusTitle').inner_text() == 'Önce sınavını seç'
    passed.append('Eski tercih biçiminde tema/veri korunur; geçersiz düzey ve bozuk tercih güvenli yönetilir')
    assert not errors, errors
    context.close()
    browser.close()
print(json.dumps({'passed': passed, 'page_errors': errors}, ensure_ascii=False, indent=2))
