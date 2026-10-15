# KPSS içerik kaynakları ve doğrulama durumu

15 Ekim 2026 itibarıyla kaynak verileri ve editör onaylı eğitim içeriği ayrı değerlendirilir. Kaynak tablo aktarımı aşamasında yeni tam ders anlatımları üretilmedi. Sonraki Temel Kavramlar çalışma paketi aşağıda ayrıca belirtilmiştir; gerçek AI servisi bağlı değildir.

## Renkli notlar, font ve ses metinleri

Hatırlama kancaları, soru/cevap kartları ve üç konuşma metni bu geliştirmede özgün çalışma taslağı olarak yazıldı. `temel-audio.json` matematiksel sembolleri konuşma diliyle açıklar; yayımlanmış bir podcastten alınmadı. Gerçek ses üretilirse yapay zekâ sesi olarak etiketlenir. Caveat fontu Google Fonts'un resmî deposundan alındı; Türkçe Latin karakterler için alt kümelenip Akademi Notes adıyla gömüldü. Kaynak telif bildirimi ve SIL OFL 1.1 lisansı `apps/capacitor/src/math/assets/OFL.txt` ve üretilen CSS'te korunur. Türkçe Ç/Ğ/İ/Ö/Ş/Ü ve küçük harflerin karakter haritası kontrol edildi. Sağlayıcı taklitleriyle yapılan test sesleri veya AI sonuçları gerçek içerik olarak yayımlanmaz.

## Temel Kavramlar özgün çalışma içeriği

15 Ekim 2026: Ayrıntılı anlatım, üç özet, sekiz formül kartı, seslendirme metni, üç çözümlü örnek ve 30 test sorusu bu geliştirme sırasında asistan tarafından özgün taslak olarak yazıldı. Kitapseç veya ÖSYM soruları kopyalanmadı; eğitim içeriği “çıkmış soru” veya uzman onaylı ürün olarak sunulmaz. Yalnız KPSS Lisans içindeki Temel Kavramlar paketinde kullanılabilir.

`scripts/content-validation/validate_math.py`; beş seçeneğin benzersizliğini, cevapları ve içerik alanlarını denetler. Tam sayı/rakam aralıklarında sayma, rasyonel hesaplarda Fraction, parite sınıfları ve polinom katsayıları kullanılır. Negatif sayı sıralaması gibi iki genel iddiada sayısal örnek kontrolü yapılır; genel cebirsel gerekçe çözüm metnindedir. Kod kontrolü pedagojik kalite, telif taraması, tam biçimsel ispat veya insan uzman onayı değildir. Tüm paket uzman incelemesi bekleyen çalışma/demodur; arayüz bu durumu belirtir. Formül kartı örnekleri editör incelemesinde ayrıca değerlendirilecektir.

Çözümlü örnekler test havuzundan ayrı kimliklerle tutulur; çözülmemiş soru sayısını yapay biçimde artırmak için aynı sorular çoğaltılmaz. Geçmiş dağılım verileri özgün soru üretiminin doğruluğu veya 2026 kesin kapsamı için onay sayılmaz.

## Lisans Matematik konu listesi ve genel dağılım

Kaynak: [Kitapseç — 2026 KPSS Lisans Matematik konuları ve soru dağılımı](https://www.kitapsec.com/blog/2026-kpss-lisans-matematik-konulari-ve-soru-dagilimi-149.html). URL bu bulut ortamında 403 ile engellendi. Kullanıcı yazının konu ve soru sayısı bilgilerini sohbet içinde metin olarak paylaştı; bu paylaşımdaki olgusal liste ve sayılar uygulamaya aktarıldı. Yazının tüm metni kopyalanmadı ve doğrudan erişilerek doğrulanmış gibi sunulmadı.

17 ana başlık ve alt konuları korunur. Denklemler, mevcut Birinci Dereceden Denklemler örneği ve üç demo soruya bağlanır. Temel Kavramlar çalışma paketi hariç diğer konu başlıkları hazırlık durumundadır. Mevcut örnekler tam ders veya uzman onaylı müfredat sayılmaz.

Genel dağılım 16 gruptur; sayılar toplamı 26 eder. Paylaşılan metin dağılımın dayandığı sınav yılını belirtmez. 2026 için kesin ÖSYM soru sayısı olarak sunulmaz. “Bağıntı ve Fonksiyon” genel dağılımda bulunur, 17 ana konuda ayrı başlık değildir; sessizce yeni bir ana konu icat edilmedi. Resmî kapsam/uzman karşılaştırması gereklidir.

## 2015–2024 yıllık dağılım

Kaynak: kullanıcının sohbet içinde paylaştığı “KPSS Lisans Matematik Konu Dağılımı” tablo görseli. Görseldeki 16 konu satırı, 10 yıl ve toplam satırı aktarılır. Değerler `mathAnnualRows` içinde; kaynak toplamları `mathAnnualSourceTotals` içinde tutulur. Çizgi işaretleri `null` olarak saklanır ve ekranda çizgi görünür; satır toplamında sıfır katkı sayılır. Bu işaret tek başına resmî bir “soru sorulmadı” doğrulaması değildir.

| Yıl | Görseldeki toplam | Konu satırları toplamı | Durum |
|---|---:|---:|---|
| 2015 | 27 | 36 | Doğrulanmalı |
| 2016 | 27 | 26 | Doğrulanmalı |
| 2017 | 27 | 26 | Doğrulanmalı |
| 2018 | 26 | 26 | Aritmetik tutarlı |
| 2019 | 26 | 26 | Aritmetik tutarlı |
| 2020 | 26 | 26 | Aritmetik tutarlı |
| 2021 | 26 | 25 | Doğrulanmalı |
| 2022 | 27 | 27 | Aritmetik tutarlı |
| 2023 | 28 | 27 | Doğrulanmalı |
| 2024 | 26 | 28 | Doğrulanmalı |

Aritmetik tutarlılık resmî doğruluk veya uzman onayı değildir. Görseldeki değerler tahminle düzeltilmez; uygulama iki toplamı gösterir ve fark varsa uyarır. 2025 ve 2026 yıllık verisi paylaşılmadığı için eklenmedi. Genel dağılım ile yıllık tabloda konu grupları farklıdır; bunlar ayrı görünümlerdir, tek seri gibi birleştirilmez.

## Diğer düzeyler ve dersler

Lisans, Ön Lisans ve Ortaöğretim ayrı yerel ilerleme kayıtları kullanır. Ön Lisans/Ortaöğretim henüz düzeye özel müfredat içermez; ortak demo içeriği açıkça etiketlenir. Eski ortak istatistiklerin Lisans alanında korunması yalnız veri kaybını önleyen bir demo uyumluluk kararıdır.

Geometri ve Güncel Bilgiler yalnız ders alanı/hazırlık ekranı olarak eklendi. Anlatım/özet/soru/ses içerikleri yoktur. Güncel Bilgiler yayınına kaynak, olay tarihi ve son kontrol tarihi eklenmelidir. Üç düzey için resmî kapsam doğrulanmadan tam müfredat iddiası yapılmamalıdır.

## Sayılar özgün çalışma taslakları — 15 Ekim 2026

Kullanıcının verdiği alt konu adlarına göre yedi konu için anlatım, üç özet, hatırlama kartı, seslendirme metni, 70 beş seçenekli test sorusu ve 14 ayrı çözümlü örnek oluşturuldu. Metinler ÖSYM veya yayıncı sorularından kopyalanmadı; resmî çıkmış soru, resmî sınav dağılımı veya uzman onaylı içerik olarak sunulmaz. Tanım tercihi: doğal sayılar sıfırı içerir; sorudaki tanım önceliklidir.

`python scripts/content-validation/validate_math.py` seçenek benzersizliğini, konu/kimlik/sürüm bağlantılarını ve cevapları bağımsız aritmetik, sonlu küme taraması, taban denklemi, faktöriyel ve Öklid bölmesiyle kontrol eder. Kontrol tanımları her yeni sorunun `verification` alanındadır. Bu kontroller öğretim yeterliliği, zorluk kalibrasyonu veya uzman incelemesi değildir. Sayılar alt konularında 20/30 soruluk tam havuzlar ve daha fazla zor örnek sonraki görevlerdir.
