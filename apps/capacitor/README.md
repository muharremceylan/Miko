# Akademi AI — Capacitor mobil uygulama (v0.4)

Aktif mobil geliştirme yolu **Capacitor 8 + mevcut HTML/CSS/JavaScript**. Flutter kullanılmaz. Uygulama web sayfasını uzaktan açmaz; dört örnek ders ve on soruluk içerik Android paketinin içine kopyalanır, temel ders/soru akışı çevrimdışı kullanılabilir.

Kaynak web uygulaması `../../akademi_ai_prototip/index.html` dosyasıdır. `scripts/build.mjs` bu dosyayı değiştirmeden HTML/JavaScript varlıklarını `www/` içine çıkarır; `src/native.js` cihaz bağlantısını ve `src/mobile.css` mobil güvenli alanlarını ekler. `www/` ve native hostlara kopyalanan web dosyaları üretilmiş çıktıdır; doğrudan düzenlenmez. Flutter denemesi `../mobile` altında tarihsel kaynak olarak korunur; bu uygulamanın build adımlarına dahil değildir.

## Öncelik: web tarayıcısında mobil görünüm

Kullanıcının güncel tercihi önce web üzerinde telefon görünümüyle geliştirmek, ardından Android/iOS paketlerini hazırlamaktır. `npm start` web sunucusunu, `/preview.html` mobil çerçeveyi açar. `npm run export:web` yayın dosyalarını üretir; GitHub Pages hazırlığı, kontroller ve henüz çözülmeyen erişim adımı [WEB_PREVIEW.md](WEB_PREVIEW.md) içindedir.

## Ekranların görsel tasarımı

Lacivert gradyan başlık, kırık beyaz arka plan, beyaz yuvarlak kartlar ve mor/indigo ana işlem butonları kullanılır. Tasarım mobilde tek sütun, ana sayfa kısayollarında iki sütundur. Alt gezinme: Ana sayfa, Dersler, Sorular, Dinle, Analiz. İçerik genişliği büyük ekranda 490 px ile sınırlandırılır.

- **Ana sayfa:** günlük soru hedefi, doğru ve başarı oranı; ders/test/ses/fotoğraf kısayolları.
- **Dersler:** dört ders kartı; konu detayında anlatım/kısa özet ve ilgili test.
- **Sorular:** ders filtresi, büyük şıklar, seçilen yanlış ve doğru cevapların renklendirilmesi, açıklama; son soruda sonuç kartı.
- **Dinle:** konu seçimi, dinle/durdur ve ses durumu. Türkçe ses yoksa kullanıcıya metin alternatifi sunulur.
- **Fotoğraf:** çek/galeriden seç; görsel önizlemesi ve açıkça etiketlenmiş sabit çözüm demosu.
- **Analiz:** toplam doğru/yanlış ve ders doğruluğu; AI olmayan basit tekrar önerisi.

Renk ve metin birlikte geri bildirim verir. Klavye odakları belirgindir; şık butonları en az 52 px yüksekliğindedir. Android çentik/sistem çubuğu için Capacitor safe-area değişkenleri, iOS için env() fallback kullanılır. Büyük yazı ve ekran okuyucuyla gerçek cihaz doğrulaması henüz yapılmadı.

Telefon boyutunda gerçek tarayıcı görüntüleri `/workspace/outputs/akademi-ai-ana-sayfa.png`, `akademi-ai-ders.png`, `akademi-ai-test.png` dosyalarında bulunur. Bunlar paketle aynı web varlıklarının Chromium görüntüleridir, emülatör ekran görüntüsü değildir. Ana sayfadaki üç cevap test verisidir.

## Cihaz bağlantıları

- Kamera: Capacitor Camera ile sistem kamera/galeri seçimi. Görsel mevcut 10 MB ve JPEG/PNG/WebP kontrolünden geçer. Galeriye otomatik kaydetme ve geniş depolama izni yoktur. Android aktivitesi işletim sistemi tarafından kapatılıp yeniden açılırsa `appRestoredResult` ele alınır.
- Ses: cihazın Türkçe TTS motoru kullanılır. Konu değişimi, ekran değişimi veya arka plana geçişte durdurulur. Cihazın Türkçe ses paketine ve motorunun koşullarına bağlıdır; tüm seslerin çevrimdışı çalışacağı garanti edilmez.
- Android geri tuşu: konu detayından ders listesine, diğer sekmelerden ana sayfaya döner; ana sayfada çıkış onayı gösterir.
- İlerleme WebView localStorage içinde kalır. Normal tarayıcı veya önceki Flutter denemesiyle otomatik senkronizasyon yoktur. Uygulama verilerinin temizlenmesi/kaldırılması ilerlemeyi siler. Android otomatik yedekleme kapalıdır.

## Kurulum ve Android derleme

Bu bulut ortamında Node.js 24, Temurin JDK 21.0.12.1+1, Android SDK 36, build-tools 35/36 ve Gradle 8.14.3 kullanılır. Temurin arşivi resmî GitHub sürümünün SHA-256 kaydıyla, Gradle dağıtımı resmî SHA-256 ile doğrulanır. TLS doğrulaması kapatılmaz. Java HTTPS bağlantıları ortamın mevcut proxy'sini ve `/etc/ssl/certs/java/cacerts` sistem güven deposunu kullanır; gizli bilgiler projeye kopyalanmaz.

```bash
cd /workspace/Miko/apps/capacitor
npm ci --cache /workspace/.tools/npm-cache --no-audit --no-fund
python scripts/install_jdk.py
# SDK henüz kurulmadıysa:
python /workspace/Miko/scripts/setup_android.py
npm run build
npx --no-install cap sync android
npm test
python scripts/build_android.py
```

Yerel SDK yolu Android Studio tarafından verilirse kendi SDK/JDK kurulumuyla `android/` klasörü açılıp normal Gradle derlemesi de kullanılabilir. `scripts/build_android.py` bu Linux bulut ortamına özeldir. Derlenen debug APK normalde `android/app/build/outputs/apk/debug/app-debug.apk` konumundadır. Bu geliştirme kimliği `dev.akademiai.mobile` ve debug imzası içindir; mağaza yayını için kalıcı kimlik ve release imzası ayrıca hazırlanır.

## Android derleme sonucu — 15 Ekim 2026

`assembleDebug` başarıyla tamamlandı: **BUILD SUCCESSFUL**, 187 görev yürütüldü. Debug APK üretildi ve APK Signature Scheme v2 doğrulaması geçti. Paket adı `dev.akademiai.mobile`, sürüm `0.4.0`, minimum Android API 24 (Android 7), hedef API 36. Dört paketlenmiş web dosyası (`index.html`, `app.js`, `native.js`, `mobile.css`) üretilen varlıklarla byte düzeyinde eşleşti.

Teslim dosyası: `/workspace/outputs/akademi-ai-v0.4-debug.apk` (yaklaşık 7,8 MiB).
SHA-256: `34f31dc7d9fd30e90bb07ef033068df4358eb4bd36aa2ec547de80e4666864e5`.

Bu başarı cihazda çalıştırma testi değildir. Kamera, Türkçe ses, sistem çubukları ve işletim sistemi yaşam döngüsü gerçek Android telefonda ayrıca doğrulanmalıdır. iOS projesi oluşturuldu ancak iOS derlemesi yapılmadı.

## Doğrulama

- Paketlenen web arayüzünde Chromium/Playwright ile 11 regresyon kontrol grubu geçti: ders/özet, filtre, 10 soruluk sonuç, kayıt kalıcılığı, hedef, gün değişimi, eski/bozuk kayıt ve depolama engeli, görsel hataları, ses iptali, sıfırlama ve mobil genişlikler.
- 24 px üst/alt safe-area kontrolü geçti.
- Web regresyonunu tekrar çalıştırmak için `www/` klasörünü 8001 portunda yerel sun ve Python Playwright/sistem Chromium mevcutken `python test/web_smoke.py` çalıştır. Test URL'si `AKADEMI_TEST_URL` ile değiştirilebilir. Bu yerel test adresi kullanıcı önizlemesi değildir.
- `npm test`: 11 native köprü davranışı testi geçti. Kamera/TTS/App API'leri bu testlerde taklit edilir; fiziksel cihaz testi yerine geçmez.
- Android debug APK derlemesi ve imza/varlık doğrulaması yukarıdaki sonuçla tamamlandı.
- Emülatör/USB cihaz sağlanmadığı için Android üzerinde açılış, gerçek kamera, Türkçe ses ve yaşam döngüsü uçtan uca doğrulanmadı.

## iOS

`ios/` Xcode projesi ve Swift Package Manager bağlantıları oluşturuldu; kamera/galeri kullanım açıklamaları eklendi. macOS/Xcode üzerinde `npm ci`, `npm run build`, `npx cap sync ios`, `npx cap open ios` ile devam edilir. iOS derlemesi bu Linux makinede yapılmadı; Apple imzalama ve cihaz doğrulaması gerekir.

## İçerik ve sonraki kapsam

Sorular örnektir, uzman onayı bekler; ÖSYM çıkmış soruları değildir. Gerçek AI bağlı değildir ve fotoğraf çözümü yüklenen görseli analiz etmez. Hesap, bulut backend/PostgreSQL, yanlış defteri, çalışma koçu, süreli test ve tam müfredat bu Capacitor sürümünde henüz yoktur. Flutter kaynaklarında hazırlanmış fakat doğrulanmamış yanlış defteri bu sürüme otomatik aktarılmış sayılmaz. Bu modüller mevcut web kodunu modüllere ayırarak ve sunucuda güvenli API kurarak geliştirilebilir. Sağlayıcı anahtarları istemciye konulmaz.
