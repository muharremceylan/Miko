# Kaynaklar ve otomatik soru üretimi

## Çalışan kapsam — 15 Ekim 2026

Matematik ana ekranından veya konu içindeki **Bu konu için ek kaynaklar** düğmesinden kaynak kütüphanesi açılır. Konu anlatımı, soru/alıştırma, resmî sınav bilgisi ve konu listesi ayrı süzülür. Kaynaklar dış bağlantıdır; PDF, kitap veya soru metni uygulamaya alınmadı.

**Matematik → Temel Kavramlar veya Sayılar → Test Çöz → Çalışma kaynağı → Otomatik alıştırma üret** yolunda 10/20/30 soru üretilebilir. Temel Kavramlar ve Sayıların yedi alt konusu desteklenir. Her soru beş seçenek, doğru cevap, çözüm adımları, formül, tahmini düzey ve üretim kaydı taşır. API hesabı veya sunucu gerektirmez. Gerçek AI üretimi değildir.

16 özgün kalıp toplam 1.706 farklı parametre seçimi sunar. Aynı yöntemin sayılarla değişen örnekleri yeni soru türü sayılmaz. Kolay/orta etiketleri henüz öğrenci pilotuyla kalibre edilmedi. Zor soru üretimi veya tüm müfredat kapsamı iddia edilmez. Kayıtlı 100 soru ve 17 ayrı örnek korunur; otomatik alıştırmalar ayrı seçimdir.

## Kaynak kataloğu ve kullanım

Katalog: `content/kpss/lisans/matematik/sources.json`.

| Aday kaynak | Kullanım amacı | Sınır |
|---|---|---|
| [ÖSYM](https://www.osym.gov.tr/) | Resmî duyuru ve erişime açılmış soru sayfalarına ulaşma | Belirli belge henüz incelenmedi |
| [OGM Materyal](https://ogmmateryal.eba.gov.tr/) | Matematik anlatımı ve alıştırma arama | KPSS’ye özel değildir; bölüm eşlemesi bekler |
| [ÖDSGM](https://odsgm.meb.gov.tr/) | Ölçme ve değerlendirme materyali arama | Belge/sınıf/konu incelemesi bekler |
| [EBA](https://www.eba.gov.tr/) | Anlatım ve etkinlik arama | Bazı içerikler giriş gerektirebilir |
| [OpenStax Prealgebra 2e](https://openstax.org/details/books/prealgebra-2e) | İngilizce aritmetik/cebir için aday kitap | Bölüm ve güncel lisans koşulları incelenmedi |
| Kullanıcının Kitapseç bağlantısı | Önceki konu/dağılım aktarımının kaynağı | Resmî kapsam veya soru kaynağı değildir |

15 Ekim 2026 HTTP denemelerinde altı kaynak ve OpenStax lisans sayfası bu ortamın ağ geçidinden 403 aldı. Bu, sitelerin kullanıcı tarafında kapalı olduğunu göstermez. Başarılı erişim veya lisans kontrolü yapılmış sayılmaz. Kayıtlar `candidate`, `general-reference`, `blocked-in-environment`, `importAllowed:false` durumundadır. Mevcut anlatımlar bu kaynaklarla doğrulanmış sayılmaz.

Katalog kaynak kimliği, kurum, URL, dil, kullanım amacı, konu kapsamı, inceleme durumu, erişim denemesi ve hak/izin alanlarını taşır. Konu kapsamı şimdilik geneldir; belirli bölüm/sayfa eşlemesi gibi sunulmaz. Aday kaynağı kaydetmek, içeriği uygulamaya veya AI servisine aktarma izni değildir.

Kaynak kabul sırası:

1. Belgeyi ve ilgili bölüm/sayfaları incele; tarih/sürüm ve hedef kazanımı kaydet.
2. Sınav kapsamı için güncel ÖSYM kılavuzunu esas al. MEB/İngilizce kitapları anlatım desteği olarak değerlendir.
3. Lisans/yazılı izin belgesini; ticari kullanım, çeviri, uyarlama ve AI’a aktarım koşullarını kaydet. Hak bilinmiyorsa yalnız bağlantı ver.
4. Öğretmen birden fazla kaynaktaki yöntemleri karşılaştırıp özgün anlatım taslağı hazırlar. Yayınevi soruları ve uzun metinler izinsiz kopyalanmaz.
5. Tanım, ön koşul, formülün şartları, gerekçeli örnek, karşı örnek, sık hata, üç özet, görsel ve ses metnini incele; kaynak bölümü ve son kontrol tarihini ilişkilendir.

Soru kaynağını genişletmenin ikinci yolu yayıneviyle lisans anlaşması veya yetkili içerik/API akışıdır. Kitap satın almak dijital yeniden yayın izni değildir. İzinli sorular kimlik/sürüm, konu/kazanım, zorluk, doğru cevap, çözüm ve hak bilgileriyle ortak modele aktarılacaktır.

## Otomatik üretim ve bağımsız kontrol

- `apps/capacitor/src/math/generator.js`: 16 özgün kalıp, sonlu parametre uzayı, sabit soru kimliği/seçenekler ve konu/düzey seçimi.
- `apps/capacitor/src/math/generation-check.js`: üretim kısa yollarından ayrı sayma, arama, tekrarlı işlem ve büyük tam sayı hesapları.
- `apps/capacitor/src/math/engine.js`: test ve soru görüntülerini saklama, geçmiş varyasyonları eleme, sonuç ve yanlış tekrarları.
- `scripts/content-generation/generate.mjs`: editör için tekrarlanabilir JSON taslağı; var olan dosyayı değiştirmez.

Kontrol örnekleri: ardışık toplam formülüne karşı tek tek toplama; rakam denklemine karşı 10–99 taraması; faktöriyel son sıfır formülüne karşı büyük tam sayı faktöriyelinin son sıfırlarını sayma; kalan formülüne karşı ardışık çıkarma; 12’ye bölünme kurallarına karşı doğrudan bölüm kalanı. Tam beş farklı sayısal seçenek ve tek doğru seçenek aranır. Kontrol geçmeden deneme yazılmaz. Bu, dil/anlam doğruluğu, öğretim yeterliliği veya uzman onayı değildir.

`origin` alanı kalıp kimliği/sürümü, parametreler, `akademi-templates-v1` özgün kaynak kimliği ve `expertApproved:false` bilgisini taşır. Aynı kalıp/parametre için soru kimliği ve seçenek sırası sabittir. Test içinde tekrar yoktur; önceki otomatik testlerine seçilen varyasyonlar yeni üretimden çıkarılır. Sonlu havuz tükenirse düğmeler pasif olur. Kayıt sıfırlanır veya farklı cihaz kullanılırsa geçmiş bilinmez; küresel benzersizlik iddiası yoktur.

Yarım test yenileme sonrası aynı sorularla sürer. Cevaplar istatistiklere eklenir. Bitmiş testin son yanlışları deftere ve yanlış filtresine girer; aynı sürüm doğru çözülünce listeden çıkar. Öğrenci alıştırmaları uzman onaylı/çıkmış soru bankasına otomatik eklenmez.

Depo kökünden örnek taslak:

```bash
node scripts/content-generation/generate.mjs \
  --topic sayilar --count 30 --difficulty mixed --seed pilot-1 \
  --output /tmp/akademi-soru-taslagi.json
```

Düzeyler `mixed`, `Kolay`, `Orta`; sayı 1–30. Dosya `status:draft` ve `expertApproved:false` taşır; soru bankasına aktarılmaz. Aynı tohum aynı listeyi verir. Mevcut dosya üzerine yazma reddedilir.

## Sonraki aşama: kaynakla desteklenen gerçek AI taslakları

Bu bölüm tasarımdır; çalışan AI soru üretim servisi veya yönetim paneli değildir. Mevcut metin/fotoğraf çözüm API’si soru üretim ucu olarak gösterilmez. Gerçek üretim için sağlayıcı hesabı/anahtarı ve HTTPS sunucu gerekir; anahtar yalnız sunucuda kalır.

Önerilen hat: **İzinli ve incelenmiş kaynak → konu/kazanım modeli → üretim işi → AI taslağı → bağımsız kontrol → öğretmen incelemesi → sürümlü yayın**.

FastAPI üretim işini alır; worker kuyrukta yürütür. PostgreSQL kaynak izinlerini, belge/bölüm sürümlerini, iş durumunu, soru sürümlerini ve inceleme kararını tutar. Gereken dosyalar özel nesne deposuna alınır. AI’a yalnız aktarım izni bulunan ve editörün seçtiği parçalar gider. Kaynak metinleri veri olarak ele alınır; içlerindeki talimatlar sistem talimatı sayılmaz.

İstek sınav/düzey, konu/kazanım, hedef zorluk, soru türü, sayı ve izinli kaynak kimliklerini taşır. Çıktıda beş seçenek, tek doğru cevap, adımlı çözüm, koşullar, kaynak bölüm kimlikleri ve mümkünse sınırlı doğrulanabilir matematik modeli istenir. Anahtar, kullanıcı/rol yetkisi, kalıcı kota, maliyet sınırı, model/prompt sürümü, iptal/zaman aşımı ve başarısız iş kaydı sunucuda yönetilir.

Modelin cevabı tek başına cevap anahtarı olmaz. Bağımsız hesap, tanım kümesi/koşullar, tek doğru seçenek, çelişkili adımlar ve soru benzerliği kontrol edilir. Modelin gönderdiği Python/JavaScript çalıştırılmaz. Benzerlik yalnız metne değil yöntem/kalıp ailesine göre de ölçülür; sayıları değişen örnekler ayrı soru türü sayılmaz.

Durumlar: `draft → automatic-check → needs-review → approved → published`; hatalı/belirsiz içerik `rejected` veya `quarantined` olur. Otomatik kontrol uzman onayının yerine geçmez. Yayında inceleyen kişi, tarih ve sürüm kaydedilir; geri alma mümkündür. İlk pilot 30–50 uzman cevaplı soruyla kapsam, tek doğru, çözüm ve dil kalitesini ölçer; zorluk öğrenci cevaplarıyla kalibre edilir.

İlk sıra: belirli kaynak bölümlerini/haklarını doğrulamak → öğretmenle mevcut kalıpları değerlendirmek → yöntem çeşitliliğini artırmak → izinli kaynak deposu ve kalıcı taslak kuyruğu → gerçek AI sağlayıcısı.
