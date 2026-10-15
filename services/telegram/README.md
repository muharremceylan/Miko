# Telegram PDF aktarım servisi

Akademi AI için tek sahipli, özel sohbetten PDF kabul eden bağımsız Python servisi. iPhone yönlendirmeleri: [adım adım rehber](../../TELEGRAM_IOS_SETUP.md).

## Akış ve sınırlar

```text
iPhone → kendi botuna PDF ilet
      → özel sohbet + sahiplik + tür/boyut + disk kontrolü
      → kalıcı iş kaydı → tek işçi kuyruğu → özel diske indir
      → sınırlı ayrı süreçte PDF bölme + metin/Türkçe OCR
      → needs-review manifesti → sahibine PDF parçaları/metin
      → kaynak/izin ve uzman incelemesi (henüz otomatik değil)
```

Telethon ile **MTProto bot oturumu** kullanılır. Standart bulut Bot API dosya indirmesindeki 20 MB sınırına bağlı değildir; bağlantı kendi API ID/Hash ve BotFather token’ıyla yapılır. `TelegramClient.start()` veya kişisel telefon/OTP girişi kullanılmaz. Oturumun bot kimliği token’daki kimlikle karşılaştırılır. Alan adı, webhook veya dışarı açılan port gerekmez; Telegram veri merkezlerine giden bağlantı gerekir. Bu yöntem Telegram’ın hesap ve sunucu kısıtlarını kaldırmaz.

Varsayılan kaynak 250 MiB / 1000 sayfa; parçalar en çok 25 MiB; özel işler için 2 GiB yumuşak disk kotası; sıra kapasitesi 3 bekleyen + 1 çalışan iş; tek işçi; 7 gün saklama. Bir PDF önce iki sayfa aralığına bölünür, büyük parçalar yeniden bölünür; tek sayfa sınırı aşıyorsa işlem durur. Kaynak sayfa numaraları ve SHA-256 manifestte korunur. Şifreli/bozuk PDF reddedilir. OCR başarısızsa iş başarısız işaretlenir; yeniden gönderilebilir. Kalın taramalarda varsayılan süre/kaynak sınırları pilotta ayarlanabilir.

## Sunucuda kurulum

Docker Engine + Compose v2 ve Git bulunan, kalıcı diski olan bir Linux sunucu kullan. Pilot için 2 GB RAM ve birkaç GB boş alanla başla. Servis konteyneri 1 GB RAM / 1 CPU ile sınırlıdır; işletim sistemi ve Docker ayrıca kaynak kullanır. Buradaki testler sunucu satın alındığını veya botun canlı olduğunu göstermez.

```bash
git clone https://github.com/muharremceylan/Miko.git
cd Miko
```

Gizli yapılandırmayı **yalnız sunucu terminalinde** oluştur. iPhone’da sunucu sağlayıcının web konsolu kullanılabilir. Aşağıdaki yardımcı bot kullanıcı adı, API ID, gizli API Hash ve gizli token sorar; son iki alan terminalde görünmez. Önceden boş `.env` oluşturma; yardımcı mevcut dosyanın üzerine yazmaz.

```bash
docker build -t akademi-telegram:local -f services/telegram/Dockerfile .
docker run --rm -it --network none --read-only \
  --user "$(id -u):$(id -g)" \
  --volume "$PWD/services/telegram:/config" \
  akademi-telegram:local python -m services.telegram.setup --output /config/.env
```

Bu yardımcı ağ bağlantısı kurmaz. Var olan gerçek ayarı asla silme. Yardımcı `.env` ve `pairing-link.txt` dosyalarını 0600 izinle oluşturur ve üzerine yazmaz. Bu iki dosya Git/Docker build kapsamından hariçtir.

> Komut sırası: `git clone` → `cd Miko` → `docker build` → yukarıdaki `docker run ...setup` → aşağıdaki Compose kontrol/başlatma. Bu işlem kişisel Telegram hesabında oturum açmaz.

```bash
docker compose -f services/telegram/compose.yaml config --quiet
docker compose -f services/telegram/compose.yaml run --rm --no-deps telegram-pdf \
  python -m services.telegram.bot --check
docker compose -f services/telegram/compose.yaml up -d --build
docker compose -f services/telegram/compose.yaml ps
docker compose -f services/telegram/compose.yaml logs --tail 30 telegram-pdf
```

`--check` yalnız ayar biçimini doğrular; Telegram bağlantısı test edilmiş sayılmaz. Gerçek başlatmadan sonra logda “Bot bağlandı” ve sağlık durumunda `healthy` görülmeli. Sunucudaki `services/telegram/pairing-link.txt` içindeki özel bağlantıyı güvenli şekilde iPhone’da aç; Başlat’a dokun. Bağlantıyı veya `.env` içeriğini paylaşma. Önce kendi küçük, izinli PDF’nle; ardından boyut sınırları içindeki büyük taramayla gerçek pilotu tamamla.

## Ayarlar

| Değişken | Değer / varsayılan |
|---|---|
| `TELEGRAM_API_ID`, `TELEGRAM_API_HASH` | my.telegram.org → API development tools; yalnız sunucuda |
| `TELEGRAM_BOT_TOKEN` | BotFather; yalnız sunucuda |
| `BOT_PAIRING_CODE` | Yardımcı rastgele üretir; 24–64 karakter |
| `BOT_DATA_DIR` | `/data`; özel kalıcı volume |
| `BOT_ENABLE_OCR` | Docker örneği/yardımcı `1`; ayarlanmazsa Python varsayılanı `0` |
| `BOT_MAX_FILE_MB` | `250`; MiB biriminde, izin verilen 1–500 |
| `BOT_PART_MB` | `25`; MiB biriminde, izin verilen 1–25 |
| `BOT_QUOTA_MB` | `2048`; kaynak sınırının en az 4 katı, en çok 16384 MiB |
| `BOT_MAX_PAGES` | `1000`; 1–2000 |
| `BOT_RETENTION_DAYS` | `7`; 1–30 |
| `BOT_JOB_TIMEOUT` | `1800` saniye; 30–3600 |

Dosya alanı hesabı PDF iş klasörlerini kapsar; işletim sistemi, SQLite, geçici OCR ve yedekler için ayrıca alan gerekir. PDF alt süreci 768 MiB adres alanı ve 300 CPU saniyesi ile sınırlıdır; OCR alt komutlarının da süre/çözünürlük sınırı vardır. İş süresi, CPU sınırı veya konteyner kaynak sınırı aşılırsa işi daha küçük PDF’lerle tekrar dene. Bunlar genel amaçlı zararlı belge tarayıcısı sınırları değildir.

## Güvenlik ve veri yaşam döngüsü

- Yalnız ilk doğru eşleştirme kodunu kullanan özel sohbet sahibi kabul edilir. Grup/kanal mesajları ve diğer kişiler dosya indirmeyi başlatamaz. Kod denemeleri sınırlandırılır. Kurulum bağlantısı sızarsa sunucuyu durdurup güvenli yeniden eşleştirme gerekir; çalışan botta sahip değiştirme komutu yoktur.
- Telegram’dan gelen dosya adları disk yolu yapılmaz. Belgelerdeki yönergeler ve iletilen mesajlar komut olarak çalıştırılmaz; dosya açıklaması `/sil` vb. komut tetiklemez. PDF/OCR metni yalnız veridir; AI’ye otomatik verilmez.
- Dosyalar `original.pdf` ve iş koduna bağlı özel dizinlerde tutulur. İndirmenin gerçek boyutu da kontrol edilir. PDF işleme ayrı süreçtedir; bilinen sayfa/annotation JavaScript/Launch/SubmitForm/ImportData aksiyonları çıktıdan kaldırılır. Bu işlem tam PDF güvenlik temizleyicisi değildir; güncel bağımlılıklar ve container sınırları korunmalıdır.
- Konteyner root değildir; kök dosya sistemi salt okunur, yetkileri düşürülmüş, belleği/süreçleri sınırlıdır. Dışarıya port açmaz. Metin veya dosya içerikleri, token, hata nesneleri ve oturum sırları loglanmaz.
- `telegram-data` volume’u PDF’leri, `bot.sqlite3` iş/sahip kaydını ve **`telegram.session` yetkilendirmesini** içerir. Volume, `.env`, eşleştirme bağlantısı ve bunların yedekleri gizlidir. Sunucunun yetkili yöneticileri diski okuyabilir; ayrıca disk şifreleme/yedekleme politikası uygulanabilir. Bu dosyaları web köküne/GitHub’a koyma.
- `/sil İŞ_KODU` kaynak/parça/metni ve içerik hash/manifest kaydını kaldırır; minimal iş kodu, sahip kimliği, ders, zaman ve silinme durumu kalır. Saklama süresi dolan terminal işler saatte bir temizlenir. Telegram’a gönderilmiş kopyalar ve sunucu yedekleri ayrıca yönetilir.
- Yeniden başlatmada tamamlanmış işler korunur. Yarım işler “başarısız” olur, yarım indirme temizlenir; dosyayı tekrar iletmek gerekir. Gönderim başarısız olursa hazır çıktı korunur ve `/parcalar` veya `/metin` ile yeniden istenir.
- `docker compose down` volume’u korur. `down -v` **PDF’ler, bot oturumu ve sahip eşleşmesi dahil kalıcı veriyi siler**; rutin durdurma için kullanma.

## Yerel ve CI doğrulama

```bash
python3 -m venv /tmp/akademi-telegram-venv
/tmp/akademi-telegram-venv/bin/python -m pip install -r services/telegram/requirements.txt
/tmp/akademi-telegram-venv/bin/python -m unittest services.telegram.test_telegram -v
```

OCR testi için `pdftoppm`, `tesseract` ve Türkçe `tur.traineddata` gerekir. Docker imajı üçünü de içerir. CI gerçek imajı üretir ve testleri **ağ kapalı** çalıştırır:

```bash
docker build -t akademi-telegram:test -f services/telegram/Dockerfile .
docker run --rm --network none --read-only --tmpfs /tmp:rw,size=512m \
  akademi-telegram:test python -m unittest services.telegram.test_telegram -v
```

Testler gerçek Telegram API’sine bağlanmaz; sahte iletim adaptörü ve özgün PDF/raster fikstürleri kullanır. 32 MiB üstü kaynak → 25 MiB altı parçalar, tam sayfa kapsamı, gerçek Türkçe OCR motoru, yetkilendirme, komut enjeksiyonu sınırı, boyut, yeniden başlatma, saklama/silme ve hata sonrası devam davranışları kapsanır. Başarılı yerel/CI testleri **gerçek Telegram bağlantısı, sunucu yayını veya tüm ders notlarının içeriğinin onayı değildir**. Canlı pilot bu hesap/sunucu bilgileri sağlandıktan sonra yapılmalıdır.

Referanslar: [Telegram botları](https://core.telegram.org/bots), [Telegram uygulama bilgileri](https://core.telegram.org/api/obtaining_api_id), [Telethon bot hesabı girişi](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in-as-a-bot). Bağımlılıklar `requirements.txt` içinde sürüme sabittir.
