# Akademi AI — mobil prototip (v0.2)

Bu ilk ürün prototipi **tek HTML dosyasıdır**. `index.html` dosyasını telefon veya bilgisayar tarayıcısında açarak deneyebilirsiniz. İnternet, sunucu, üyelik veya ücretli API gerektirmez.

## Çalışan alanlar
- Ana sayfa ve günlük hedef kartı
- 4 örnek ders için detaylı konu anlatımı + kısa özet
- 10 özgün, editör kontrolünden geçirilmesi gereken örnek soru; konu filtresi, karışık test, açıklamalar
- Soru istatistiklerinin cihaz tarayıcısında tutulması (localStorage)
- Cihaz destekliyorsa tarayıcının Türkçe ses senteziyle sesli özet
- Görsel seçme/kameradan fotoğraf alma ve **örnek** AI çözüm akışı ekranı
- Ders bazında analiz ve kişisel tekrar önerisi (basit kural tabanlı)

## Henüz olmayanlar
- Gerçek görüntü anlama / yapay zekâ ile fotoğraftaki soruyu çözme
- Gerçek AI ile soru üretimi veya AI öğretmeni
- Kullanıcı hesabı, bulut senkronizasyonu, gerçek podcast dosyaları
- ÖSYM çıkmış soruları / telif izinleri / yönetici paneli
- Gerçek Android/iOS paketi

## Önerilen üretim mimarisi
Flutter (Android/iOS) + FastAPI (Python) + PostgreSQL + S3 nesne deposu + sunucu tarafında AI servisleri. İçeriklerin uzman onayı, versiyonlama, kaynak atfı ve soru çözümü doğrulaması zorunlu.

## İlk veri modeli
`exam`, `subject`, `topic`, `lesson`, `lesson_revision`, `question`, `answer_choice`, `question_source`, `attempt`, `user_progress`, `audio_asset`, `ai_solution`, `content_review`.

## Sonraki sprint
1. Prototipi Flutter ekranlarına taşımak.
2. Backend ve kullanıcının soru çözme oturumları için API tasarlamak.
3. Onaylı soru bankasını içeri almak.
4. Görseldeki soruyu algılama ve doğrulama hattı kurmak.
5. 15–30 katılımcı ile mobil pilot test yapmak.

> Bu bir ürün prototipidir; eğitim içeriği örnektir, ÖSYM tarafından yayımlanmış veya onaylanmış değildir.

## v0.2 — İlk düzeltmeler

Günlük/toplam sayaçlar ayrıldı; günlük hedef 10 soruda dolu kalır. Bozuk/engelli tarayıcı kaydı uygulamayı durdurmaz. Eski sürüm toplamları korunur, geçmiş cevapların tarihi bilinmediğinden günlük sayaca aktarılmaz.

Testler aynı örnek havuzdan dengeli karıştırılır ve havuz sonunda sonuç ekranına geçer. Yeni test aynı soruları yeniden içerebilir; yarım oturum sayfa yenilemesinde devam etmez. Fotoğraf seçimi JPEG/PNG/WebP ve 10 MB ile sınırlıdır; çözüm hâlâ sabit demodur. Ses başka ekrana geçince durur.

### Çalıştırma

Flutter kurulumu gerekmez. `index.html` tarayıcıda açılabilir. Daha tutarlı yerel kullanım için klasörde `python -m http.server 8000 --bind 127.0.0.1` çalıştırıp tarayıcıdan erişin. Bu aşama Android/iOS paketi değildir.

### Doğrulama

Playwright ile sistem Chromium'unda 11 kontrol grubu geçti: ders/özet/filtre, 10 soruluk sonuç, tekrar cevap engeli, 10/11 hedefi, kayıt kalıcılığı, gün geçişi, eski ve bozuk kayıtlar, engelli depolama, görsel hata durumları, ses iptali ve farklı ekran genişlikleri. Otomasyon çalışma ortamında `/workspace/scratch/akademi-review/regression.py` dosyasındadır. Gerçek Türkçe ses çıktısı ve mobil kamera fiziksel cihazda ayrıca test edilmelidir.
