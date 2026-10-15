# AKADEMİ AI — Önceliklendirilmiş Görevler

Bu liste 14 Ekim 2026 incelemesine dayanır. P0 ilk geliştirme öncesi karar/engel, P1 MVP, P2 genişleme, P3 ileri özellik anlamındadır. Onaylanmamış örnek içerik üretim içeriği değildir. İlk inceleme sonrasında kullanıcı düzeltmeleri yetkilendirdi; v0.2 kapsamında aşağıdaki görevler uygulandı.

## Yeni Matematik gereksinimleri — uygulanacak işler

Ayrıntılı kapsam ve kabul ölçütleri: [MATH_REQUIREMENTS.md](MATH_REQUIREMENTS.md). İşaretlenen maddeler ilk Temel Kavramlar çalışma paketi için uygulandı; tüm müfredat veya uzman onayı tamamlanmış sayılmaz.

- [x] A–E içerik alanlarını ve Matematik ana sayfası/yedi sekmeyi mevcut kodla karşılaştır; içerik şemasını, ekran akışını ve bağımlılıkları belgele.
- [x] M01 — Konu kimlikleri, içerik sürümü/onay durumu, beş seçenekli soru ve ayrıntılı deneme/cevap modeli oluştur; eski toplamları koru, geçmiş cevap uydurma.
- [x] M02 — Matematik ana ekranına ilerleme, tamamlanan/kalan konu, matematik soru sayısı/doğruluğu ve gerçek son çalışılan konu ekle. İlerleme ile başarıyı ayrı hesapla; hazırlanan konuların eksikliği gizlenmesin.
- [x] M03 — Ana/alt konu için yedi sekmeli erişilebilir mobil ekran oluştur; özet içinde üç seviye; eksik içerik/ses/AI için açıklayıcı durum göster.
- [x] M04 — Temel Kavramlar paketini hazırla: tanım, kavram, kural, formül, gerekçeli örnek, bağlantı, KPSS tekniği, hata, hatırlatma; üç özet ve özgün ses metni.
- [x] M05 — Kolay/orta/zor çözümlü örnekleri ve 30 farklı test sorusunu beş seçenekle hazırla; sonuç/koşul/tek doğru kontrollerini kodla doğrula; editör/uzman inceleme durumunu kaydet.
- [x] M06 — Yeterli gerçek havuzda 10/20/30, rastgele, son cevabı yanlış ve çözülmemiş filtrelerini uygula; yetersiz/boş havuz, tekrarsızlık ve çift cevap kaydı kontrollerini tamamla.
- [x] M07 — Test sonucu ve tekrar bağlantıları: doğru/yanlış/boş, doğruluk, süre, konu analizi; yarım denemeyi sürdürme ve kayıt hatası yönetimini doğrula.
- [ ] M08 — Sayılar ve alt konularından başlayarak diğer içerik paketlerini aynı ölçütlerle genişlet; mevcut denklem örneklerini yeni konu/soru şemasına taşı.
- [ ] M09 — Gerçek medya sağlandığında oynat/duraklat, sarma, hız ve dinleme konumunu uygula; cihaz TTS'sini ayrı etiketle; arka plan oynatmayı platformlarda doğrula.
- [ ] M10 — Gerçek AI'ı FastAPI üzerinden konu bağlamı ve doğrulama durumuyla bağla; anahtarlar yalnız sunucuda. Hizmet yokken hazırlık durumu korunsun.

Sıra: M01–M03 → M04–M05 → M06–M07 → M08. M09–M10 ilgili medya/hizmet hazır olduğunda ilerler. İlk kullanılabilir içerik örneği Temel Kavramlar tamamlandı; M08 kapsamında sonraki konu Sayılar ve alt konularıdır. Uzman incelemesi, gerçek ses/AI ve Android/iOS cihaz doğrulaması beklenir. Tüm müfredatın tamamlandığı iddia edilmez.

## Güncel adım — KPSS düzeyleri ve Lisans Matematik

- [x] KPSS → Lisans / Ön Lisans / Ortaöğretim seçimini ve tercih kalıcılığını ekle.
- [x] Düzeylerin soru ilerlemesini ayır; eski demo kaydını Lisans alanında koru; eski tercih biçiminde düzeyi kullanıcı seçsin.
- [x] Geometri ve Güncel Bilgiler ders alanlarını ekle; içerik ve soru yokluğunu açık göster.
- [x] Kullanıcının paylaştığı 17 matematik ana konusunu ve alt konuları Lisans alanına ekle.
- [x] 26 soruluk genel dağılımı kaynak açıklamasıyla ekle.
- [x] Görseldeki 2015–2024 yıllık dağılımı, yıl seçimini, tam tabloyu ve kaynak toplamı/hesaplanan toplam ayrımını ekle.
- [x] Mevcut denklem örneği/özet/üç soru akışını konu listesine bağla.
- [x] Kaynak aktarımını ve uyuşmazlıklarını CONTENT_SOURCES.md içinde belgele.
- [ ] P1: Kaynaktaki altı yıllık toplam farkını resmî/uzman kaynakla doğrula; doğrulanmış yeni kaydı kaynak/sürüm bilgisiyle yayımla.
- [ ] P1: Bağıntı/Fonksiyon ve konu listesi/dağılım gruplarını karşılaştır; sınav kapsamını doğrula.
- [ ] P1: Lisans Matematik Temel Kavramlar ile başlayarak anlatım, kısa/orta/ayrıntılı özet, örnek ve editör onaylı soruları ders ders hazırla.
- [ ] P1: Sorulara konu kimliği ve içerik onay/sürüm bilgisi ekle; konu bazlı test ve analizi tamamla.
- [ ] P2: Geometri için düzeye özel konu listesi ve özgün görseller; Güncel Bilgiler için kaynak/olay tarihi/son kontrol tarihi hazırla.
- [ ] P2: Ön Lisans ve Ortaöğretim için düzeye özel onaylı müfredat ve soru havuzları ekle.

## Tamamlanan inceleme

- [x] ZIP içindeki index.html ve README.md dosyalarını incele; özgün dosyaları koru.
- [x] HTML prototipini yerel HTTP sunucusunda çalıştır.
- [x] Dört ders, kısa özet, konu testi, 10 cevap, analiz, kayıt kalıcılığı, sıfırlama ve fotoğraf önizlemesini tarayıcıda doğrula.
- [x] Günlük hedef çubuğu ve bozuk localStorage başlangıç hatasını yeniden üret.
- [x] Seslendirme sınırını kaydet: Türkçe ses bulunmadı, işitilebilir çıktı doğrulanmadı.
- [x] Mevcut durum, mimari, ekran/akış planı ve görev listesini Türkçe hazırla.

## Güncel küçük adım — sınav seçimi ve gündüz/gece modu

- [x] İlk açılışta KPSS/AGS seçimini ana ekrana ekle; sınav seçmeden çalışma içeriğini açma.
- [x] KPSS örnek alanını koru; AGS'yi seçilebilir hazırlık durumu olarak ayır.
- [x] Sınava göre ders/soru erişimini ve ilerleme anahtarını ayır; eski KPSS kayıtlarını koru.
- [x] Gündüz/gece modunu tüm mevcut uygulama ekranlarına uygula.
- [x] Sınav/tema tercihini sakla; bozuk/engelli kayıt durumlarını yönet.
- [x] Test oturumunu tema değişiminde, KPSS ilerlemesini sınav değişiminde koru.
- [x] Varlık ve iframe URL'lerine içerik hash'i ekle; tek HTML export uyumunu doğrula.
- [x] Dokuz ayar kontrol grubu, mevcut 11 web grubu, önizleme/export ve 12 native köprü mock testini geçir.
- [ ] KPSS içeriklerini kullanıcıyla ders ders geliştirmeye başla; mevcut dört örnek konu tam müfredat sayılmaz.
- [ ] AGS ve diğer ÖSYM sınavlarına onaylı içerikler hazır oldukça geç.

Bu adım web sürümüne yöneliktir; Android/iOS paketleri yeniden derlenmedi.

## Güncel aşama — web üzerinde mobil önizleme

- [x] Telefon çerçevesi, üç boyut, 1:1/sığdırma ve uygulamayı ayrı açma denetimlerini ekle.
- [x] npm start ile tekrarlanabilir, dosya erişimi sınırlı web sunucusunu başlat.
- [x] Önizleme iframe'i içinde ders/özet/soru akışını ve boyut geçişlerini doğrula.
- [x] Yeni web sunucusunda mevcut 11 regresyon grubunu geçir.
- [x] Statik yayın ZIP'i ve tek HTML sürümü üret; yayın paketini HTTP üzerinden doğrula.
- [x] GitHub Pages iş akışını ve kullanıcı için yayın durumunu hazırla.
- [ ] Ortam ayarlarında GitHub API ve yayın kontrol adreslerinin ağ izinlerini uygula.
- [ ] GitHub depo görünürlüğü, Pages planı ve yazma/yayın erişimini mevcut kimlik doğrulamayla kontrol et.
- [x] Kaynakları `main` dalına gönder; origin/main ile ilk commit `25c22e1` eşleşti.
- [x] GitHub iş akışını kontrol et: ilk deneme Pages yapılandırmasını bulamadı.
- [x] Kullanıcının Pages ayarından sonra yayını yeniden çalıştır: 38692055701 başarılı. Ana önizleme, app.html ve preview.js canlı HTTP kontrolleri geçti.
- [ ] Web üzerinde istenen tasarım/işlevleri tamamladıktan sonra Android APK'sını yeniden derle; iOS paketini macOS/Xcode'da hazırla.

Önceki Android APK üretimi geçerlidir, ve yeni web önizlemesi https://muharremceylan.github.io/Miko/ adresinde yayımlandı. Canlı HTTP kontrolü geçti; canlı sitede uzaktan tarayıcı uçtan uca testi henüz yapılmadı.

## v0.4 — Aktif Capacitor mobil yolu

- [x] Kullanıcı tercihiyle Flutter bağımlılığını aktif iş akışından çıkar; mevcut kaynakları koru.
- [x] Capacitor 8 projesini, sürümü sabit npm bağımlılıklarını ve package-lock dosyasını oluştur.
- [x] HTML prototipini değiştirmeden paketleyen build scriptini hazırla.
- [x] Android ve iOS hostlarını üret; iOS kamera/galeri izin açıklamalarını ekle.
- [x] Yerel kamera/galeri, Türkçe TTS, arka plan durdurma, geri tuşu ve kamera aktivite kurtarma bağlantılarını ekle.
- [x] Mobil güvenli alanları, uygulama adını ve Android açılış simgesini ekle.
- [x] Paketlenen web arayüzünde 11 regresyon grubu ve güvenli alan kontrolünü geçir.
- [x] Native API'leri taklit eden 11 köprü davranışı testini geçir.
- [x] Telefon boyutunda ana sayfa/ders/test ekran görsellerini oluştur ve görsel tasarımı belgele.
- [x] Android debug APK derlemesini tamamla: 187 görev başarılı; APK v2 imzası ve paket içindeki web varlıkları doğrulandı. Sonuç README'ye kaydedildi.
- [ ] Android cihazda kurulum/açılış, geri tuşu, kamera/galeri, Türkçe ses ve uçak modu akışını doğrula.
- [ ] iOS projesini macOS/Xcode ve cihazda doğrula; yayın kimliği/imzasını kesinleştir.
- [ ] Yanlış defteri ve sonraki modülleri aktif web kaynaklarına, testleriyle birlikte aktar.

Aşağıdaki v0.3 Flutter ağ/derleme maddeleri tarihsel durumdur; aktif yolun ön koşulu değildir. T08 ve sonraki mobil görevler artık Capacitor istemcisi olarak değerlendirilir; backend/içerik onayı maddeleri geçerlidir.

## v0.3 — Mobil kaynak aşaması

- [x] Flutter klasörlerini, Türkçe Material 3 gezinmesini ve yerel örnek veriyi oluştur.
- [x] Ders/özet, test/sonuç, analiz ve yanlış defteri kaynaklarını hazırla.
- [x] Cihaz kaydı arayüzünü, bozuk kayıt yönetimini ve sıralı yazmayı hazırla.
- [x] Kamera/galeri demosu ve Türkçe TTS plugin kodunu hazırla; bunlar cihazda test edilmedi.
- [x] Android SDK 36/build-tools ve resmî checksum doğrulanmış komut satırı araçlarını kur.
- [x] 14 Flutter testini hazırla; Dart parser ve yardımcı script sözdizimi kontrollerini yap.
- [ ] Flutter/Dart indirme ağ engelini çöz: ortam ayarlarında `storage.googleapis.com` değişikliğini kaydet/uygula.
- [ ] Resmî `flutter create` ile Android/iOS hostlarını üret; izinleri yapılandır.
- [ ] `flutter pub get` ile lockfile oluştur; `flutter analyze` ve 14 testi çalıştır, bulunan sorunları düzelt.
- [ ] Android debug APK derle ve fiziksel cihaz/emulatörde doğrula.
- [ ] iOS hostunu macOS/Xcode'da derle ve kamera/TTS/yaşam döngüsünü cihazda doğrula.

T08 başlangıç kaynağı hazırdır, fakat derleme/cihaz doğrulaması bekleniyor. T09–T17'deki backend, onaylı içerik ve sunucuda puanlama tamamlanmış değildir. Yanlış defteri şu anda yalnız örnek havuza ve yerel cihaza dayanır.

## v0.2 — Tamamlanan düzeltmeler

- [x] T03 — Günlük sayaçları ayır; 10/11 cevapta hedefi dolu tut; gün geçişinde toplamları koru.
- [x] T04 — Bozuk/uyumsuz/engelli cihaz kaydında açılışı koru; eski biçimi taşı ve kayıt hatasını bildir.
- [x] T05 — Temel test oturumunu sonlandır; Fisher–Yates, sonuç ekranı, çift cevap ve boş havuz yönetimi ekle. Süre/çoklu ders/yarım oturum kurtarma T14 kapsamındadır.
- [x] Görsel tür/boyut ve decode hatası yönetimi; object URL temizliği.
- [x] Ses ekranından çıkışta durdurma ve eski olayların durum mesajını değiştirmesini engelleme.
- [x] 11 tarayıcı kontrol grubunu çalıştır; çalışma zamanı hatası görülmedi.

## P0 — İlk geliştirme öncesi

| ID | Görev | Bağımlılık | Kabul ölçütü |
|---|---|---|---|
| T01 | Sınav türü ve MVP müfredatını resmî kaynaklarla tanımla | Yok | KPSS/AGS kapsamları, ders/konu eşlemeleri ve güncelleme sorumlusu kayıtlı |
| T02 | Örnek içerikleri uzman incelemesine ayır; kaynak/telif politikasını belirle | T01 | Her yayın içeriğinde kaynak, kontrol tarihi, izin ve onay durumu; izin yoksa çıkmış sorular kopyalanmıyor |
| T03 | Hedef sayacı ve günlük tarih modelini düzelt | Ayrı kodlama görevi | 0/9/10/11 cevap, gün geçişi ve saat dilimi testleri; 10'da dolu hedef; günlük ve toplam ayrı |
| T04 | localStorage ayrıştırma/yazma hatalarını güvenli yönet | Ayrı kodlama görevi | Bozuk JSON, yanlış şema, depolama engeli/kota durumlarında ekran açılıyor; kullanıcıya veri kurtarma durumu bildiriliyor |
| T05 | Testi oturum, sonuç ve dengeli karıştırmayla sınırlandır | T01 | Fisher–Yates; havuz boyutu sınırı; aynı cevap bir oturumda tek kayıt; bitiş ekranı; boş havuz durumu |
| T06 | Mimari kararları ve API sözleşmelerini kesinleştir | T01 | Flutter dikey dilimi, auth yöntemi, offline kapsamı, alan modelleri ve API hata/idempotency kuralları belgeli |
| T07 | Veri ve güvenlik tasarımını çıkar | T06 | Veri envanteri, rol/sahiplik, saklama/silme, AI aktarımı ve secret yönetimi tanımlı; anahtar istemcide yok |

## P1 — Kullanılabilir MVP

| ID | Görev | Bağımlılık | Kabul ölçütü |
|---|---|---|---|
| T08 | Flutter modüler temelini, Türkçe tema/router ve ortak durumları kur | T06 | Android başlangıç akışı; metin ölçekleme, ekran okuyucu etiketleri; iOS derleme için macOS iş akışı tanımlı |
| T09 | FastAPI/PostgreSQL geliştirme ortamı, migration ve CI kur | T06–T07 | Temiz kurulum/migration, API entegrasyon testleri ve geçerli OpenAPI; production secrets ayrı |
| T10 | Hesap/misafir ve profil-hedef akışını uygula | T08–T09 | Oturum yenileme, çıkış, güvenli token saklama ve başka kullanıcı verisine erişim reddi testli |
| T11 | Asgari editör/uzman paneli ve yayın akışını kur | T02,T09 | Taslak→inceleme→yayın; rol ayrımı, gerekçeli ret, değişiklik izi ve yayın geri alma |
| T12 | Ders, konu, örnek/görsel ve üç uzunlukta özet ekranlarını taşı | T01,T08,T11 | Onaylı içerik API'den okunuyor; sınav filtresi, kaynak/güncellik ve boş durum gösteriliyor |
| T13 | Soru bankası filtrelerini ve açıklamalı cevabı uygula | T11–T12 | Ders/konu/zorluk/sınav filtresi; yalnız yayınlı sorular; puanlama sunucuda; soru sürümü korunuyor |
| T14 | Çoklu ders, sayı, süre ve test sonuç ekranını uygula | T13 | Süre sonu/erken bitiş/boş/yeniden açma; soru havuzu sınırı; idempotent cevap; sınava göre net formülü |
| T15 | Yanlış defteri ve tekrar testini uygula | T13–T14 | Yanlış kaydı ilgili soru sürümü/konuya bağlanıyor; yeniden çözme geçmişi korunuyor |
| T16 | Temel analiz ve günlük ana sayfayı kur | T10,T14–T15 | Net, doğru/yanlış/boş, ders/konu, süre ve tarih aralığı tutarlı; sıfır veri durumu doğru |
| T17 | Uçtan uca MVP ve erişim testlerini tamamla | T10–T16 | İçerik→test→yanlış→analiz akışı Android/iOS'ta; erişim ve tekrar gönderim testleri; açıklanmamış hata yok |

## P2 — Tekrar, ses, offline ve içerik genişlemesi

| ID | Görev | Bağımlılık | Kabul ölçütü |
|---|---|---|---|
| T18 | Kural tabanlı çalışma koçu ve tekrar takvimi | T10,T15–T16 | Sınav tarihi, günlük süre, zayıf konu ve geciken görevler hesaba katılıyor; önerinin kaynağı belirtiliyor |
| T19 | Türkçe TTS ve ses oynatıcı | T08,T12 | Fiziksel cihazlarda Türkçe ses; duraklat/durdur/hız; izin/hata durumları; alternatif metin erişimi |
| T20 | Lisanslı podcast/ses dosyaları, indirme ve devam etme | T11,T19 | Kaynak/izin, oynatma konumu, indirme silme, bağlantı kopması ve özel medya erişimi testli |
| T21 | Offline içerik/cevap kuyruğu ve senkronizasyon | T09,T14 | Bağlantı kesilmesi/yeniden gönderme/çakışma yönetiliyor; kişisel önbellek çıkışta temizleniyor |
| T22 | İzinli çıkmış sorular kataloğu | T02,T13 | Yıl/sınav/konu filtresi; izin kaydı; izin alınamazsa resmî erişim bağlantısı ve açık durum |
| T23 | Fotoğraf modülünün dosya/izin temelini kur | T07,T08–T09 | Kamera reddi, boyut/tür, kırpma, EXIF temizliği, imzalı yükleme ve silme; demo etiketleri korunuyor |

## P2 — Gerçek AI için zorunlu kalite kapıları

| ID | Görev | Bağımlılık | Kabul ölçütü |
|---|---|---|---|
| T24 | Sağlayıcı karşılaştırması ve uzman değerlendirme seti | T02,T07 | Türkçe metin/görsel/matematik, maliyet/gecikme/veri koşulları ölçülüyor; yayın eşikleri önceden tanımlı |
| T25 | Sunucu adaptörü, kuyruk ve iş durumlarını kur | T09,T24 | Anahtarlar yalnız sunucuda; kota, iptal, zaman aşımı, hata ve model/prompt sürümü kayıtlı |
| T26 | OCR metin onayı ve adımlı fotoğraf çözümü | T23,T25 | Kullanıcı okunan soruyu düzeltiyor; formül/şekil güvenli render; gerçek sonuç ile demo ayrımı |
| T27 | Doğrulama hattını uygula | T24–T26 | Matematik kontrolü, şık tutarlılığı, kaynak/güncellik; çelişkide kesin sonuç yok; uzman setinde ölçülen kalite |
| T28 | AI öğretmen ve ipucu/alternatif çözüm | T12,T25,T27 | Konu bağlamı ve kaynak; belirsizlik/hata; sohbet sahipliği ve silme; görsel/metin prompt injection sınırları testli |
| T29 | AI soru taslağı üretimi ve insan inceleme kuyruğu | T11,T25,T27 | Otomatik yayın yok; tek doğru cevap, çözüm, kaynak/telif ve uzman onayı tamamlanıyor |

## P3 — İleri özellikler ve yayın

- [ ] T30 — İki anlatıcılı podcast ve kişiye özel sesli tekrar: T20,T25 sonrası; lisanslı ses ve editör onayı, maliyet sınırı.
- [ ] T31 — Uyarlamalı koç: T18,T24 sonrası; basit kural tabanlı plana karşı fayda ölçümü ve açıklanabilir öneri.
- [ ] T32 — Bildirimler ve hatırlatmalar: izin, saat dilimi, sessiz saat ve kapatma akışı; görev tarihleriyle tutarlılık.
- [ ] T33 — İçerik kapsamını genişlet: uzman kapasitesine göre tüm hedef müfredat, tarihli mevzuat güncellemeleri ve kalite kontrolü.
- [ ] T34 — 15–30 katılımcılı mobil pilot: kamera/TTS, erişilebilirlik, offline, test bitişi, AI belirsizliği ve cihaz performansı; bulguların önceliklendirilmesi.
- [ ] T35 — Yayın hazırlığı: KVKK/aktarımı, içerik izinleri, hesap silme, güvenlik incelemesi, migration/yedek geri yükleme, gözlemleme ve maliyet alarmları.
- [ ] T36 — Android/iOS paketleme: macOS/Xcode, geliştirici hesapları ve imzalama; mağaza gizlilik formları; yayın sonrası hata/geri alma planı.

## Uygulama sırası ve doğrulama yaklaşımı

İlk sıra: T01–T07 → T08–T11 → T12–T17. Ardından koç/ses/offline içerik ihtiyacına göre; gerçek AI yalnız T24–T27 kalite kapılarından sonra. İçerik ekibi onaylı örnek havuzu teknik dikey dilimle birlikte hazırlar. Hedef, büyük toplu yeniden yazım yerine ders→soru→sonuç→yanlış defteri→analiz akışını küçük, gözden geçirilebilir değişikliklerle tamamlamaktır.

Birim testleri hesaplama/planlama kurallarına, PostgreSQL entegrasyon testleri migration/işlem/sahiplik/idempotency davranışına, mobil uçtan uca testleri ana akışa odaklanır. AI değerlendirmeleri sürüm sabitlenmiş uzman cevaplı setle yürütülür; tek başarılı demo yeterli değildir. Sesli çıktı ve kamera gerçek cihazda ayrıca doğrulanır. Test edilmeyen özellik tamamlandı işaretlenmez.

Mevcut HTML uygulamasını büyük çapta değiştirmeden önce bu durum raporu incelenmelidir. v0.2 tamamlananlar bölümünün dışındaki geliştirme görevleri henüz uygulanmış değildir; gerekecek sağlayıcı anahtarları sohbetten istenmez, güvenli ortam ayarlarında tanımlanır.
