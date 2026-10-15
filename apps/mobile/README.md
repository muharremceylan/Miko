# Akademi AI — Flutter kaynak denemesi (v0.3)

> 15 Ekim 2026: Kullanıcının Flutter kullanmama talebiyle aktif yol `../capacitor` oldu. Bu klasör tarihsel kaynak olarak korunur; aşağıdaki Flutter kurulum adımları aktif mobil iş akışı değildir.

## Güncel durum

HTML prototipi korunarak `apps/mobile` altında modüler Dart/Flutter kaynakları hazırlandı. Bu klasör henüz derlenmiş, cihazda doğrulanmış mobil uygulama değildir. 14 Ekim 2026 ortamında Flutter kaynak SDK'sı indirildi ancak Dart/engine indirmesi `storage.googleapis.com` için ağ politikasından 403 aldı. Bu nedenle `flutter analyze`, 14 Flutter testi ve APK derlemesi **henüz çalıştırılmadı**; Android/iOS platform klasörleri de henüz Flutter tarafından üretilmedi.

Doğrulananlar: Android SDK platform 36, build-tools 36.0.0, komut satırı araçları 19.0 kurulumu; resmî arşiv checksum kontrolü; adb sürümü; 18 Dart dosyasının parser kontrolü; shell/Python yardımcı dosyalarının sözdizimi; örnek içeriğin aktarılması. Parser kontrolü Dart tip kontrolü veya çalışan Flutter uygulaması kanıtı değildir.

## Hazırlanan uygulama kapsamı

- Material 3 tabanlı Türkçe arayüz, ana sayfa/dersler/testler/araçlar/analiz alt gezinmesi.
- Özgün prototipin dört dersi ve on sorusu `assets/sample_content.json` içinde korunur. Tam KPSS/AGS müfredatı değildir; uzman onayı gerektiren örnek içeriktir.
- Anlatım/kısa özet, dersten teste geçiş; konu filtresi, tekrarsız sonlu test, doğru/yanlış açıklaması ve sonuç ekranı.
- Tarihli cevap geçmişinden günlük hedef ve toplam/ders analizi; 10 ve üzeri cevapta günlük hedef dolu kalır.
- Yerel cihaz kaydı, kayıt şeması doğrulaması, okuma/yazma hatası bildirimi ve sıralı yazma. HTML localStorage kaydı ayrı tarayıcıya aittir; otomatik mobil aktarım yapılmaz.
- Yanlış Defteri: son cevabı yanlış olan sorular; ilgili konu; tekrar testi. Doğru tekrarda listeden çıkar, geçmiş toplamları korunur.
- Cihaz Türkçe TTS desteğiyle sesli özet için plugin entegrasyonu; alternatif metin. Ses ekranından çıkış ve uygulama arka plana geçişinde durdurma.
- Kamera/galeri seçimi, JPEG/PNG/WebP ve 10 MB kontrolü, geçici önizleme. Fotoğraf hiçbir AI servisine gönderilmez; sabit matematik çözümü açıkça demo olarak sunulur.

Gerçek AI, üyelik, FastAPI/PostgreSQL, bulut senkronizasyonu, süreli test, çoklu ders seçimi, yarım test kurtarma, podcast ve çalışma koçu sonraki kapsamdır. Yerel kayıt shared_preferences tabanlı bir prototip çözümüdür; kritik üretim verisi için kalıcı veritabanı/senkronizasyon ayrıca tasarlanmalıdır. AI anahtarı veya sahte AI servisi yoktur.

## Araç zinciri ve çalışma adımları

Flutter resmî stable **3.47.7**, commit `abaf9c523780a608bd46686fd5e53740a07077f8` seçildi. Pubspec bağımlılıkları sürümle sabitlendi; transitive `pubspec.lock` ilk başarılı `pub get` ile oluşturulup kaydedilmelidir. Kilit dosyası henüz oluşturulamadı.

Bu bulut ortamında Flutter'ı kullanıcının bilgisayarına indirmesi gerekmez. Ortam ayarlarında `storage.googleapis.com` ağ izni kaydedilip çalışma ortamına uygulanınca:

```bash
cd /workspace/Miko
bash scripts/setup_mobile.sh
bash scripts/prepare_mobile.sh
```

İlk script SDK'yı doğrular ve Android/pub önkoşullarını kurar. İkinci script resmî `flutter create` ile yalnız eksik Android/iOS hostlarını üretir; izin/açılış adını yapılandırır, paketleri çözer, analiz/test çalıştırır ve **debug APK** oluşturmayı dener. Bu scriptin tamamı henüz yürütülmüş değildir. Var olan Dart kaynaklarını `--overwrite` ile değiştirmez. Üretilecek uygulama kimliği `dev.akademiai.akademi_ai` geliştirme kimliğidir; mağaza kimliği ve imzalama yayın öncesi kesinleştirilmelidir.

Beklenen APK yolu: `apps/mobile/build/app/outputs/flutter-apk/app-debug.apk`. Bu dosya şu anda mevcut değildir. Emulator veya USB bağlı cihaz henüz sağlanmadı; APK testi için Android cihaz gerekir. Debug APK mağaza yayını için uygun imzalanmış release değildir.

Araç zinciri açıldıktan sonra:

```bash
source /workspace/Miko/scripts/mobile_env.sh
cd /workspace/Miko/apps/mobile
flutter analyze
flutter test
flutter devices
flutter run -d <android-cihaz-kimliği>
```

iOS için aynı Dart kaynakları ve oluşturulan `ios/` hostu macOS/Xcode ortamında derlenmelidir. Apple geliştirici hesabı ve imzalama dağıtım için gerekir; Linux ortamında iOS paketi üretildiği iddia edilmez.

## Klasörler ve testler

`lib/models`: içerik, tarihli cevap/ilerleme ve test oturumu. `lib/data`: değiştirilebilir cihaz kayıt arayüzü. `lib/core`: durum ve sıralı kayıt yönetimi. `lib/features`: ekranlar. `lib/app`: Türkçe tema ve gezinme. `test`: 10 model/kayıt testi ve 4 widget testi.

Kontrol senaryoları: 10/11 hedefi, gün değişimi ve toplam koruma, yanlış defterinden doğru tekrar çıkarılması, cevap kilidi/sonlu test/boş havuz, kayıt kalıcılığı, bozuk şema ve okuma/yazma hataları, eşzamanlı yazma, sıfırlama, mobil gezinme, özet geçişi, test sonucu ve yanlış defteri ekranı. Bunlar hazırlanmış testlerdir, geçmiş test sonucu değildir. Kamera, TTS, büyük yazı, erişilebilirlik ve Android/iOS yaşam döngüsü fiziksel cihazda ayrıca doğrulanmalıdır.
