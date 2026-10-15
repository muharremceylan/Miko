# KPSS Lisans Matematik — İçerik ve Ekran Gereksinimleri

15 Ekim 2026. Bu belge kullanıcının A–E içerik alanları ve Matematik mobil ekranı talebinin değerlendirmesidir. Uygulanmış özellikleri ve sonraki geliştirme işlerini ayırır. Bu değerlendirmeyle uygulama ekranları değiştirilmedi; tüm ders içeriklerinin üretildiği iddia edilmez.

## 1. Mevcut durum ve kapsam

| Alan | Şu anda | Hedef |
|---|---|---|
| Konu kataloğu | 17 ana konu, 22 alt başlık | Her ana/alt konu için kalıcı kimlik ve ayrı içerik paketi |
| Anlatım ve özet | Birinci Dereceden Denklemler için kısa demo anlatım ve tek kısa özet | Öğrenme hedefleri, ön bilgiler, ayrıntılı anlatım ve üç özet seviyesi |
| Formüller/örnekler | Anlatım içinde sınırlı örnek | Ayrı formül kartları, koşullar ve kolaydan zora çözümlü örnekler |
| Matematik test havuzu | Üç denklem sorusu, dört seçenek | Beş seçenekli, konu kimlikli, doğrulanmış ve sürümlenmiş sorular |
| Test seçenekleri | Ders filtresi ve mevcut havuzdan rastgele sıralama | 10/20/30 soru, rastgele, yanlış ve çözülmemiş filtreleri |
| Kayıt ve analiz | KPSS düzeyine göre günlük/toplam ve ders bazlı sayaç | Soru/deneme geçmişi, konu bazlı başarı, süre ve son çalışılan konu |
| Ses | Cihaz desteği varsa kısa özeti okuyan TTS ve durdurma | Özgün ses metni; gerçek medya varsa podcast oynatıcı |
| AI | Gerçek hizmet yok | Sunucu üzerinden, doğrulama durumu açık konu bağlamlı asistan |

Mevcut konu yapısında 34 son düzey konu vardır: alt başlığı olan beş ana konunun 22 alt konusu ve alt başlıksız 12 ana konu. Her son düzey konuda 30 benzersiz test sorusu sunulacaksa en az **1.020 özgün test sorusu** gerekir. Bu sayı kapsam hesabıdır; hazırlanmış soru sayısı değildir. Üst konu testleri alt konuların aynı soru havuzlarını kullanabilir; tek denemede soru tekrarlanmaz. Konu taksonomisi doğrulandıktan sonra bu hedef yeniden hesaplanır.

Her ana ve alt konu ayrı açılabilir: toplam 39 içerik düğümü. Üst başlıklar alt konuları bağlayan özgün bir giriş, bağlantılar ve toplu tekrar sunar; aynı anlatımı kopyalayarak içerik sayısı artırılmaz.

## 2. Her konu için içerik paketi

### A — Ayrıntılı anlatım

Sıra: öğrenme hedefi ve gerekli ön bilgi → tanım → temel kavramlar → kurallar ve geçerlilik koşulları → formüller → açıklamalı örnekler → önceki/sonraki konularla bağlantılar → KPSS çözüm teknikleri → sık hatalar → önemli hatırlatmalar ve öz değerlendirme.

Her işlem adımının gerekçesi açıklanır. Bölme işleminde paydanın sıfır olmaması, köklü ifadelerde tanım koşulları gibi kısıtlar örnekle birlikte gösterilir. Pratik yöntemlerin hangi koşullarda geçerli olduğu belirtilir; ezber tek başına açıklama yerine geçmez. Geometriye bağlantı verilebilir, ancak Geometri ayrı ders alanı olarak korunur.

### B — Üç özet seviyesi ve formüller

- **1 dakikalık hızlı tekrar:** temel kavram, ana formül, en sık hata ve tek kısa hatırlatma.
- **5 dakikalık standart özet:** ana kurallar, kullanım koşulları, küçük örnekler ve çözüm sırası.
- **Ayrıntılı tekrar notları:** tüm kazanımların düzenli tekrarı, istisnalar, karşılaştırmalar ve hata kontrol listesi.

Süreler yaklaşık okuma süresidir; her öğrencinin aynı sürede okuyacağı veya ses dosyasının tam bu uzunlukta olacağı iddia edilmez. Formül kartı; ad, okunabilir matematik gösterimi, değişken tanımları, koşullar, kullanım örneği ve pratik yöntemi içerir. Üç özet ayrı düzenlenir; ayrıntılı anlatımı otomatik kesmek yeterli değildir.

### C — Özgün çözümlü örnekler

Her son düzey konu için başlangıç önerisi en az bir kolay, bir orta, bir zor örnektir; gereken örnek sayısı kazanımlara göre artırılır. Bu sayılar yeni bir kullanıcı şartı değil, ilk içerik hedefidir.

Her örnekte soru kimliği/sürümü, sınav düzeyi, ilgili ana/alt konu, zorluk, özgün soru metni, **beş seçenek**, tek doğru seçenek, gerekçeli çözüm adımları, kullanılan formül veya kural ve uygunsa alternatif çözüm yer alır. Formül gerekmeyen soruda ilgili mantık/kural açıklanır; yapay bir formül eklenmez.

Kod doğrulaması; tam sayı ve rasyonel işlemlerde kesin aritmetik, denklemlerde yerine koyma/kök kontrolü, olasılıkta uygun sayma ve gerekirse sembolik hesap kullanır. Sayısal yaklaşım gerekiyorsa hata toleransı ve tanım aralığı kaydedilir. Kontrol kodu soru verisine güvenli bildirimsel alanlarla bağlanır; istemcide içerikten gelen rastgele kod çalıştırılmaz.

Doğru cevabın hesapla uyuşması, beş seçeneğin birbirinden farklı olması ve yalnız bir seçeneğin doğru olması ayrıca denetlenir. Kod kontrolü; soru metninin açıklığını, pedagojik uygunluğu, özgünlüğünü veya uzman onayını tek başına kanıtlamaz.

İçerik durumu: **taslak → matematiksel kontrol → editör/uzman incelemesi → onaylı/yayınlı**. AI ile yazılmış taslaklar bu süreçten geçmeden onaylı içeriğe dönüşmez. Önizlemede yayımlanacak onaysız örnek varsa açık demo etiketi taşır.

### D — Konu testleri ve sonuç

10/20/30 seçenekleri seçilen kapsamda yeterli uygun soru varsa çalışır. Havuz yetersizse gerçek sayı gösterilir; örneğin “Bu konuda 7 uygun soru var”. Daha kısa test açıkça teklif edilebilir. Otuz soruluk test izlenimi oluşturmak için sorular çoğaltılmaz veya tekrar ettirilmez.

Filtrelerin anlamı:

- **Rastgele:** seçilen sınav/düzey/konuya uygun havuzdan tekrarsız seçim. Tek tek rastgele çözüm de aynı havuzu kullanır.
- **Yalnızca yanlışlar:** o sorudaki son değerlendirilmiş cevabı yanlış olan sorular. Sonraki doğru cevap bu aktif listeden çıkarır; geçmiş yanlış denemeler silinmez.
- **Çözülmemişler:** geçerli içerik sürümü için hiç değerlendirilmiş cevabı olmayan sorular. Daha önce çözüm örneği olarak gösterilmiş soru yeniden kullanılacaksa bu maruziyet ayrıca işaretlenir; hiç görülmemiş yeni soru diye sunulmaz.

Yanlış/çözülmemiş havuzu boşsa nedenini ve uygun alternatif yolu göster. İçerik sürümü değiştiğinde önceki doğru/yanlış geçmişini sessizce yeni soruya taşıma; eski soru sürümünü deneme kaydında koru.

Test akışı: kapsam ve soru sayısı → uygun havuz sayısı → başlat → cevap/boş → bitirme → sonuç ve çözümler → yanlışlara veya ilgili anlatıma dön. Konu öğrenme modunda anında açıklama; değerlendirme modunda bitişte açıklama ayrımı yapılır. Yenileme sonrası yarım denemeye dönülebilir; tekrarlanan cevap olayı ikinci kez puanlanmaz.

Sonuçta doğru, yanlış, boş, cevaplanan/toplam soru, doğruluk oranı, test süresi, konu dağılımı ve önerilen tekrar gösterilir. Doğruluk `doğru / cevaplanan × 100` olarak etiketlenir; sıfır cevapta oran “—” olur. Boşlar ayrı gösterilir. Resmî net hesabı ancak ilgili sınavın güncel puanlama kuralı doğrulanıp sürümlendiğinde eklenir. Birkaç soruya dayanarak “konuyu kesin öğrendin” denmez.

### E — Sesli anlatım

Her konu için, matematiksel sembolleri dinlenebilir Türkçe ile açıklayan özgün bir anlatım metni bulunur. Örneğin sembolü yalnız okumak yerine işlemin anlamı ve adımları söylenir. Görsel gerektiren örneklerin metin/şekil bağlantısı sunulur.

Gerçek ses dosyası veya ses üretim hizmeti yoksa ses sekmesi **“Sesli anlatım henüz hazırlanmadı”** durumunu ve okunabilir ses metnini gösterir; çalışmayan oynatma, sarma veya süre çubuğu eklenmez. Mevcut cihaz TTS özelliği kullanılacaksa “Cihaz sesiyle oku” olarak ayrı ve desteğe bağlı sunulur; podcast kaydı gibi adlandırılmaz.

Gerçek medya bulunduğunda oynat/duraklat, 15 saniye geri/ileri, süreye göre sarma, hız seçimi, geçen/toplam süre ve dinleme konumu çalışır. Konum kaydı konu ve medya sürümüyle tutulur. Web'de arka plan oynatma tarayıcı/işletim sistemi politikasına bağlıdır; Android/iOS'ta ayrıca yapılandırma ve fiziksel cihaz testi gerekir. Gerçek dosya süresi ölçülmeden süre tahmin edilmez.

## 3. Matematik ana ekranı ve konu akışı

Üst bölümde **KPSS Lisans · Matematik**, ders ilerleme çubuğu ve “Devam et” kartı yer alır. Kart; son gerçekten çalışılan konuya, aynı sekmeye ve mümkünse okuma konumuna döner. Sırf listeden açmak konu tamamlama sayılmaz.

Özet alanı: tamamlanan/kalan son düzey konular, çözülen matematik soru sayısı ve matematik cevap doğruluğu. Mevcut diğer ders sayaçları Matematik istatistiğine katılmaz. Konu listesinde durumlar “Hazırlanıyor”, “Başlanmadı”, “Devam ediyor”, “Tamamlandı” olarak gösterilir. Genel/yıllık soru dağılımları kaynak bilgileriyle korunur; kişisel performans istatistiği gibi gösterilmez.

**İlerleme ve başarı farklıdır.** İlk sürümde tamamlanma öğrencinin açık “Konuyu tamamladım” işlemiyle, gerekli anlatım/örnek paketi hazır olan son düzey konular için kaydedilir. Ders ilerlemesi `tamamlanan son düzey konu / sürümlenmiş müfredattaki tüm son düzey konular × 100` olur. Hazırlanmakta olan başlıklar paydada kalır; yalnız bir örneğin bulunması %100 ilerleme oluşturmaz. Ana konu tüm zorunlu alt konular tamamlanınca tamamlanır; üst başlık ayrıca sayılarak çifte ağırlık verilmez. Müfredat genişlerse sürüm ve değişen toplam öğrenciye açıklanır. Test başarısı bu öz bildirimden ayrı ölçülür.

Konu ekranındaki yedi sekme:

| Sekme | Gösterilecek içerik |
|---|---|
| Konu Anlatımı | Öğrenme hedefleri, anlatım, bağlantılar, hatalar ve hatırlatmalar |
| Kısa Özet | 1 dakika / 5 dakika / ayrıntılı tekrar seçimi |
| Formüller | Formül ve kural kartları; koşullar ve kullanım örnekleri |
| Çözümlü Örnekler | Kolay/orta/zor; beş seçenek ve açılabilir adımlı çözüm |
| Test Çöz | Soru sayısı ve havuz filtreleri; devam eden test ve sonuç |
| Sesli Dinle | Gerçek oynatıcı veya açık hazırlık durumu ve ses metni |
| Yapay Zekâya Sor | Gerçek sunucu entegrasyonu varsa konu bağlamlı asistan; yoksa açık hazırlık durumu |

Mobilde yedi sekme tek satıra sıkıştırılmaz: yatay kaydırılan, seçili sekmeyi görünür tutan erişilebilir sekme şeridi kullanılır. Klavye/ekran okuyucu erişimi, 320 piksel genişlik, büyük yazı ve iki tema kontrol edilir. Konu başlığı ve geri dönüş yolu anlaşılır kalır; sekme değişimi cevapları veya okuma konumunu silmez. Hazırlık sekmeleri açılabilir ama gerçek işlevi olmayan gönder/oynat düğmeleri içermez.

AI alanında hizmet bağlanana kadar sahte sohbet veya sabit yanıt gerçek sonuç gibi sunulmaz. Entegrasyon sonradan FastAPI üzerinden yapılır; anahtarlar istemciye konmaz. Soru, konu ve içerik sürümü bağlama eklenir; yanıtların kaynak/doğrulama durumu ve belirsizlikleri gösterilir.

## 4. Veri ve uygulama düzeni

İçerik şeması şu ayrımları taşımalıdır: `Topic` (üst konu, sıra, kazanımlar), `LessonContent` (A/B/formül/ses metni ve sürüm), `Question` (beş seçenek, doğru cevap, çözüm, zorluk, alt konu, doğrulama ve yayın durumu), `Attempt`/`AnswerEvent` (soru sürümü, cevap, değerlendirme, süre), `TopicProgress` (durum ve son konum), `AudioAsset`/`ListeningProgress` (gerçek medya ve dinleme konumu).

Her kayıt sınav/düzey/ders kimliğiyle ayrılır. Mevcut ders bazlı sayaçlardan geçmiş soru kimlikleri veya yanlış listesi türetilemez; bu geçmiş uydurulmaz. Eski toplamlar önceki demo istatistiği olarak korunur; yeni ayrıntılı geçmiş yalnız kayıt tutulmaya başlandıktan sonraki olayları içerir.

Uygulama tek HTML dosyasını büyütmek yerine adım adım içerik verisi, ekranlar, test motoru, kayıt, analiz ve ses modüllerine ayrılır. İlk web sürümünde yerel ayrıntılı kayıt için IndexedDB değerlendirilebilir; kayıt hatası açık gösterilir. Hesaplar ve cihazlar arası eşitleme için FastAPI/PostgreSQL hedefi korunur. Backend henüz kurulmuş sayılmaz.

Önerilen ek yapı, mevcut dosyalar korunarak geliştirilir:

```text
akademi_ai_prototip/content/kpss/lisans/matematik/
  curriculum.json
  topics/<konu-kimligi>.json
  questions/<konu-kimligi>.json
  audio-scripts/<konu-kimligi>.md
apps/capacitor/src/math/
  screens/             # Ana ekran ve konu sekmeleri
  quiz/                # Havuz seçimi, deneme ve sonuç
  progress/            # Tamamlama, geçmiş ve uyumluluk
  audio/               # Gerçek medya / cihaz TTS ayrımı
scripts/content-validation/
  validate_math.py     # Şema, seçenek, sonuç ve koşul kontrolleri
```

Bu yapı bir öneridir; dizinler ve doğrulama aracı bu değerlendirmede uygulanmadı. Derleme/export ve Capacitor köprüsü yeni modüllere geçirilirken mevcut dersler ve yayın yolu korunmalıdır.

## 5. Öncelikli uygulama sırası ve kabul ölçütleri

1. **Ortak model ve ekran:** ana/alt konu kimlikleri, Matematik ana ekranı, yedi sekme, açık hazırlık durumları ve ayrı ilerleme/başarı hesapları. Gerçekte olmayan veriyle dolu kart yok.
2. **Temel Kavramlar içerik örneği:** ayrıntılı anlatımın dokuz alanı, üç özet, formüller, kolay/orta/zor çözümlü örnekler ve ses metni. Editör/uzman durumu açık; hesaplanabilir sonuçlar kodla kontrol edilir.
3. **Test ve geçmiş:** bu kapsamda 30 farklı beş seçenekli test sorusu hazır olduğunda 10/20/30 ve filtreler etkinleşir. Tek doğru, havuz sınırı, tekrarsızlık, boş havuz, kayıt hatası, yenileme ve çift kayıt kontrolleri geçer. Yanlış/çözülmemiş listeleri aynı geçmişle tutarlıdır.
4. **Kalan konular:** Sayılar ve alt konularıyla devam et; her paket aynı kalite koşullarından geçsin. Eski denklem örneklerini konu kimliği ve beş seçenekli soru şemasına kontrollü taşı.
5. **Gerçek ses ve AI:** medya/hizmet mevcut olduğunda gerçek kontrolleri bağla; sesin cihaz davranışını ve AI matematik doğrulama akışını ayrıca test et. Önce web, ardından Android/iOS paketleme.

İlk kullanılabilir örnek, Temel Kavramlar içinde **anlatım → özet → formül → örnek → test → sonuç → tekrar** yolunun tamamlanmasıdır. Tüm 39 düğümde eksik içerikleri hazır gibi göstermek veya aynı soruları çoğaltmak bu gereksinimleri karşılamaz.
