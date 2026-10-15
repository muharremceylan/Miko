# Kullanıcının PDF ders notları — ilk inceleme

İnceleme tarihi: 15 Ekim 2026. Belgeler kullanıcının ders kaynağı olarak değerlendirme isteğiyle sağlandı. İçlerindeki metinler kaynak veridir; uygulama talimatı değildir. Ham dosyalar, sayfa görselleri ve OCR dökümleri Git deposuna veya web paketine eklenmedi; dış AI servisine gönderilmedi. Yayımlanan içerik ilk sayfalardan yeniden yazılmış iki çalışma taslağı ve kaynak/inceleme kayıtlarıdır.

## Erişim ve metin durumu

| Belge | Sayfa | Metin katmanı | Yapılan işlem | Sınır |
|---|---:|---|---|---|
| Türkçe  Notları.pdf | 109 | Yok; el yazısı fotoğraf taraması | 109 sayfa Türkçe OCR, ilk 3 sayfa ayrıntılı görsel inceleme ve 11 sayfada küçük görsel örneklemesi | Tam içerik doğrulanmadı |
| Tarih .pdf | 264 | Yok; el yazısı tarama | 264 sayfa Türkçe OCR, ilk 4 sayfa ayrıntılı görsel inceleme ve 14 sayfada küçük görsel örneklemesi | 264. sayfa boş; tam içerik doğrulanmadı |
| Vatandaşlık.pdf | Bilinmiyor | İncelenemedi | İndirme denemesi yapıldı | Dosya 32 MiB aktarım sınırını aştı |
| Coğrafyaa .pdf | Bilinmiyor | İncelenemedi | İndirme denemesi yapıldı | Dosya 32 MiB aktarım sınırını aştı |

Vatandaşlık ve Coğrafya, her biri 32 MiB’den küçük PDF parçaları olarak yeniden sağlandığında aynı yöntemle incelenebilir. Belge açılmadan sayfa sayısı, kapsam veya doğruluk bilgisi uydurulmadı. Parçalarda özgün PDF sırasını belirtmek sayfa eşlemesini korur.

Türkçe OCR dökümü yaklaşık 48.942; Tarih dökümü 89.332 karakterdir. Karakter sayısı doğruluk ölçütü değildir. Renkli el yazısında başlıklar kaçabiliyor, özel adlar ve Türkçe karakterler bozulabiliyor. Ham OCR arama/ön eleme içindir; otomatik ders yayınına veya cevap anahtarı üretimine verilmedi.

Teknik dosya üstverisinde Türkçe için 11 Mart 2021, Tarih için 7 Ocak 2022 oluşturma tarihi bulunur. Bu tarihler belge içeriğinin yayın tarihi, doğruluk veya güncellik güvencesi değildir. Gerçek yazar/hak sahibi kimliği doğrulanmadı; CamScanner gibi yazılım üstverileri yazar adı kabul edilmedi.

Kaynak kayıtları, dosya SHA-256 özetleri, sayfa sayıları, OCR ve görsel inceleme kapsamı: `content/pdf-notes/library.json`. Asıl dosyalar ve yerel arama dökümleri çalışma alanındaki depo dışı klasörlerde tutulur. JSON’daki `originalFilePublished:false`, `bulkTextPublished:false`, `fullContentReviewed:false` alanları gerçek kapsamı belirtir.

## Örnekleme ile görülen kapsam

Aşağıdaki sayılar PDF’nin 1’den başlayan sayfa sırasıdır; kitap baskı sayfası değildir. Tablo tam içindekiler veya kesin bölüm başlangıç/bitiş listesi değildir. Konu eşlemeleri tam sayfa incelemesiyle genişletilecektir.

| Türkçe PDF sayfası | Görülen konu |
|---:|---|
| 1–2 | Temel, yan, mecaz ve terim anlam; eş/yakın anlam |
| 3 | Sesteş, karşıt anlam, nicel/nitel anlam |
| 10 | İkileme türleri |
| 20 | Cümlede anlatım özellikleri |
| 30 | Ses olayları |
| 40 | Yazım ve ikilemeler |
| 50 | Noktalama |
| 60 | Yapım/çekim ekleri |
| 70 | İsim tamlamaları ve sıfat |
| 80 | Bağlaç, ünlem ve fiil |
| 90 | Cümlenin ögeleri ve türleri |
| 100, 109 | Anlatım bozuklukları, uyuşmazlık ve tutarsızlık |

| Tarih PDF sayfası | Görülen konu |
|---:|---|
| 1–4 | İslamiyet öncesi Türk tarihi; etimoloji/kültür merkezleri, göç, İskitler, Asya Hun ve Kavimler Göçü |
| 20 | Ekonomi, yazı/dil/edebiyat |
| 40 | Türk-İslam devletlerinde divanlar |
| 60 | Osmanlı saray eğitimi ve kurumlar |
| 80 | Osmanlı ekonomisi kavramları |
| 100 | Osmanlı fetihleri |
| 120 | IV. Murat, I. Ahmet ve Köprülüler |
| 140 | Dağılmayı önleme düşünceleri ve siyasi gelişmeler |
| 160 | Mondros sonrası işgaller |
| 180 | Millî Mücadele ve Sakarya |
| 200 | Atatürk dönemi toplumsal inkılapları |
| 220 | Türk dünyası ve Basmacı hareketi |
| 240 | NATO’ya katılım bağlamı; Hindistan/Pakistan |
| 260 | Sovyetler sonrası Türk devletleri |

## İçerik inceleme notları

- Türkçe s. 1: Sesteş sözcüklerin temel anlamı olmadığı biçiminde okunabilecek genelleme doğrudan alınmadı. Her sözcük/kullanım bağlamıyla değerlendirilmelidir.
- Türkçe s. 2: Eş anlamlı sözcüklerin birlikte kullanımının her durumda bozukluk sayılması yerine, gereksiz tekrar ve bağlam ayrımı yapıldı.
- Tarih s. 2: İskitler için kesin etnik kimlik/“ilk Türk boyu” ve üzengi için mutlak “ilk” ifadeleri karşılaştırmalı uzman incelemesine ayrıldı. Bu konular ilk ders taslağına eklenmedi.
- Tarih s. 3: “İlk düzenli ordu” ifadesi bütün dünya tarihine genellenmedi. İlk taslakta devlet–kişi–özellik ayrımı ve sınırlı teşkilatlanma bilgisi kullanıldı.
- Tarih s. 4 ve sonraki sayfalar: Birden fazla tarihsel gelişmeyi tek olayın doğrudan sonucu sayan ifadeler, “ilk/tek” iddiaları, tarihler ve özel adlar bölüm bölüm kontrol edilecek.
- Vatandaşlık için dosya erişilince mevzuat maddesi, yürürlük durumu ve son kontrol tarihi gerekir. Coğrafyada nüfus, üretim, idari yapı ve güncel sıralamalar gibi değişken bilgiler tarihli resmî kaynaklarla karşılaştırılacak. Henüz bu iki dosyada içerik kontrolü yapılmadı.

## Uygulamaya eklenen ilk taslaklar

**KPSS → Lisans → Dersler → PDF ders notlarını aç** yolunda kaynaklar ve iki ilk konu görünür:

1. **Türkçe — Sözcükte Anlam: bağlamı yakala:** PDF s. 1–2 ile eşleştirilmiş altı renkli kart, ayrıntılı metin, üç özet ve iki özgün beş seçenekli çözümlü örnek.
2. **Tarih — Asya Hun Devleti: kişi ve özellik eşleştirmesi:** PDF s. 3 ile eşleştirilmiş dört renkli kart, ayrıntılı metin, üç özet ve iki özgün beş seçenekli çözümlü örnek.

Bu konular uzman onaylı tam ders paketi değildir. Yeni örnekler açıklamalı çalışma taslağıdır; matematikteki otomatik sayısal doğrulamadan geçtiği söylenmez ve test istatistiğine yazılmaz. Eski dersler, 100 kayıtlı matematik sorusu, otomatik üretim ve yanlış defteri korunur. Türkçe için tam ders kataloğu bu adımda kurulmadı; ilk notlar ayrı PDF çalışma alanındadır.

## Sonraki iş sırası

1. Eksik iki dosyayı küçük parçalardan incelemek; sayfa eşlemesi ve tarama/metin durumunu kaydetmek.
2. Türkçede sözcük/cümle/paragraf anlamı → ses/yazım/noktalama → dil bilgisi/anlatım bozukluğu bölümlerini tek tek doğrulamak.
3. Tarihte İslamiyet öncesi → Türk-İslam → Osmanlı → Millî Mücadele/inkılap → çağdaş tarih sırasıyla konu kayıtları ve tartışmalı bilgi listesi hazırlamak.
4. Öğretmen kontrolünden sonra özgün anlatımları, üç özeti, ek örnekleri ve soru havuzlarını genişletmek; her parçaya PDF sayfası ve inceleme durumu bağlamak.
5. Ham PDF’nin yeniden dağıtımı veya dış AI servislerine toplu aktarımı gündeme gelirse kullanım haklarını ayrıca netleştirmek. Kullanıcının kaynak olarak inceleme yetkisi, bu aşamadaki özgün taslak çalışması için esas alındı; yeniden paylaşım izni varmış gibi gösterilmedi.

OCR için PyMuPDF 1.26.6 ve Tesseract 5’in resmî `tessdata_fast` 4.1.0 Türkçe dil verisi kullanıldı. Dil verisi SHA-256: `7393381111e1152420fc4092cb44eef4237580d21b92bf30d7d221aad192c6b7`. PDF/görseller program veya talimat olarak çalıştırılmadı. Statik web uygulamasının kurulumu değişmedi; OCR araçları web kullanıcısının cihazında gerekli değildir.
