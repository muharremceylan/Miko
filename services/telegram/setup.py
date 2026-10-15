"""Yalnız sunucu terminalinde çalıştırılır; gizli değerler sohbete veya Git'e yazılmaz."""
import argparse
import getpass
import os
import re
import secrets
from pathlib import Path
from .config import Settings,ConfigurationError

def write_config(path,username,api_id,api_hash,token):
    path=Path(path)
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{4,31}',username) or not username.casefold().endswith('bot'):raise ValueError('Bot kullanıcı adı geçersiz.')
    values={'TELEGRAM_API_ID':api_id,'TELEGRAM_API_HASH':api_hash,'TELEGRAM_BOT_TOKEN':token,'BOT_PAIRING_CODE':secrets.token_urlsafe(24),'BOT_DATA_DIR':'/data','BOT_ENABLE_OCR':'1','BOT_MAX_FILE_MB':'250','BOT_PART_MB':'25','BOT_QUOTA_MB':'2048','BOT_MAX_PAGES':'1000','BOT_RETENTION_DAYS':'7'}
    Settings.from_environment(values)
    link=path.with_name('pairing-link.txt')
    if path.exists() or link.exists():raise FileExistsError('Mevcut ayar veya eşleştirme dosyası değiştirilmedi.')
    path.parent.mkdir(parents=True,exist_ok=True)
    # Sayılar/base64url/hex doğrulandığından env satırı veya Compose değişkeni enjekte edilemez.
    with open(path,'x',opener=lambda p,flags:os.open(p,flags,0o600)) as file:file.write('\n'.join(k+'='+v for k,v in values.items())+'\n')
    try:
        with open(link,'x',opener=lambda p,flags:os.open(p,flags,0o600)) as file:file.write('https://t.me/'+username+'?start='+values['BOT_PAIRING_CODE']+'\n')
    except Exception:path.unlink();raise
    return link

def main():
    parser=argparse.ArgumentParser(description='Sunucuda özel Telegram bot ayarlarını oluştur.');parser.add_argument('--output',default='services/telegram/.env');args=parser.parse_args()
    try:
        username=input('Bot kullanıcı adı (@ olmadan): ').strip().lstrip('@')
        api_id=input('Telegram API ID: ').strip();api_hash=getpass.getpass('Telegram API Hash (gizli): ').strip();token=getpass.getpass('BotFather token (gizli): ').strip()
        link=write_config(args.output,username,api_id,api_hash,token)
        print('Ayar dosyası oluşturuldu. Özel eşleştirme bağlantısı yalnız sunucudaki '+str(link)+' dosyasında; sohbete/Git’e gönderme.')
    except (ConfigurationError,ValueError,FileExistsError,EOFError) as error:print(str(error));return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
