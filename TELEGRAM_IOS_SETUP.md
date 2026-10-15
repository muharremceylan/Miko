# iPhone ile Telegram PDF botu

Bu bot, iPhone’dan özel sohbetine ilettiğin PDF’leri sunucuya indirir; küçük parçalara böler ve inceleme için metin taslağı çıkarır. Telefonunun sürekli açık kalması gerekmez. Telegram hesabındaki bütün kanalları veya eski mesajları kendiliğinden taramaz.

**Mevcut durum:** Kod ve sunucu kurulum dosyaları hazır. Gerçek bot hesabı ve sürekli açık sunucu henüz bağlanmadı. GitHub kodu saklar ve testleri çalıştırır; GitHub Pages sürekli bot çalıştırmaz. Bot kurulumu için Flutter veya iPhone’a Python yüklemek gerekmez.

## 1. Şimdi yapacağın işlem: bot oluştur

1. iPhone’da Telegram’ı aç. Doğrulanmış **[@BotFather](https://t.me/BotFather)** hesabına gir.
2. `/newbot` yaz.
3. Bir görünen ad seç: örneğin **Akademi PDF Asistanı**.
4. Sonu `bot` ile biten ve boşta olan bir kullanıcı adı seç. Örneğin `akademi_kaynak_asistani_bot`; bu adın boşta olduğu garanti edilmez.
5. BotFather’ın verdiği **token/anahtarı kendinde sakla**. Sohbete, GitHub dosyasına veya ekran görüntüsüne koyma. Burada yalnız botun `@kullanıcıadını` paylaşabilirsin.

BotFather’da isteğe bağlı `/setcommands` ile şu komutları tanımlayabilirsin:

```text
yardim - Kullanım ve komutlar
ders - Sonraki PDF için ders seç
durum - Son dosyaların durumu
parcalar - Hazır PDF parçalarını yeniden gönder
metin - İncelenmemiş metin taslağını gönder
sil - Dosyayı sunucudan sil
```

## 2. Büyük dosyalar için Telegram uygulama bilgileri

Normal Telegram Bot API indirme sınırı büyük PDF’lerimizi karşılamadığı için **bot hesabıyla MTProto bağlantısı** kullanıyoruz. Bu nedenle BotFather anahtarına ek olarak Telegram’ın verdiği `API ID` ve `API Hash` gerekir.

Safari’de [my.telegram.org](https://my.telegram.org) adresini aç. Telegram’ın kendi sitesinde giriş yapıp **API development tools** bölümünden uygulama bilgilerini oluştur. Giriş kodunu yalnız Telegram’ın resmî giriş ekranında kullan; bana gönderme. Oluşan `API ID` ve `API Hash` değerlerini de kendinde sakla. Bu işlem kişisel Telegram oturumunu bota devretmek değildir; yazılım yalnız bot anahtarıyla giriş yapar ve hesabın bot olduğunu kontrol eder.

Bu bilgiler istemci uygulamasına veya Pages’e konmaz. Kurulum aşamasında yalnız sunucu terminaline girilir. Giriş veya hesap oluşturma tamamlanamıyorsa gerçek bağlantı o aşamada bekler; test edilmiş yerel dosya işleme botun bağlandığı anlamına gelmez.

## 3. Sürekli çalışacak sunucu

Yalnız GitHub hesabın olduğu için bu adım henüz eksik. Docker çalıştırabilen, kapanmayan bir **Linux VPS** veya kalıcı diskli sürekli çalışan container hizmeti gerekir. Başlangıç pilotu için en az 2 GB RAM ve işletim sistemi/Docker dışında birkaç GB boş disk uygun bir başlangıçtır; kapasite PDF büyüklüğüne göre artırılır. Uykuya geçen ücretsiz web servisleri bu sürekli bağlantı için uygun olmayabilir.

Sunucu ücretli olabilir; bu çalışma bir hesap açmaz veya satın alma yapmaz. Alan adı satın almak gerekmez. Bot dışarıya bağlandığından webhook ve herkese açık web portu gerekmiyor; sunucunun Telegram veri merkezlerine çıkışına izin vermesi gerekiyor. Sağlayıcı seçildiğinde [teknik rehberdeki](services/telegram/README.md) hazır kurulum kullanılabilir. Sağlayıcı panelinin iPhone Safari üzerinden sunucu konsolu sunması işleri kolaylaştırır.

## 4. Sunucu bağlandıktan sonra iPhone’da kullanım

1. Kurulumun ürettiği **özel eşleştirme bağlantısını** iPhone’da açıp Başlat’a dokun. Bu bağlantıyı başkalarına gönderme. İlk doğru eşleşen kişi botun tek sahibi olur; sonraki kişiler erişemez.
2. Botun özel sohbetinde `/ders vatandaslik` veya `/ders cografya` yaz.
3. İzinli PDF’nin bulunduğu Telegram kanalını aç. PDF mesajına basılı tut → **İlet** → kendi botunu seç. Dosyayı sohbetin ek menüsünden de yükleyebilirsin. Kanal iletmeyi engelliyorsa bu kısıtlamayı aşmayız; paylaşım hakkın olan başka bir kopya gerekir.
4. Bot iş kodu verir. `/durum` ile takip et. İşlem tamamlanınca PDF parçalarını aynı özel sohbete gönderir.
5. Metin için `/metin İŞ_KODU`, yeniden parça istemek için `/parcalar İŞ_KODU` yaz. Taranmış sayfalarda Türkçe OCR kullanılır; hatalar olabilir ve inceleme gerekir.
6. `/sil İŞ_KODU` sunucudaki kaynak, parçalar ve metni kaldırır. Telegram sohbetine önceden gönderilen kopyaları sohbetten ayrıca silmelisin.

Varsayılan sınırlar: **250 MiB kaynak PDF, 1000 sayfa, parça başına 25 MiB, 7 gün saklama**. Önce iki parça denenir; boyut gerekiyorsa daha fazla parça oluşur. Tek sayfa bile 25 MiB’ı aşıyorsa sıkıştırma gerektiği bildirilir. Her dosya bu sınırlarla işlenebilir diye garanti verilmez; yoğun OCR zaman aşımına ulaşabilir.

Çıkan metinler ders notu hazırlamak için **inceleme taslağıdır**. Otomatik soru üretimi, gerçek AI çözümü veya uygulamaya otomatik yayın bu botun parçası değildir. İçerik, kaynak/izin ve doğruluk incelemesinden sonra uygulamaya ayrıca alınır.
