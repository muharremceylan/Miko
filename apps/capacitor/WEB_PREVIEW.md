# Web üzerinde mobil görünümle geliştirme

Bu aşamada hedef tarayıcıda çalışan web sürümünü telefon ekranında görerek geliştirmektir. Android ve iOS paketleri sonraki aşamadır; günlük arayüz çalışması için APK veya Flutter gerekmez. Uygulamanın ortak kaynağı `akademi_ai_prototip/index.html`, mobil bağlantıları `apps/capacitor/src` altındadır.

## Hazır olanlar

- 360×800, 390×844 ve 412×915 telefon boyutları; ekrana sığdırma veya 1:1 gösterim.
- Önizleme içindeki gerçek uygulamada ders, özet, soru, test sonucu ve analiz akışları.
- Ekran boyutu değiştirildiğinde içerik veya ilerleme yeniden yüklenmez.
- “Uygulamayı aç” düğmesi çerçevesiz sürümü ayrı sekmede açar.
- Web yayını statik HTML/CSS/JavaScript'tir; bu sürüm için backend sunucusu veya sağlayıcı anahtarı gerekmez.

Yerel geliştirme için `apps/capacitor` içinde `npm start` çalışır. Bu bulut ortamında sunucu 4173 portunda başlatıldı. `/preview.html` telefon çerçevesini, `/index.html` uygulamayı sunar. Bu yerel adres dışarıdan erişilebilir yayın bağlantısı değildir. Kaynak değişikliğinde `npm run build` ile web dosyaları yenilenir; tarayıcı sayfasını yenileyerek değişiklik görülür. Otomatik hot reload henüz yoktur.

`npm run export:web` komutu `web-release/` klasörünü oluşturur. Yayımlanacak klasörde `index.html` mobil önizlemedir; uygulama `app.html` olarak tutulur. Bu ayrım iframe'in kendisini tekrar yüklemesini engeller. `standalone.html`, ayrı dosya gerektirmeyen uygulama sürümüdür; sunucu üzerinden kontrol edildi. Bulut tarayıcısının file:// kuralı yerel dosya açılışını engelledi; bu yöntem burada doğrulanamadı. ZIP'in içeriği bir statik sunucuya olduğu gibi yüklenebilir.

## GitHub Pages için hazırlık

Hedef hesap/depo kullanıcı bilgisinden `muharremceylan/Miko` olarak belirlendi. Kendi alan adınız gerekmez. GitHub Pages etkinleştirilirse beklenen proje adresi `https://muharremceylan.github.io/Miko/` olur. **Bu adres henüz doğrulanmış veya yayına alınmış değildir.**

`.github/workflows/web-preview.yml` hazırlandı. Ana dala yüklenip Pages kaynağı **GitHub Actions** olarak seçilirse iş akışı kilitli npm bağımlılıklarını kurar, köprü testlerini çalıştırır, mobil web önizlemesini üretir ve Pages'e dağıtır. Android/iOS/Flutter derlemez. Eylemler resmî depolardan doğrulanan commit'lere sabitlenmiştir. Bu GitHub iş akışı henüz GitHub üzerinde çalıştırılmadı.

Mevcut makinede HTTPS Git okuması başarılı, fakat GitHub ayar API'si `api.github.com` ağ politikasından 403 alıyor. Bu yüzden depo görünürlüğü, Pages uygunluğu ve yazma/yayın izni henüz doğrulanamadı. `api.github.com` ve yayın sonucunu kontrol etmek için `muharremceylan.github.io` ağ izinleri ortam taslağına eklendi; ayarlarda kaydetme/uygulama bekleniyor. Yalnızca taslağa kaydetmek erişimi açmaz. Kullanıcıdan GitHub şifresi veya ham token istenmez.

Ağ ayarı uygulandıktan sonra mevcut kimlik doğrulamayla depo/Pages yetkileri tekrar kontrol edilmelidir. Depo gizliyse herkese açık hale getirilmez; Pages plan uygunluğu veya alternatif yayın kullanıcıyla değerlendirilir. Remote `main` üzerinde mevcut iş varsa korunur; üzerine zorla yazılmaz. Kaynakları yükleme, Pages etkinleştirme, gerçek HTTPS isteği ve tarayıcı kontrolü başarılı olmadan “yayında” denmez.

## Kontroller

- Node web sunucusu çalıştırıldı; yalnız izinli web dosyalarını sunuyor. Bilinmeyen dosya/yol 404, yazma isteği 405, HEAD isteği 200.
- `python test/preview_smoke.py`: iframe içi ders/özet/test, ekran boyutu değişimi, 1:1/sığdırma, dar ekranlarda taşma ve sunucu erişim kontrolleri geçti.
- `AKADEMI_TEST_URL` yeni sunucuyu gösterecek şekilde 11 mevcut web regresyon grubu geçti; JavaScript hatası görülmedi.
- Export edilen tek HTML ve mobil önizlemenin ders/soru akışı HTTP üzerinden doğrulandı; bulut tarayıcısında yerel file:// açılışı yönetici politikasıyla engellendi.
- Kamera ve ses tarayıcı/cihaz desteğine bağlı. Gerçek AI hâlâ bağlı değil. Android test APK'sı önceki aşamada üretildi; bu web önizleme değişiklikleri için mobil paket yeniden derlenmedi. iOS derlemesi yapılmadı.
