# Web üzerinde mobil görünümle geliştirme

## Canlı yayın — doğrulandı

Mobil web önizlemesi: **https://muharremceylan.github.io/Miko/**

15 Ekim 2026 tarihinde `0eb2039` commit'inin [38692055701 numaralı GitHub Actions yayını](https://github.com/muharremceylan/Miko/actions/runs/38692055701) başarıyla tamamlandı. Yayın sonrasında GitHub çalıştırıcısından ana önizleme, `app.html` ve `preview.js` için HTTP 200 ve beklenen içerik kontrolü geçti. Önizleme 360×800, 390×844 ve 412×915 ölçülerini sunar. Önizleme içindeki uygulama akışları önceki yerel Chromium testlerinde doğrulanmıştır; canlı siteye bu bulut makinesinden doğrudan erişim hâlâ ağ kısıtına takıldığı için uzaktan tarayıcı testi yapılmış sayılmaz.

GitHub Pages seçimi artık tamamdır; kullanıcıdan tekrar ayar veya parola istenmez. Aşağıdaki ilk deneme/ağ notları durum geçmişidir.


Bu aşamada hedef tarayıcıda çalışan web sürümünü telefon ekranında görerek geliştirmektir. Android ve iOS paketleri sonraki aşamadır; günlük arayüz çalışması için APK veya Flutter gerekmez. Uygulamanın ortak kaynağı `akademi_ai_prototip/index.html`, mobil bağlantıları `apps/capacitor/src` altındadır.

## İlk Matematik çalışma paketi

**KPSS → Lisans → Dersler → Matematik → Temel Kavramlar → Test Çöz** yolunda 10/20/30 soru veya rastgele tek soru seçilebilir. Yanlış/çözülmemiş filtreleri, sonuç analizi ve yarım teste dönüş çalışır. Konu içinde anlatım, üç özet, sekiz formül kartı, üç çözümlü örnek ve ses metni vardır. Ders ilerlemesi başarı oranından ayrıdır; 34 son düzey konudan yalnız ilk tam paket açılmıştır. Uzman incelemesi beklenir; gerçek ses/AI sekmeleri hazırlık durumudur. Yeni sekmeler ve paket, tek HTML sürümünde de çalışır. Android/iOS henüz bu güncellemeyle yeniden paketlenmedi.

## Son eklenenler — KPSS düzeyleri ve matematik

Ana sayfada **KPSS → Lisans / Ön Lisans / Ortaöğretim** seçilir. Düzeylerin ilerlemesi ayrıdır. Dersler alanında Geometri ve Güncel Bilgiler hazırlık ekranları eklendi. **KPSS Lisans → Dersler → Matematik** içinde konu listesi (17 ana başlık), genel dağılım ve yıllara göre (2015–2024) görünüm vardır. Yıllık tabloda yıl seçimi veya tüm yılları yatay kaydırarak inceleme kullanılabilir; toplam uyuşmazlıkları açık gösterilir. Denklemler örneği ve üç demo soru korunur. Diğer anlatımlar henüz hazırlanmadı; kaynak/güncellik notları uygulamada ve `akademi_ai_prototip/CONTENT_SOURCES.md` içinde yer alır.

Yerel tarayıcı doğrulaması: `python test/kpss_levels_smoke.py` yedi grup; `python test/home_settings_smoke.py` dokuz grup; `AKADEMI_TEST_URL` çalışan yerel sunucuya ayarlanarak `python test/web_smoke.py` 11 grup; ayrıca preview/export testleri. `npm test` 12 native mock testini çalıştırır. Bunlar fiziksel Android/iOS cihaz testleri değildir.

## Hazır olanlar

- 360×800, 390×844 ve 412×915 telefon boyutları; ekrana sığdırma veya 1:1 gösterim.
- Önizleme içindeki gerçek uygulamada ders, özet, soru, test sonucu ve analiz akışları.
- Ekran boyutu değiştirildiğinde içerik veya ilerleme yeniden yüklenmez.
- “Uygulamayı aç” düğmesi çerçevesiz sürümü ayrı sekmede açar.
- Web yayını statik HTML/CSS/JavaScript'tir; bu sürüm için backend sunucusu veya sağlayıcı anahtarı gerekmez.

Yerel geliştirme için `apps/capacitor` içinde `npm start` çalışır. Bu bulut ortamında sunucu 4173 portunda başlatıldı. `/preview.html` telefon çerçevesini, `/index.html` uygulamayı sunar. Bu yerel adres dışarıdan erişilebilir yayın bağlantısı değildir. Kaynak değişikliğinde `npm run build` ile web dosyaları yenilenir; tarayıcı sayfasını yenileyerek değişiklik görülür. Otomatik hot reload henüz yoktur.

`npm run export:web` komutu `web-release/` klasörünü oluşturur. Yayımlanacak klasörde `index.html` mobil önizlemedir; uygulama `app.html` olarak tutulur. Bu ayrım iframe'in kendisini tekrar yüklemesini engeller. `standalone.html`, ayrı dosya gerektirmeyen uygulama sürümüdür; sunucu üzerinden kontrol edildi. Bulut tarayıcısının file:// kuralı yerel dosya açılışını engelledi; bu yöntem burada doğrulanamadı. ZIP'in içeriği bir statik sunucuya olduğu gibi yüklenebilir.

## GitHub Pages için hazırlık

Hedef hesap/depo kullanıcı bilgisinden `muharremceylan/Miko` olarak belirlendi. Kendi alan adınız gerekmez. GitHub Pages etkinleştirilirse beklenen proje adresi `https://muharremceylan.github.io/Miko/` olur. **Bu adres artık yayındadır; doğrulama sonucu yukarıdadır.**

`.github/workflows/web-preview.yml` hazırlandı. Ana dala yüklenip Pages kaynağı **GitHub Actions** olarak seçilirse iş akışı kilitli npm bağımlılıklarını kurar, köprü testlerini çalıştırır, mobil web önizlemesini üretir ve Pages'e dağıtır. Android/iOS/Flutter derlemez. Eylemler resmî depolardan doğrulanan commit'lere sabitlenmiştir. İlk kaynak commit'i `25c22e1334fe4da322fdcd219e7ef54d7b11ffb7` ile `main` dalına gönderildi. GitHub iş akışı çalıştı; `38690903289` numaralı deneme Pages yapılandırmasını bulamadı (`Get Pages site failed / Not Found`). Bu ilk başarısız denemeden sonra kullanıcı Pages ayarını yaptı; yeni yayın başarıyla tamamlandı.

Mevcut makinede HTTPS Git okuması başarılı, fakat GitHub ayar API'si `api.github.com` ağ politikasından 403 alıyor. HTTPS Git push başarıyla çalıştı ve GitHub web sayfasından deponun Public olduğu doğrulandı. Pages ayar API'si ise bu makineden erişilemiyor. `api.github.com` ve yayın sonucunu kontrol etmek için `muharremceylan.github.io` ağ izinleri ortam taslağına eklendi; ayarlarda kaydetme/uygulama bekleniyor. Yalnızca taslağa kaydetmek erişimi açmaz. Kullanıcıdan GitHub şifresi veya ham token istenmez.

Ağ ayarı uygulandıktan sonra mevcut kimlik doğrulamayla depo/Pages yetkileri tekrar kontrol edilmelidir. Depo gizliyse herkese açık hale getirilmez; Pages plan uygunluğu veya alternatif yayın kullanıcıyla değerlendirilir. Remote `main` üzerinde mevcut iş varsa korunur; üzerine zorla yazılmaz. Kaynakları yükleme, Pages etkinleştirme, gerçek HTTPS isteği ve tarayıcı kontrolü başarılı olmadan “yayında” denmez.

## Kontroller

- Node web sunucusu çalıştırıldı; yalnız izinli web dosyalarını sunuyor. Bilinmeyen dosya/yol 404, yazma isteği 405, HEAD isteği 200.
- `python test/preview_smoke.py`: iframe içi ders/özet/test, ekran boyutu değişimi, 1:1/sığdırma, dar ekranlarda taşma ve sunucu erişim kontrolleri geçti.
- `AKADEMI_TEST_URL` yeni sunucuyu gösterecek şekilde 11 mevcut web regresyon grubu geçti; JavaScript hatası görülmedi.
- Export edilen tek HTML ve mobil önizlemenin ders/soru akışı HTTP üzerinden doğrulandı; bulut tarayıcısında yerel file:// açılışı yönetici politikasıyla engellendi.
- Kamera ve ses tarayıcı/cihaz desteğine bağlı. Gerçek AI hâlâ bağlı değil. Android test APK'sı önceki aşamada üretildi; bu web önizleme değişiklikleri için mobil paket yeniden derlenmedi. iOS derlemesi yapılmadı.

## İlk kurulumda kullanılan GitHub ayarı — tamamlandı

`https://github.com/muharremceylan/Miko/settings/pages` içinde **Build and deployment → Source → GitHub Actions** seçildi. Ardından `https://github.com/muharremceylan/Miko/actions/runs/38690903289` üzerinden **Re-run all jobs** ile yeniden denenebilir. Kullanıcı bu ayarı tamamladı. Sonraki 38692055701 numaralı iş akışı yayını ve canlı HTTP kontrolünü başarıyla tamamladı. Bu eski denemeyi tekrar çalıştırmak gerekmez.
