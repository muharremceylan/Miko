# AKADEMİ AI — Proje Planı ve Mevcut Durum Raporu

## Telegram PDF aktarımı — 15 Ekim 2026

Bot hesabıyla MTProto kullanan ayrı `services/telegram` servisi hazırlandı. Özel sohbet sahibi bir kez eşleştirilir; PDF indirme/bölme, Türkçe OCR, kalıcı iş kaydı, yeniden gönderim, saklama ve silme akışı uygulandı. İçerik inceleme taslağıdır, uygulamaya otomatik aktarılmaz. GitHub yalnız kod/test içindir; kullanıcı henüz bot oluşturmadı ve sunucu hesabı yok. Gerçek Telegram bağlantısı ve canlı sunucu pilotu tamamlanmadı. Kurulum: [iPhone rehberi](../TELEGRAM_IOS_SETUP.md), [teknik kurulum](../services/telegram/README.md).

## Kullanıcının PDF ders notları — 15 Ekim 2026

Türkçe (109 sayfa) ve Tarih (264 sayfa) el yazısı taramalarına Türkçe OCR uygulandı. Ham OCR, doğrulanmış ders içeriği sayılmaz. İlk sayfalar ayrıntılı; ilerleyen bölümler küçük görsellerle örnekleme yoluyla incelendi. Vatandaşlık ve Coğrafya dosyaları 32 MiB aktarım sınırını aştığından açılamadı; küçük parçalar gerekiyor.

Lisans alanına ayrı PDF ders notları ekranı eklendi. Kaynak/sayfa eşleşmeli Sözcükte Anlam ve Asya Hun Devleti taslakları; renkli kartlar, tam metin, üç özet ve toplam dört özgün açıklamalı örnek sunar. Uzman incelemesi bekler; test puanı/ilerleme uydurulmaz. Ham PDF ve OCR metinleri web paketine alınmadı. Türkçe tam ders kataloğu ve iki PDF’nin bütün konuları henüz tamamlanmadı.

51 JavaScript testi, PDF notları tarayıcı testinde dört grup, önceki otomatik üretim testinde altı grup ve web yayın paketi testi geçti. 320–768 pikselde iki tema, kaynak durumları, örnek/özetler, geri dönüş ve eski kayıtların korunması doğrulandı. Ayrıntılı inceleme, sayfa örneklemesi, düzeltme notları ve sonraki işler [PDF_REVIEW.md](PDF_REVIEW.md) içinde kayıtlıdır.


## Kaynak kütüphanesi ve otomatik alıştırma — 15 Ekim 2026

Matematik ana ekranı ve konu ekranlarından altı aday kaynağa erişilir; kaynak türü süzülebilir, konuya geri dönülebilir. Katalog kurum/dil/amaç, kapsam, inceleme ve kullanım hakkını ayrı tutar. ÖSYM, OGM, ÖDSGM, EBA, OpenStax ve önceki Kitapseç bağlantısının içerikleri bu ortamda 403 nedeniyle incelenemedi; bağlantılar genel aday başvuru kaynağıdır. Belirli bölüm eşlemesi, lisans doğrulaması veya bu kaynaklarla anlatım zenginleştirmesi yapılmış sayılmaz. Kaynaklardan metin/soru aktarılmadı.

Temel Kavramlar ve Sayıların yedi alt konusu için 16 özgün matematik kalıbı ve 1706 sonlu parametre varyasyonu hazırdır. Test Çöz ekranında kayıtlı havuz veya otomatik alıştırma seçilir; 10/20/30 soru, tahmini kolay/orta/karışık düzey ve öğrenme/değerlendirme modu desteklenir. Cevap/seçenekler üretimden ayrı kodla kontrol edilir; sayısal kontrol uzman onayı değildir. Otomatik sorular AI veya çıkmış soru diye gösterilmez. Yarım test, sürümlü tekrar, yanlış defteri ve eski kayıtlar korunur. Kayıtlı 100 sorunun sayısı değişmedi; varyasyonlar farklı soru türü gibi sayılmaz.

Editör için komut satırından tekrarlanabilir JSON taslağı çıkarılabilir; mevcut dosya üzerine yazılmaz ve taslak kendiliğinden soru bankasına aktarılmaz. Gerçek AI üretimi, lisanslı kaynak deposu, kalıcı inceleme kuyruğu ve yayın akışı henüz uygulanmadı. Mimari, kaynaklar, çalışan kod ve sonraki görevler [CONTENT_PIPELINE.md](CONTENT_PIPELINE.md) içinde açıklanır.

Doğrulama: 49 JavaScript testi (bütün 1706 varyasyonun matematik kontrolü ve CLI taslak korumaları dahil), 18 API testi, yeni kaynak/üretim tarayıcı testinde altı grup, önceki Matematik testinde sekiz grup ve yayın paketi testi geçti. 320–768 pikselde gündüz/gece görünümü, 10/20/30 üretim, sonlu havuzun tükenmesi, yarım testin korunması, değerlendirme çözümünün gizlenmesi ve yanlış tekrarları doğrulandı. Dış kaynakların gerçek içerikleri, ücretli AI üretimi ve fiziksel Android/iOS cihaz doğrulaması bu kapsama dahil değildir.


## Sayılar çalışma paketi ve yanlış defteri — 15 Ekim 2026

Güncel web kapsamı: Temel Kavramlar + Sayı Kümeleri, Doğal Sayılar, Tam Sayılar, Faktöriyel, Sayma Sistemleri, Bölme ve Bölünebilme Kuralları. Yedi yeni alt konunun her birinde dört renkli anlatım/hatırlama kartı, tam metne geçiş, üç özet, formüller, iki ayrı çözümlü örnek ve 10 test sorusu vardır. Toplam havuz 100 test sorusu ve havuzdan ayrı 17 çözümlü örnektir. Sayılar ana ekranı alt konu rotası ve 70 soruluk havuz üzerinden 10/20/30 soruluk karma test sunar. Alt konu havuzu 10 olduğu için 20/30 düğmeleri açıkça pasiftir; içerik tamamlanmış gibi gösterilmez. Sonraki içerik adımı EBOB–EKOK ve Asal Çarpanlara Ayırma; ardından Denklemler paketidir.

Anlatım/özet/ses verileri konu kimliğiyle seçilir. Temel Kavramlara özgü kartların diğer konularda görünmesi önlendi. Üç uzunlukta seslendirme metni hem cihaz TTS yoluna hem sunucudaki izinli ses metni kataloğuna bağlandı. Sunucu ses önbelleği konu+sürüm+özet seviyesine göre ayrılır; istemci farklı konunun kaydını oynatmaz. API hesabı, anahtar ve uzak sunucu henüz sağlanmadığından gerçek AI veya ücretli ses üretimi yapılmadı.

Yanlış defterine Matematik ana ekranından veya test sonucundan girilir. Yalnız bitmiş yeni testlerin son cevapları dikkate alınır; soru kimliği/sürümü, konu, cevap ve çözüm saklanır. Öğrenci konuya dönebilir, alt konuya göre süzebilir veya eski soru sürümünü aynen yeniden çözebilir. Doğru çözüm sonrasında soru tekrar listesinden çıkar; boş bırakmak önceki yanlışı silmez. Değerlendirme testi bitmeden yeni cevaplar deftere eklenmez; yarım test varken ikinci test başlatılmaz. Eski demo toplamlarından soru geçmişi üretilmez.

Mevcut localStorage anahtarı ve müfredat sürümü değişmedi; önceki Temel Kavramlar tamamlama ve denemeleri korunur. İlerleme paydası 34 son konudur; sekiz hazır konu tamamlanırsa %24 gösterir. Sayılar ana ekranı ayrıca tamamlandı sayılmaz. Kalıcılık yalnız bu tarayıcı/cihaz içindir; üretim kullanıcı hesabı, PostgreSQL, senkronizasyon ve uzman onayı ayrı işlerdir.

Doğrulama: 40 JavaScript testi ve 18 API testi geçti. Yeni Sayılar/yanlış defteri tarayıcı testi dört grubu; Matematik testi sekiz, defter/servis testi altı, KPSS düzeyleri testi yedi grubu geçti. Yayın paketi telefon çerçevesi, içerik kimlikleri, seçim/tema kalıcılığı ve iframe/tek HTML arasında yarım test devamını doğruladı. Matematik kontrolü 100 test sorusu ve 17 ayrı örneğin cevaplarını denetledi. Türkçe ses ve AI yanıtlarında test taklitleri kullanıldı; gerçek sağlayıcı veya fiziksel Android/iOS testi yapılmadı.


## Renkli çalışma defteri, görünür menü ve AI/ses bağlantısı

15 Ekim 2026: Kullanıcının yeni görsel tercihine göre anlatım ve üç özet; el yazısı başlık/formüller, dört renkli not kartları, Kural/Aklında tut/Dikkat etiketleri, kapatıp hatırlama soruları ve açılabilir tam anlatımla düzenlendi. Düz metin tercihi ayrıca saklanır. Caveat'tan Türkçe karakterlerle alt kümelenen ve Akademi Notes olarak adlandırılan font uygulamaya gömülür; SIL OFL lisansı kaynaklarda ve üretilen CSS'te bulunur. Haricî font isteği gerekmez.

Yedi bölüm yatay kaydırma yerine iki sütunlu görünür menüdür. Bölüm seçimi içeriğe gider; yapışkan “Bölümler” bağlantısı menüye döner ve okuma konumu korunur. Yeni tasarım diğer konu başlıklarının hazırlanmış olduğunu göstermez.

Sesli özet için üç ayrı konuşma metni `temel-audio.json` içinde hazırlandı. Destekleyen cihazda Türkçe TTS, tarayıcıda duraklat/devam, hız ve gerçek okuma olaylarından ilerleme uygulanır. Native TTS'de desteklenmeyen duraklatma sunulmaz. Gerçek AI ses dosyası varsa HTML medya oynatıcısı süre/sarma ve hız kontrolünü kullanır; gerçek kayıt yokken sahte süre veya sarma yoktur.

`services/api` altında FastAPI metin/fotoğraf çözüm adaptörü, gerçek ses üretimi, davet oturumu, sınırlı kota, görsel doğrulama/metadata temizliği ve sayısal eşitlik kontrolü hazırlandı. İstemci yalnız genel `AKADEMI_API_URL` adresini bilir; OpenAI anahtarı sunucuda kalır. Kod ve Docker/Render kurulum tanımı hazırdır. **Sağlayıcı anahtarı ve kamuya açık API adresi tanımlı olmadığı için gerçek AI/üretilmiş ses canlıda etkin değildir.** Ödeme gerektiren çağrı yapılmadı. Ayrıntılı ve kullanıcıya uygun kurulum yolu `services/api/README.md` içindedir; GitHub Pages Python çalıştırmaz. Sunucunun yerel sağlık/anahtarsız yetenek uçları doğrulandı. Hesap/anahtar/sunucu ayarları ve gerçek sağlayıcı/cihaz testi dış ön koşuldur.

Doğrulama: 37 JavaScript motor/native/servis kontrolü ve temiz Python sanal ortamında 17 API testi geçti. Yeni tarayıcı kontrollerinde cihaz sesi ve uzak AI/medya test taklitleridir; gerçek ses kalitesi veya sağlayıcı başarısı sayılmaz. Mevcut ders/test/kayıt regresyonları ayrıca çalıştırılır. Kotalar ve oturumlar süreç belleğindedir; genel kullanıcı yayınına uygun kalıcı yetkilendirme/kota henüz eklenmedi.

## İlk Matematik çalışma paketi — uygulandı

15 Ekim 2026: KPSS Lisans Matematik için modüler içerik verisi, kalıcı deneme motoru, Matematik ana ekranı ve 39 ana/alt konuda açılabilen yedi sekmeli konu ekranı eklendi. Temel Kavramlar; dokuz bölümlü anlatım, üç özet, sekiz formül kartı, üç kolay/orta/zor çözümlü örnek, özgün ses metni ve 30 ayrı beş seçenekli test sorusu içerir. İçerikler matematiksel kontrolden geçti; uzman incelemesi bekleyen çalışma/demodur, onaylı soru bankası değildir. Diğer başlıklarda hazırlık durumu gösterilir; önceki denklem örneği ve diğer dersler korunur.

10/20/30, rastgele tek soru, son cevabı yanlış ve çözülmemiş filtreleri; yetersiz/boş havuz; öğrenme/değerlendirme modu; boş bırakma ve erken bitirme; sonuç/çözüm/kazanım analizi uygulandı. Soru sürümü ve cevap olayları `akademi_math_v1_kpss_lisans` içinde tek yerel kayıtta tutulur. Yenileme aynı soru sırası/cevaplarla devam eder. Önceki toplamlar korunur; eski sayaçlardan soru geçmişi uydurulmaz. Yeni cevaplar genel günlük/analiz ekranına eski sayaçları değiştirmeden eklenir. İstatistik sıfırlama yeni denemeleri de temizler, konu tamamlama ve tema korunur. Hesap/backend/cihazlar arası eşitleme yoktur; tarayıcı verisi silinirse ilerleme kaybolur.

Ders ilerlemesi öğrenci işaretlemesine dayanır ve 34 son düzey konu üzerinden hesaplanır: Temel Kavramlar tamamlanınca %3; başarı oranı ayrı hesaplanır. Son konu/sekme ve okuma konumu kaydedilir. Ses ve AI sekmeleri açık hazırlık durumudur; gerçek medya/AI servisi ve kullanılmayan sahte oynatıcı/sohbet kontrolü eklenmedi. Kaynak dağılım tabloları ve tutarsızlık uyarıları korunur.

Doğrulama: 30 test sorusu + 3 çözümlü örnek bağımsız Python hesaplarıyla kontrol edildi; 12 Matematik motoru ve 13 native mock testi geçti. Yerel Chromium'da sekiz yeni Matematik grubu, önceki dokuz ayar, 11 web ve yedi KPSS grubu; telefon önizlemesi ve tek HTML/export kontrolleri geçti. İki tema ve 320–768 piksel genişlikler kontrol edildi. Gerçek cihaz testi veya yeni Android/iOS paketi bu adımda yapılmadı. Yayın iş akışına içerik/motor kontrolleri eklendi; canlı yayın sonucu ayrıca doğrulanır.

## Matematik içerik ve ekran gereksinimleri — değerlendirme

15 Ekim 2026: Kullanıcının ayrıntılı anlatım, üç özet seviyesi, beş seçenekli çözümlü örnekler, altı test seçeneği, sesli anlatım ve yedi konu sekmesi talebi [MATH_REQUIREMENTS.md](MATH_REQUIREMENTS.md) içinde değerlendirildi. Mevcut kodla farklar, içerik alanları, ekran akışı, ilerleme hesabı, soru geçmişi, kalite kontrolleri ve uygulama sırası tanımlandı. Bu adım dokümantasyon değerlendirmesidir; yeni ekranlar, 10/20/30 testleri veya yeni içerikler uygulanmış sayılmaz.

Mevcut katalogda 17 ana konu ve 22 alt konu, toplam 39 içerik düğümü vardır. Test kapsamı için 34 son düzey konu bulunur. Her birinde 30 benzersiz soru gerekecekse en az 1.020 test sorusu hazırlanmalıdır. İlk uygulama hedefi ortak Matematik ekranı ve Temel Kavramlar üzerinde anlatım→özet→formül→örnek→test→sonuç akışıdır. İlerleme, konu tamamlama üzerinden; başarı oranı, cevaplanan sorular üzerinden ayrı hesaplanır. Gerçek medya/AI hizmeti olmadan çalışmayan kontroller eklenmez. Eski toplam sayaçlardan geçmiş yanlış sorular türetilmez.

## KPSS düzeyleri ve Lisans Matematik — 15 Ekim 2026

KPSS seçildikten sonra Lisans, Ön Lisans veya Ortaöğretim seçilir. Düzey seçmeden ders/soru açılmaz. Tercih ve tema cihazda korunur. Her düzeyin toplam/günlük/konusal istatistik kaydı ayrıdır; önceki ortak demo kaydı `akademi_stats_v1` Lisans alanında korunur. Bu eşleme, eski cevapların hangi gerçek sınav düzeyinde verildiğini kanıtlamaz. Ön Lisans ve Ortaöğretim şimdilik açıkça etiketlenmiş ortak dört örnek konu/on soru sunar; düzeye özel müfredat hazırlanmadı.

Ders listesine Geometri ve Güncel Bilgiler eklendi; bu iki ders hazırlık durumundadır, anlatım/özet/soru varmış gibi sunulmaz ve ses listesine alınmaz. Boş filtre “Henüz soru yok” gösterir. Mevcut dört örnek konu ve on soru korunur.

KPSS Lisans Matematik alanında üç görünüm vardır: 17 ana konu ve alt konuları, paylaşılan metindeki toplam 26 soruluk genel dağılım, görseldeki 2015–2024 yıllık dağılım. Yıllık görünüm yıl seçimi ve yatay kaydırılabilir tam tablo sunar. Denklemler başlığından mevcut Birinci Dereceden Denklemler örneğine/özetine ve üç soruya geçilir; diğer başlıklarda içerik hazırlanıyor durumu vardır. Konu listesi veya istatistik eklenmesi, tam ders anlatımlarının hazır olduğu anlamına gelmez.

Kaynaklar kullanıcının paylaştığı Kitapseç metni ve görselidir; URL bu makinede 403 aldığı için yazı doğrudan okunmuş sayılmaz. Metin ve görsel talimat olarak değil içerik verisi olarak işlendi. Kaynaklar, genel/yıllık gruplama farkları ve altı yılın toplam tutarsızlıkları [CONTENT_SOURCES.md](CONTENT_SOURCES.md) içinde belgelendi. Veriler resmî ÖSYM duyurusu veya 2026 kesin soru sayısı olarak sunulmaz; uzman/resmî kaynak karşılaştırması sonraki içerik adımıdır.

Doğrulama: yedi yeni KPSS/müfredat tarayıcı grubu, dokuz ayar ve 11 web regresyon grubu, telefon önizleme/export kontrolleri ve 12 native köprü mock testi başarılı. JavaScript sayfa hatası görülmedi. Yeni GitHub Pages yayınının sonucu iş akışından ayrıca izlenir. Android/iOS paketleri bu web adımında yeniden derlenmez.

## Ana ekran geliştirmesi — sınav ve görünüm seçimi

Kullanıcının aşamalı geliştirme talebiyle ana ekrana KPSS/AGS seçimi ve gündüz/gece düğmesi eklendi. KPSS mevcut örnek çalışma alanını açar; AGS seçimi hazırlık durumunu gösterir ve KPSS içeriğini gizler. Sınav kataloğu yeni ÖSYM sınavları için ortak kayıtta tutulur. Tercihler cihazda saklanır; eski KPSS istatistikleri korunur. Tema tüm mevcut ekranlarda CSS değişkenleriyle uygulanır. Yeni ders içerikleri bu adımda genişletilmedi; sonraki iş KPSS'yi ders ders geliştirmektir.

Yerel tarayıcı doğrulaması: dokuz yeni ayar grubu; mevcut 11 web regresyon grubu; telefon çerçevesi ve export; 12 native köprü mock testi başarılı. Android/iOS paketleri bu değişikliklerle yeniden hazırlanmadı. GitHub Pages yayın kontrolü yeni ana ekran ve sınav seçimi betiğini de doğrulayacak şekilde güncellendi.

## Canlı mobil web önizlemesi

15 Ekim 2026: Kullanıcının GitHub Pages ayarından sonra 38692055701 numaralı yayın başarıyla tamamlandı. Mobil önizleme **https://muharremceylan.github.io/Miko/** adresindedir. GitHub çalıştırıcısındaki yayın kontrolü önizleme ana sayfası, app.html ve preview.js için HTTP 200 ve beklenen içeriği doğruladı. Uygulama akışları yerel Chromium'da önceden test edilmiştir; bu bulut makinesindeki ağ kısıtı nedeniyle canlı adreste uzaktan tarayıcı testi yapılmadı. İlk başarısız yayın ve ağ engeli aşağıdaki tarihsel notlarda korunur; Pages'i tekrar etkinleştirme gerekmiyor.

## Güncel öncelik — web üzerinde telefon görünümü

Kullanıcının yeni tercihi önce web üzerinden mobil ekranı görerek geliştirmek, Android/iOS paketlerini sonra hazırlamaktır. `apps/capacitor/src/preview.html` ve `preview.js` ile etkileşimli telefon çerçevesi, üç ekran boyutu, 1:1/sığdırma ve uygulamayı ayrı sekmede açma eklendi. `npm start` ile yerel sunucu başlatıldı; iframe içinde ders/soru, boyut geçişi ve mevcut 11 regresyon grubu doğrulandı. Statik yayın paketi ve tek dosyalık sürüm HTTP üzerinden kontrol edildi. file:// açılışı bu bulut tarayıcısının yönetici politikası nedeniyle doğrulanamadı.

GitHub hesabı/depo `muharremceylan/Miko` olarak belirlendi; alan adı satın alma gerekmez. GitHub Pages iş akışı hazırlandı ancak uzak depoya yükleme, Pages ayarları ve gerçek HTTPS yayın henüz doğrulanmadı. Git okuma erişimi var; GitHub ayar API'si ağ politikasından 403 alıyor. `api.github.com` ve `muharremceylan.github.io` izinleri ortam taslağına eklendi; ayarlarda uygulanması bekleniyor. Parola/token sohbetten istenmez. Ayrıntılar `apps/capacitor/WEB_PREVIEW.md` içinde; hazır APK önceki sürüme aittir, bu web önizleme güncellemesi için tekrar derlenmedi.

## Aktif mobil yol — v0.4 Capacitor (15 Ekim 2026)

Kullanıcının Flutter kullanmama talebiyle aktif uygulama `../apps/capacitor` altında Capacitor 8 + HTML/CSS/JavaScript olarak kuruldu. Düzeltmeleri yapılmış HTML kaynak olarak korunuyor; build scripti onu mobil pakete kopyalıyor. Flutter denemesi tarihsel kaynak olarak duruyor ve aktif kurulumda kullanılmıyor. Flutter indirme ağ izni bu yol için ön koşul değildir.

Android hostu, iOS Xcode/SPM hostu, yerel kamera/galeri, cihaz TTS, Android geri tuşu ve güvenli alan katmanı oluşturuldu. Tarayıcıda 11 regresyon grubu ve 24 px güvenli alan kontrolü; native API'leri taklit eden 11 köprü testi geçti. Gerçek kamera/TTS ve Android/iOS cihaz davranışı henüz doğrulanmadı. Android debug APK başarıyla üretildi (187 derleme görevi); v2 imzası ve dört paketlenmiş web varlığının eşleşmesi doğrulandı. Cihazda açılış testi henüz yapılmadı. APK derleme sonucu ve komutları `../apps/capacitor/README.md` içindedir.

Görsel çizgi: lacivert gradyan üst alan, beyaz yuvarlak kartlar, indigo vurgu; alt menü Ana sayfa/Dersler/Sorular/Dinle/Analiz. Telefon boyutunda gerçek web arayüzü görüntüleri `/workspace/outputs/akademi-ai-ana-sayfa.png`, `akademi-ai-ders.png` ve `akademi-ai-test.png` olarak hazırlandı. Bunlar cihaz/emülatör görüntüsü değildir; ana ekrandaki üç cevap test verisidir.

Bu sürüm orijinal dört ders/on soru havuzuna dayanır. Flutter denemesinde yazılan fakat çalıştırılmayan yanlış defteri, bu Capacitor sürümüne aktarılmış sayılmaz. Yanlış defteri, koç, gerçek AI ve backend sonraki geliştirmelerdir. FastAPI/PostgreSQL ve sunucuda AI hedefi korunur; mobil istemci API sözleşmesi Capacitor'a göre uygulanacaktır.

## Mobil geliştirme başladı — v0.3 kaynak aşaması

Kullanıcının mobil uygulamaya geçiş talebiyle `../apps/mobile` altında Flutter kaynakları, yerel veri arayüzü ve 14 test hazırlandı. Ana sayfa, ders/özet, test/sonuç, analiz, yanlış defteri, ses ve açıkça etiketli fotoğraf demosu kaynakları oluşturuldu. HTML sürümü korunuyor.

Flutter stable 3.47.7 kaynak SDK'sı ve Android SDK 36/build-tools kuruldu. Dart/engine indirmesi `storage.googleapis.com` için ağ politikasından 403 aldı; gerekli ağ eklemesi ortam taslağına kaydedildi. Android/iOS host oluşturma, Flutter analiz/test ve APK derleme henüz yürütülmedi. Hazır veya cihazda çalışır mobil uygulama iddiası yapılmaz. Ağ erişimi açılınca `scripts/setup_mobile.sh` ve `scripts/prepare_mobile.sh` ile bu adımlar tamamlanacak. Ayrıntılı durum `../apps/mobile/README.md` içindedir.

## Son geliştirme durumu — v0.2

Kullanıcının inceleme sonrası düzeltme talebiyle HTML üzerinde sınırlı değişiklikler yapıldı. Aşağıdaki ilk inceleme bulguları tarihsel rapordur; güncel durum şudur:

- Günlük sayaçlar cihazın yerel tarihine göre ayrı tutuluyor; analiz toplamları korunuyor. 10 ve üzeri cevapta hedef çubuğu %100 kalıyor.
- JSON/şema ve depolama erişim hataları yönetiliyor; eski biçimdeki toplamlar taşınıyor. Eski kayıtlarda tarih olmadığı için geçmiş cevaplar bugüne yazılmıyor. Bozuk kayıt açılışta değiştirilmez; yeni cevap/sıfırlama sağlıklı kayıt oluşturur.
- Fisher–Yates karıştırma ve sonlu test oturumu eklendi. Havuz bitince doğru/yanlış/yüzde sonuç ekranı açılıyor; çift cevap veya bitmiş oturumda cevap kaydı engelleniyor.
- Havuzda olmayan “5 yeni soru” önerisi kaldırıldı. Yeni testin aynı örnek havuzdan hazırlandığı açıkça yazıyor.
- JPEG/PNG/WebP, 10 MB sınırı, bozuk görsel hatası ve object URL temizliği eklendi. Bu kontroller ilerideki sunucu tarafı yükleme doğrulamasının yerini tutmaz.
- Ses ekranından ayrılınca oynatma duruyor; iptal edilen sesin geç gelen olayları durum mesajını değiştirmiyor. Türkçe ses varsa seçiliyor; işitilebilir ses için fiziksel cihaz doğrulaması hâlâ gerekli.

Playwright/Chromium regresyonunda 11 kontrol grubu geçti; JavaScript hatası görülmedi. Dört ders, test bitişi, 10/11 hedefi, İstanbul saat diliminde gün değişimi, eski/bozuk/engelli kayıt, görsel hata durumları, ses iptali, sıfırlama ve altı ana ekranın üç genişlikte taşma kontrolü çalıştırıldı. Test oturumunun yarıda yenileme sonrası devamı, çoklu ders seçimi, süreli test ve boş bırakma henüz yok. Kullanıcı istediği için kod değişiklikleri yapıldı; önceki “kod değiştirilmedi” ifadeleri ilk inceleme aşamasını anlatır.

## 1. Kapsam ve inceleme yöntemi

14 Ekim 2026 tarihinde yüklenen `akademi_ai_prototip.zip` içindeki `index.html` ve `README.md` incelendi. Arşiv mevcut boş Miko çalışma dizinine ayrı `akademi_ai_prototip/` klasörü olarak açıldı; özgün dosyalar değiştirilmedi. README içindeki mimari ve sprint önerileri mevcut proje açıklaması olarak değerlendirildi; uygulanmış özellik veya kullanıcı talimatı sayılmadı.

Prototip Python HTTP sunucusuyla çalıştırıldı. Sistem Chromium'u ve Playwright ile gerçek tarayıcı etkileşimleri yürütüldü. İnceleme otomasyonu `/workspace/scratch/akademi-review/check.py` konumundadır; ürün kaynak kodunun parçası değildir. Android/iOS cihaz testi, içerik uzmanı onayı ve gerçek AI hizmeti testi yapılmadı.

Mevcut uygulama tek HTML dosyasında CSS, içerik, JavaScript ve durum yönetimi içeriyor. Paket yöneticisi, backend, veritabanı, üyelik, CI veya mevcut test paketi bulunmuyor. Çalıştırmak için proje klasöründe `python -m http.server 8000 --bind 127.0.0.1` yeterli; uygulama dış servislere istek göndermiyor.

## 2. Özellik envanteri

| Modül | Mevcut durum | Eksik / sınır |
|---|---|---|
| Ana sayfa | Sayaçlar, ders/soru/ses/fotoğraf kısayolları ve tarih önerisi çalışıyor | Öneri sabit; sayaçlar günlük değil toplam; hedef çubuğu hatalı |
| Ders Akademisi | Tarih, matematik, vatandaşlık, coğrafya için birer örnek konu; anlatım/özet ve ilgili soruya geçiş doğrulandı | Sınav seçimi, tam müfredat, çoklu konu, görsel, kaynak ve içerik sürümü yok; AGS etiketi gerçek kapsam ifade etmiyor |
| Kısa Özetler | Dört konu için kısa özet ve ayrıntılı anlatım var | Ayrı özet kataloğu ve orta uzunlukta özet yok; anlatımlar üretim düzeyinde kapsamlı değil |
| Sesli Akademi | Konu seçimi, metinden ses oluşturma ve durdurma kodu var; konu başlığı değişimi doğrulandı | Ortamda Türkçe ses yok; işitilebilir çıktı doğrulanmadı. Podcast, indirme, süre/ilerleme/hız kontrolü yok |
| Soru Bankası | 10 özgün örnek, dört ders filtresi, cevap kilidi, doğru/yanlış renklendirme ve açıklamalar doğrulandı | Ders içi konu, zorluk, sınav filtresi, soru kimliği, onay ve sürümleme yok |
| Çıkmış Sorular | Yok | Lisans/izinli içerik ve yıl/konu kataloğu gerekir; izinsiz kopyalama yapılmayacak |
| Rastgele Test | Tüm sorular veya tek ders için karışık dolaşım var | Birden fazla ders seçimi, süre, soru sayısı, bitiş ve sonuç ekranı yok; havuz döngüsel tekrar ediyor |
| Fotoğraftan AI Çözümü | Görsel seçme ve önizleme doğrulandı; sabit denklem çözümü demo olarak açıkça belirtiliyor | OCR, yükleme API'si, görsel analizi, doğrulanmış çözüm, şekil/formül üretimi yok; mobil kamera davranışı cihazda denenmedi |
| Yapay Zekâ Öğretmen | Yok | Sohbet, ipucu, alternatif yöntem, geçmiş ve doğrulama gerekir |
| Yanlış Defteri | Yok | Yanlış sorular tutulmuyor; yalnızca ders bazlı toplam sayaçlar saklanıyor |
| Kişisel Çalışma Koçu | En düşük ders doğruluğuna göre basit tekrar önerisi var | Sınav tarihi, süre uygunluğu, günlük görevler, tekrar aralığı ve uyarlama yok; öneri AI değil |
| Başarı Analizi | Toplam doğru/yanlış, ders doğruluğu, yenileme sonrası kalıcılık ve sıfırlama doğrulandı | Net, boş, süre, günlük seri, konu düzeyi ve gelişim eğrisi yok |
| Yönetim Paneli | Yok | Rol yetkileri, inceleme, yayın ve denetim kaydı gerekir |

## 3. Doğrulama sonuçları ve kusurlar

### Başarılı kontroller

- Dört dersin detaylı anlatımı, kısa özeti ve ilgili ders soru filtresine geçişi.
- On örnek sorunun cevaplanması; 5 doğru, 5 yanlış, toplam 10 cevap ve ders dağılımlarının analizde görünmesi. Cevaptan sonra dört seçenek de kilitleniyor ve açıklama gösteriliyor.
- İstatistiklerin sayfa yenilemesinden sonra korunması; onaylı sıfırlamada tüm sayaçların temizlenmesi.
- Görsel dosyasının yüklenip tarayıcıda çözülmesi ve sabit örnek çözüm ekranının açılması.
- Ses konusu değişimi ve seslendirme başarısızlığı mesajı.
- İncelenen ekran durumunda 320, 390 ve 768 piksel genişliklerde yatay taşma görülmemesi. Bu kontrol tüm ekran/cihaz kombinasyonları için erişilebilirlik veya mobil uygunluk onayı değildir.
- Normal akışlarda JavaScript çalışma zamanı hatası görülmedi.

### Doğrulanmış hatalar

1. **Günlük hedef yanlış hesaplanıyor:** `drawHome()` içinde `stats.solved % 10` kullanılıyor; 10 cevapta çubuk `%0` oldu. Hedef tamamlanınca dolu kalmalı; günlük sayaç tarih ve kullanıcı saat dilimiyle hesaplanmalı.
2. **Bozuk kayıt açılışı durduruyor:** `akademi_stats_v1` geçersiz JSON olduğunda korunmasız `JSON.parse` hata verdi ve başlangıç kodu kesildi. Güvenli ayrıştırma, şema kontrolü ve kurtarma gerekir.

### Kod incelemesiyle belirlenen sınırlamalar / riskler

- “Bugünkü ilerlemen” toplam cihaz sayacını gösteriyor; günlük yenilenme yok. “Hazırsın” etiketi sabit.
- `shuffle()` rastgele karşılaştırmalı `sort` kullanıyor; dengeli karıştırma garantisi yok. Fisher–Yates tercih edilmeli.
- Test havuzu sona erince bitmiyor; aynı sorular yeni cevap olarak tekrar sayılıyor. Oturum ve benzersiz soru/cevap kayıtları yok.
- “5 yeni soru” önerisi bazı derslerde yalnızca 2–3 soruluk havuz bulunduğunu hesaba katmıyor.
- localStorage yazma/okuma engeli ve kota hataları yönetilmiyor; kayıt yapısı doğrulanmıyor. Sunucu güvenilirliği ve çok cihaz senkronizasyonu yok.
- Görsel boyutu/türü uygulama tarafından doğrulanmıyor; eski object URL'leri serbest bırakılmıyor. `accept` seçici ipucu güvenlik doğrulaması değildir.
- Ses üretimi cihaz bağımlı; sekme değişiminde devam edebilir. Türkçe ses seçimi, kullanım durumu ve erişilebilir alternatif gerekir.
- Bazı içerikler `innerHTML` ile yerleştiriliyor. Şimdiki kaynaklar sabit; ileride editör/AI içeriği güvenli biçimde temizlenmeli. Bu bulgu tek başına mevcut dış kaynaklı XSS açığı kanıtı değildir.
- API anahtarı ve sunucu entegrasyonu yok; gerçek AI sonucu iddiası yapılmıyor. Sabit çözüm fotoğraf seçilmeden de açılabiliyor; demo için anlamlı, gerçek çözüm için ayrı giriş koşulu gerekir.
- Soru ve anlatımlar uzman tarafından doğrulanmış sayılmaz. Özellikle mevzuat ve sınav kapsamı resmî güncel kaynaklarla kontrol edilmeli.

Bu kusurlar raporlandı; ilk görev kapsamı gereği uygulama kodu düzeltilmedi.

## 4. Teknik mimari önerisi

### Mobil: Flutter

Flutter, Android/iOS için ortak Türkçe arayüz, kamera, yerel veri, ses oynatma ve çevrimdışı kullanım nedeniyle uygun adaydır. HTML doğrudan Flutter'a dönüşmez; tasarım ve kullanıcı akışları referans alınarak ekranlar modüler taşınır. Mevcut prototip korunur. Riverpod gibi bir durum yönetimi, go_router ile gezinme ve typed API istemcisi değerlendirilebilir; seçim küçük bir dikey dilimde doğrulanır. Formül için KaTeX/LaTeX uyumlu güvenli renderer ve şekil için izinli SVG/çizim şeması prototipi gerekir; AI'nin keyfi HTML/JavaScript'i render edilmez.

Riskler: Türkçe TTS kalitesi cihazlar arasında değişir; kamera izinleri, ses oturumu ve offline senkronizasyon fiziksel cihazlarda doğrulanmalıdır. Android geliştirme Linux ortamında yapılabilir; iOS derleme, imzalama ve mağaza yayını için macOS/Xcode ve geliştirici hesabı gerekir. WebView ile ambalajlama yalnızca geçici demo seçeneği; nihai mobil mimari önerisi Flutter'dır.

### Backend: FastAPI + PostgreSQL

Başlangıçta modüler monolit yeterli. FastAPI, Pydantic şemaları, SQLAlchemy ve Alembic ile PostgreSQL üzerinde işlem bütünlüğü sağlanır. İçerik, soru oturumu, ilerleme, koç, AI ve yönetim modülleri açık sınırlarla ayrılır. Gerektiğinde Redis ve ayrı işçi süreci uzun AI/podcast işlerini yürütür; bunlar ilk ders/soru dikey diliminin zorunlu bileşeni değildir. Medya özel S3 uyumlu depoda; erişim kısa ömürlü imzalı URL ile sağlanır.

Mobil istemci → HTTPS API → PostgreSQL / özel medya deposu. AI işleri API → kuyruk/işçi → sunucudaki sağlayıcı adaptörü üzerinden yürür. İstemciye AI sağlayıcı anahtarı konulmaz. Sağlayıcı seçimi kalite, Türkçe matematik/görsel başarısı, maliyet ve veri işleme koşulları pilotuyla yapılır.

Yönetim paneli ayrı web istemcisidir; API'nin editör/uzman/yönetici izinlerini kullanır. İnceleme ve yayın yetkileri ayrılır. Başlangıçta mikroservis zorunluluğu yoktur.

### Veri modeli ve API sınırları

- Müfredat: `exam`, `subject`, `exam_subject`, `topic`, `exam_topic`, `lesson`, `lesson_revision`, `summary_revision`. İçerik kaynağı, son kontrol tarihi ve taslak/onaylı/yayınlı/arşiv durumu tutulur.
- Sorular: `question`, `question_revision`, `answer_choice`, `question_source`, `content_review`. Sınav/konu/zorluk etiketleri, lisans/izin, çözüm ve yayın sürümü gerekir.
- Kullanıcı: `user`, `profile`, `exam_goal`, `consent`, `device`, `study_session`.
- Çalışma: `test_session`, `test_item`, `attempt`, `wrong_entry`, `review_schedule`, `study_plan`, `study_task`, `daily_progress`. Denemeler belirli soru sürümüne bağlanır; yinelenen gönderimler idempotency anahtarıyla engellenir. Atlanan soru ve süre ayrı tutulur.
- Medya/AI: `audio_asset`, `upload`, `ai_job`, `ai_solution`, `chat_session`, `chat_message`, `validation_result`. Saklama süresi, kaynak, model/prompt sürümü ve doğrulama durumu kaydedilir.
- Yönetim: `role`, `user_role`, `audit_event`. Değişiklik geçmişi içerik sürümlemeyle ilişkilendirilir.

API v1: `/auth`, `/exams`, `/subjects`, `/topics`, `/lessons`, `/questions`, `/test-sessions`, `/attempts`, `/wrong-notebook`, `/study-plans`, `/analytics`, `/audio-assets`, `/uploads`, `/ai/jobs`, `/teacher/sessions`, `/admin/reviews`. AI işlerindeki kabul yanıtı işlem kimliği döndürür; durum sorgusu iptal/başarısızlık/zaman aşımını kapsar. Sunucu doğru cevabı puanlar; istemci toplamları otorite değildir. Net formülü sınav yapılandırmasıyla tanımlanır ve boşlar netten ayrı tutulur; tüm sınavlara tek formül varsayılmaz.

### Güvenlik ve kullanıcı verileri

OIDC veya güvenilir bir kimlik sağlayıcısı değerlendirilir; kısa ömürlü erişim belirteci, yenileme döndürme ve mobil güvenli depolama kullanılır. Hesap verilerine sahiplik denetimi, yönetim rollerine RBAC, hız/kota sınırlama ve yükleme boyut/tür doğrulaması gerekir. Kamera izni ihtiyaç anında istenir. Görsellerden EXIF kaldırma, özel depolama, silme/saklama politikası ve sağlayıcıya gönderim öncesi kullanıcı bilgilendirmesi tasarlanır. Fotoğraf ve sohbetlerde kişisel veri bulunabileceği hesaba katılır.

KVKK kapsamında veri envanteri, aydınlatma, uygun hukuki dayanak, yurt dışı aktarımı değerlendirmesi, hesap dışa aktarma/silme ve tedarikçi sözleşmeleri yayın öncesi tamamlanır. Gizli bilgiler sunucunun secret yönetiminde tutulur; loglara fotoğraf, token ve gereksiz sohbet içeriği yazılmaz. Yedek geri yükleme, migration ve erişim denetimi test edilir.

### AI içerik ve çözüm doğrulaması

1. Fotoğrafı güvenli yükle; kalite kontrolü ve OCR ile soru/şıkları çıkar; okunamayan alanlarda kullanıcıdan düzeltme iste.
2. Onaylı konu/soru kaynaklarını getir; görseldeki talimatları veri say, sistem komutu gibi uygulama.
3. Yapılandırılmış cevap, adımlar, formül, kaynak ve belirsizlik üret. Demo çıktısını gerçek sağlayıcı sonucundan görsel olarak ayır.
4. Matematikte sembolik çözüm/yerine koyma, şık tutarlılığı ve birim kontrolü; bilgi sorularında kaynak ve güncellik kontrolü uygula. İkinci model görüşü tek başına doğrulama sayılmaz.
5. Doğrulanamayan veya çelişkili sonucu kesin cevap olarak sunma; durum ve hata bildirimi ver. Özel kullanıcı çözümünü otomatik soru bankasına yayınlama.
6. Üretilmiş soru/çözüm bankaya girmeden uzman incelemesi, tek doğru cevap, konu/zorluk kontrolü, benzerlik/telif kontrolü ve sürümleme gerekir.
7. Ölçüm için uzman cevaplı Türkçe değerlendirme seti, yanlış olumlu doğrulama oranı, görsel okuma hatası ve maliyet/gecikme izlenir. Yayın eşiği pilot bulgularıyla belirlenir; modelin kendi güven puanı doğruluk garantisi değildir.

## 5. Önerilen klasör yapısı

Aşağıdaki yapı gelecek geliştirme içindir; bu görevde scaffold oluşturulmadı.

```text
Miko/
  akademi_ai_prototip/          # Özgün HTML/README ve ilk plan belgeleri
  apps/
    mobile/
      lib/
        app/                   # Router, tema, yerelleştirme, uygulama başlangıcı
        core/                  # API, hata, güvenli depolama, ortak bileşenler
        features/
          onboarding/ auth/ home/ lessons/ summaries/ audio/
          question_bank/ past_questions/ tests/ photo_solver/
          ai_teacher/ wrong_notebook/ coach/ analytics/ settings/
      test/ integration_test/
    admin/                     # İçerik ve inceleme web arayüzü
  services/
    api/
      app/
        core/ db/ modules/     # Ayarlar, auth, model ve alan modülleri
        integrations/          # AI sağlayıcıları, depolama, kimlik
      migrations/ tests/
    worker/                    # Gerektiğinde AI/ses işleri
  packages/
    api_contracts/             # OpenAPI kaynaklı istemci sözleşmeleri
    content_schemas/           # İçerik, çözüm ve çizim şemaları
  content/
    samples/                   # Onaylanmamış örnekler açık etiketle
    reviewed/                  # Kaynak/lisans kayıtlı yayın içerikleri
  infra/                       # Yerel servisler, CI ve dağıtım tanımları
  docs/                        # Mimari kararlar, ekranlar, veri/AI politikaları
```

## 6. Ekranlar ve kullanıcı akışları

Ana alt gezinme: **Ana Sayfa, Akademi, Testler, Koç, Profil**. Sesli çalışma, yanlış defteri ve AI araçları ilgili ana sayfalardan ve kısayollardan erişilebilir. Yönetim ayrı web arayüzündedir. Aşağıdaki liste planlanan kapsamdır; mevcut HTML'de uygulandığı anlamına gelmez.

| Alan | Ekranlar | Temel akış ve özel durumlar |
|---|---|---|
| Başlangıç | Karşılama, sınav seçimi, hedef tarihi, günlük süre, seviye değerlendirmesi | Misafir deneme veya hesap; sınav kapsamını seç → hedef belirle → ana sayfa. Kapsam/tarih değiştirilebilir |
| Hesap | Giriş, kayıt, doğrulama, şifre kurtarma | Seçilen kimlik yöntemine göre doğrula → devam et; iptal, geçersiz giriş ve oturum süresi dolması |
| Ana sayfa | Günlük plan, ilerleme, devam et, araç kısayolları | Yarım kalan ders/teste dönüş; henüz veri yoksa başlangıç yönlendirmesi |
| Akademi | Sınav/ders listesi, konu listesi, konu detayı, kaynak/güncellik | Ders → konu → anlatım/örnek/görsel → özet/ses/ilgili sorular; kilitli veya yayınlanmamış içerik durumu |
| Özetler | Katalog, kısa/orta/ayrıntılı özet, favoriler | Konu → uzunluk seç → oku/dinle/tekrar listesine ekle |
| Sesli Akademi | Katalog, bölüm detayı, oynatıcı, indirmeler | Bölüm → oynat → duraklat/hız/konum → devam; indirme/silme ve çevrimdışı hata |
| Soru Bankası | Filtreler, soru, açıklama/kaynak, hata bildirimi | Sınav/ders/konu/zorluk → soru → cevap → açıklama → yanlış defteri/konu |
| Çıkmış Sorular | Lisans açıklaması, yıl/sınav/konu seçimi, soru/çözüm veya resmî kaynak bağlantısı | Yalnızca izinli içerik; izin yoksa erişim bağlantısı, kopyalanmış soru sunulmaz |
| Rastgele Test | Çoklu ders/sayı/süre ayarı, test, bitirme onayı, sonuç, cevap incelemesi | Uygun havuzu göster → başlat → cevapla/boş bırak → süre biter/bitir → net/doğruluk/süre → yanlışları tekrar et. Yarım oturum kurtarma |
| Fotoğraf Çözümü | Kamera izin açıklaması, çek/yükle, kırp/kalite, OCR kontrol, işlem durumu, adımlı çözüm | Görsel → okunan metni doğrula → AI işi → doğrulama durumu/formül/şekil → geri bildirim/sil. İzin reddi, okunamama, kota, zaman aşımı ve iptal |
| AI Öğretmen | Konu seçimi, sohbet, ipucu/alternatif yöntem, geçmiş | Konu/soru bağlamı → mesaj → kaynaklı yanıt → takip sorusu; doğrulanamama, uygunsuz içerik ve bağlantı hatası |
| Yanlış Defteri | Ders/konu filtreli liste, soru detayı, tekrar testi, tekrar takvimi | Yanlış cevap → sürümüyle kaydet → açıklama/konu → yeniden çöz → tekrar planını güncelle |
| Çalışma Koçu | Hedef düzenleme, günlük/haftalık plan, görev, yeniden planlama | Hedef+uygun süre+performans → plan → tamamla/ertele → kalan işleri uyarla. Veri yoksa açık kural tabanlı başlangıç planı |
| Analiz | Genel, ders, konu, zaman aralığı, oturum detayı | Net/doğruluk/boş/süre → zayıf konu → ders/tekrar. Veri yetersizken kesin öneri üretme |
| Profil/Ayarlar | Hedef, erişilebilirlik, ses, bildirim, offline/senkronizasyon, gizlilik, veri dışa aktarma, hesap silme, yardım | İzinleri yönet → veriyi yönet; hesap silmede onay ve iş durumu |
| Yönetim | Giriş, içerik listesi/editörü, soru/çözüm editörü, kaynak/izin kaydı, podcast varlığı, AI üretim taslakları, inceleme kuyruğu, yayın geçmişi, kullanıcı rolü, raporlar | Taslak → otomatik kontrol → uzman inceleme → onay/yayın veya gerekçeli ret; yayın geri alma ve denetim izi |

Ortak durumlar: yükleniyor, boş içerik, bağlantı kesildi, yeniden dene, erişim reddi, hesap oturumu yenileme, sürüm uyuşmazlığı ve işlem iptali. Türkçe karakterler, ekran okuyucu etiketleri, metin büyütme, kontrast ve dokunma hedefleri ekran kabul kriteridir. Fotoğraf/AI kotası ve sonuç kaynağı açık gösterilir.

## 7. Aşamalı geliştirme ve yayın sınırı

1. **Prototip sağlamlaştırma:** doğrulanmış sayaç/kayıt hataları, oturum sınırı ve erişilebilirlik; yalnızca ayrı kodlama göreviyle. Ürün kapsamı ve sınav müfredatı resmî kaynaklarla kesinleştirilir.
2. **MVP dikey dilim:** Flutter sınav/ders/konu/özet ekranları + FastAPI/PostgreSQL + onaylı sorular + test oturumu/sonuç + yanlış defteri + temel analiz + asgari editör onay paneli. Misafir/hızlı hesap modeli ve senkronizasyon kararı bu aşamada verilir.
3. **Çalışma alışkanlığı:** kural tabanlı koç, tekrar programı, TTS/izinli ses dosyaları, güvenilir offline önbellek. Gerçek podcast, izinli çıkmış sorular ve geniş müfredat içerik kapasitesine bağlıdır.
4. **Doğrulanmış AI pilotu:** önce fotoğraf/OCR ve kontrollü çözüm; ardından bağlamlı öğretmen. Sağlayıcı anahtarları ve kalite testleri tamamlanmadan gerçek AI özelliği olarak yayınlanmaz.
5. **Mobil pilot ve yayın:** README'deki 15–30 kişilik pilot önerisi uygulanabilir başlangıçtır. Android/iOS fiziksel cihazlarda kullanılabilirlik, ekran okuyucu, Türkçe ses, kamera, bağlantı kesilmesi ve performans ölçülür. Gizlilik/izinler, lisanslar, yedekleme, mağaza koşulları ve imzalama tamamlanır.

Takvim ve maliyet ekip kapasitesi, içerik kapsamı, AI sağlayıcısı ve platform hesapları belirlendikten sonra tahmin edilir. On iki modül nihai yol haritasında tutulur; tamamı ilk MVP'ye sıkıştırılmaz. Ayrıntılı görevler `TASKS.md` içindedir.

## 8. Hazır olma ölçütleri ve mevcut sınırlar

Şu anda yalnızca HTML demo akışları yukarıdaki kontrollerle doğrulanmıştır. Çalışan backend, PostgreSQL, Flutter projesi, Android/iOS paketi veya gerçek AI entegrasyonu yoktur. Çalışır mobil ürün iddiası yapılmaz.

MVP: onaylı içerik uçtan uca okunmalı, cevap sunucuda değerlendirilip tekil kaydedilmeli, yanlış defteri ve analiz aynı veriyi göstermeli, sahiplik/rol erişimleri engellenmeli ve cihazlar arası senkronizasyon seçilen kapsamda test edilmelidir. AI sürümü ayrıca uzman değerlendirme seti ve doğrulanamayan cevap akışını geçmelidir. İzinli içerik ve veri politikaları yayın ön koşuludur.
