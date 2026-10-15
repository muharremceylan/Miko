# Akademi AI — soru çözümü ve sesli özet sunucusu

Bu servis, istemciye anahtar koymadan OpenAI Responses üzerinden metin/fotoğraf sorusu çözmeye ve Speech üzerinden gerçek ses dosyası üretmeye hazırlanmıştır. Web arayüzü davet oturumu, görsel yükleme, adımlar/doğrulama durumu ve gerçek ses oynatıcısıyla bağlanabilir. **Bu depodaki kodun bulunması AI hizmetinin canlı olduğu anlamına gelmez.** Şu an sağlayıcı anahtarı ve yayımlanmış API adresi tanımlı değildir; ücretli sağlayıcıya gerçek çağrı yapılmadı.

## Şimdi çalışan ve kurulum isteyen parçalar

- Renkli defter, görünür bölüm menüsü ve mevcut ders/test akışları GitHub Pages üzerinden çalışır.
- Türkçe ses motoru olan cihazda “Cihaz sesiyle dinle” çalışabilir. Bu bir ses dosyası veya podcast kaydı değildir. Türkçe ses bulunmazsa nedenini gösterir; oynatma düğmeleri görünmez. Tarayıcıda duraklat/devam desteklenir; mevcut native TTS motorunda durdur/yeniden başlat kullanılır.
- Gerçek AI çözümü ve üretilmiş ses dosyası için API hesabı ve HTTPS sunucu gerekir. GitHub Pages Python sunucusu çalıştırmaz.
- OpenAI API kullanımı ayrı hesaba/bakiyeye bağlıdır; ChatGPT aboneliği API kullanımını kapsamaz. Model erişimi ve ücretler hesabın güncel koşullarından kontrol edilmelidir. Varsayılan modeller değiştirilebilir.

## En kolay yayın yolu — Render ve GitHub

1. OpenAI API hesabında kullanıma açık proje/anahtar ve bütçe takibini hazırla. **Anahtarı sohbete, HTML/JavaScript'e veya GitHub deposuna yazma.**
2. Render hesabında **New → Blueprint** üzerinden `muharremceylan/Miko` deposunu seç. Kök dizindeki `render.yaml`, Docker tabanlı `akademi-ai-api` servisini tanımlar. Plan kullanılabilirliğini ve fiyatını Render ekranında kontrol et; dosyada free plan istenir. Dosya bu geliştirme sırasında kendiliğinden hizmet açmadı.
3. Render'ın güvenli ortam alanlarına `OPENAI_API_KEY` ve en az 12 karakterlik güçlü bir `AKADEMI_ACCESS_CODE` gir. İkincisi ilk pilotun davet kodudur; OpenAI anahtarı değildir. Özel değerleri GitHub koduna veya sohbet içine koyma. `AKADEMI_ALLOWED_ORIGINS` mevcut web yayını için `https://muharremceylan.github.io` olmalıdır; `/Miko/` origin parçası değildir.
4. Servis yayımlandığında Render'ın verdiği **HTTPS servis adresini** al. `/health` yanıtı `ok`; `/v1/capabilities` yanıtında `solver_ready` ve `speech_ready` true olmalıdır. Sağlayıcı hesabı/model erişimi ayrıca gerçek denemeyle doğrulanır; true yalnız yapılandırmanın mevcut olduğunu gösterir.
5. GitHub deposunda **Settings → Secrets and variables → Actions → Variables → New repository variable** yolundan `AKADEMI_API_URL` oluştur; değerine yalnız HTTPS servis adresini yaz. Bu adres herkese açıktır, anahtar değildir. **OpenAI anahtarını bu alana koyma.**
6. **Actions → Akademi AI web önizlemesi → Run workflow** ile web sürümünü yeniden yayımla. İş akışı bu genel adresi derlemeye ekler; sağlayıcı anahtarını istemciye almaz.
7. Uygulamada **KPSS → Lisans → Dersler → Matematik → Temel Kavramlar → Yapay Zekâya Sor** aç. Pilot davet koduyla giriş yap; metin veya fotoğraf gönder. **Sesli Dinle** alanından özet seçip gerçek ses dosyası oluşturabilirsin. İlk bağlantı seçilen barındırma planı uykuya alınıyorsa gecikebilir; bağlantı ekranından tekrar dene.

Yayın hesabı ve anahtarlar tanımlanmadan “gerçek AI sonucu” veya “üretilmiş ses” gösterilmez. Hata, kota, bağlantı kopması ve belirsiz soru açık durumla sonuçlanır. Mevcut Fotoğraftan Çöz ekranındaki eski sabit demo korunur; yeni gerçek görsel gönderimi Matematikteki AI bölümündedir.

## Yerel geliştirme ve doğrulama

Depo kökünden:

```bash
python3 -m venv /workspace/.tools/akademi-api-venv
/workspace/.tools/akademi-api-venv/bin/python -m pip install --no-cache-dir -r services/api/requirements.txt
/workspace/.tools/akademi-api-venv/bin/python -m unittest services.api.test_api -v
/workspace/.tools/akademi-api-venv/bin/python -m uvicorn services.api.app:app --host 127.0.0.1 --port 8010 --workers 1
```

Ortam değişkenleri barındırma hizmetinden veya güvenli yerel ortamdan enjekte edilir. `.env.example` yalnız isimleri gösterir; uygulama dosyadan otomatik gizli değer okumaz. Gerçek `.env` dosyaları Git ve Docker bağlamından dışlanmıştır. Web geliştirme sunucusu `apps/capacitor` içinde `npm start` ile başlatılır. `AKADEMI_API_URL` derleme değişkeniyle istemci bağlanabilir. Bağlantı adrese göre HTTPS olmalı; yalnız yerel geliştirmede loopback HTTP kabul edilir.

17 servis testi; temiz sanal ortamda sabit bağımlılıklarla geçti. Testler gerçek ücretli API yerine kontrollü sağlayıcı/HTTP taklitleri kullanır. Gerçek uvicorn sunucusu başlatılıp sağlık ve anahtarsız yetenek yanıtları doğrulandı. Fiziksel cihazda duyulabilir ses, gerçek OpenAI çözümü/sesi, Render yayını ve Docker imajı çalıştırma henüz doğrulanmadı. Docker dağıtım tanımı hazırdır; çalıştırılmış imaj iddiası yapılmaz.

## Güvenlik, gizlilik ve doğrulama sınırları

- Sağlayıcı anahtarı yalnız sunucudadır. İlk pilot davet kodu doğruysa 20 dakikalık rastgele bearer oturumu oluşturulur; token sunucuda özetlenmiş halde, tarayıcıda yalnız bellekte tutulur. Sayfa yenilenince yeniden giriş gerekir. Bu, tam kullanıcı hesabı/yönetim sistemi değildir.
- Varsayılan durumda anahtar veya güçlü davet kodu eksikse ücretli uçlar kapalıdır. CORS tek başına yetkilendirme olarak kullanılmaz. İzinli origin, istek sınırı ve davet oturumu ayrıca denetlenir.
- Tek süreçte oturum başına dakikada altı istek; süreç başına günde 50 çözüm ve 20 yeni ses üretimi sınırı vardır. Aynı özetin sesi süreç belleğinde yeniden kullanılır. **Kotalar, oturumlar ve ses önbelleği süreç yeniden başlatıldığında sıfırlanır.** Bunlar kalıcı maliyet sınırı veya üretim ölçeğinde çok sunuculu kota sistemi değildir; genel yayın öncesinde kalıcı sayaç/kimlik ve sağlayıcı tarafı bütçe takibi gerekir.
- Yalnız sunucudaki üç özgün özet metni seslendirilir; sınırsız serbest metin ses üretimi yoktur. Sesler `temel-audio.json` içinde, matematiksel sembolleri sözcüklerle açıklayan ayrı metinlerdir. AI ses kaydı açıkça etiketlenir.
- İstek gövdesi en fazla 6 MB; görsel en fazla 4 MB ve 16 megapikseldir. JPEG/PNG/WebP gerçek dosya türüyle açılır, en fazla 2048 piksele indirilir ve metadata olmadan yeniden kodlanır. Uzak görsel URL'si alınmaz.
- Metin ve görseller gerçek hizmet bağlandığında AI sağlayıcısına iletilir. Uygulama sunucusu soru/görseli veritabanında saklamaz; Responses çağrısı `store:false` kullanır. Bu, sağlayıcının tüm teknik/gizlilik saklama koşullarının sıfır olduğu garantisi değildir. Herkese açık kullanımdan önce veri politikası ve sağlayıcı koşulları tamamlanmalıdır.
- Sayısal eşitlikler sınırlı AST ve kesin kesir aritmetiğiyle bağımsız kontrol edilir. `eval`, dosya/komut çalıştırma veya modelden gelen kod yürütme yoktur. Bazı eşitliklerin geçmesi çözümün bütününü doğrulamaz; değişkenli adımlar, OCR okuması ve pedagojik doğruluk uzman onayı değildir. Çelişki varsa sonuç açıkça uyarılır. AI sonuçları test istatistiğine doğru cevap olarak otomatik eklenmez.
- Postgres, kullanıcı hesabı, kalıcı kuyruk ve medya deposu bu pilotta kurulmadı. Gelecekte FastAPI/PostgreSQL mimarisine geçerken bu modül sağlayıcı adaptörü olarak korunabilir.

Resmî sağlayıcı şemaları bu geliştirmede [Responses parametreleri](https://github.com/openai/openai-python/blob/main/src/openai/types/responses/response_create_params.py) ve [Speech parametreleri](https://github.com/openai/openai-python/blob/main/src/openai/types/audio/speech_create_params.py) üzerinden incelendi. Gerçek model/hesap bağlantısı güvenli yapılandırmadan sonra ayrıca test edilmelidir.

## Sayılar ses kataloğu

Temel Kavramlar dışında Sayıların yedi alt konusu için de `quick`, `standard`, `detailed` ses metinleri sunucu kataloğundadır. İstemci serbest seslendirme metni göndermez; yalnız konu kimliği ve özet seviyesi gönderir. Önbellek anahtarı konu+sürüm+seviye olduğundan farklı konular aynı sesi paylaşmaz. `sayilar` ana konu ekranı bir çalışma rotasıdır; kendi ses kaydı yoktur. İçerik `topics/sayilar.json` içindedir. Sağlayıcı taklitleriyle konu ayrımı test edilmiştir; gerçek OpenAI ses üretimi hâlâ anahtar ve yayın hesabı bekler.
