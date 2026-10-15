# Akademi AI

[**Canlı mobil web önizlemesini aç**](https://muharremceylan.github.io/Miko/)

GitHub Pages yayını ve canlı HTTP kontrolleri 15 Ekim 2026 tarihinde başarıyla tamamlandı.

Öncelik **web tarayıcısında mobil ekran görünümüyle geliştirme**. Ortak uygulama Capacitor + HTML/CSS/JavaScript ile `apps/capacitor` altında hazırlanıyor; Android ve iOS paketlerine sonra geçilecek. Flutter gerekmiyor.

KPSS Lisans → Dersler → Matematik içinde **Temel Kavramlar ve Sayıların yedi alt konusu** çalışılabilir. Renkli el yazısı kartları, üç özet seviyesi, formüller, çözümlü örnekler ve toplam **100 test sorusu** bulunur. Temel Kavramlar 30; Sayıların alt konuları 10’ar soru içerir. Sayılar ana ekranından 70 soruluk havuzla 10/20/30 soruluk karma test hazırlanır. Yanlış defterinden konuya dönülebilir ve soru yeniden çözülebilir; sonradan doğru çözülünce soru listeden çıkar, geçmiş korunur.

İlerleme/tema ve yarım testler cihazda saklanır; hesaplar arasında bulut eşitlemesi yoktur. Destekli cihazda Türkçe sesli özet kullanılabilir. İçerikler kodla kontrol edilmiş çalışma taslaklarıdır, uzman incelemesi bekler. Gerçek AI/üretilmiş ses için [sunucu kurulum rehberi](services/api/README.md) hazırdır; sunucu anahtarı ve yayın bağlantısı gerekir.

Yeni **Kaynak kütüphanesi**, anlatım/soru çalışması için altı aday bağlantı sunar; içerik ve hak incelemesi henüz yapılmadı. **Test Çöz → Otomatik alıştırma üret** seçeneği 16 özgün kalıptan 1706 sonlu varyasyonla 10/20/30 soru oluşturur. API anahtarı gerekmez; bu özellik gerçek AI üretimi değildir. Sayısal kontroller, yarım test ve yanlış defteri desteklenir. [Kaynaklar ve otomatik soru üretimi](akademi_ai_prototip/CONTENT_PIPELINE.md).

**PDF ders notları:** Kullanıcının Türkçe/Tarih taramalarından hazırlanan iki ilk konuya **KPSS → Lisans → Dersler → PDF ders notlarını aç** yolundan erişilir. Renkli anlatım, üç özet ve dört özgün çözümlü örnek içerir; kaynak sayfaları belirtilir. 373 sayfaya OCR uygulanması bütün içeriğin onaylandığı anlamına gelmez. Vatandaşlık/Coğrafya dosyaları aktarım boyutu sınırından dolayı henüz incelenemedi. [PDF inceleme raporu](akademi_ai_prototip/PDF_REVIEW.md).

- [iPhone ile Telegram PDF botu kurulumu](TELEGRAM_IOS_SETUP.md) — kod hazır; bot hesabı ve sürekli açık sunucu bağlantısı bekliyor.
- [Web mobil önizleme ve GitHub Pages hazırlığı](apps/capacitor/WEB_PREVIEW.md)
- [Mobil uygulama, tasarım ve derleme](apps/capacitor/README.md)
- [Proje planı ve durum geçmişi](akademi_ai_prototip/PROJECT_PLAN.md)
- [Öncelikli görevler](akademi_ai_prototip/TASKS.md)
- `akademi_ai_prototip`: korunan ve düzeltilmiş HTML prototipi.
- `apps/mobile`: önceki Flutter kaynak denemesi; aktif kurulumun parçası değildir.

İçerik örnektir. Gerçek AI, tam müfredat ve üretim backend'i henüz yoktur.
