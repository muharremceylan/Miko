import os
import re
from dataclasses import dataclass, field
from pathlib import Path

class ConfigurationError(Exception):pass

@dataclass(frozen=True)
class Settings:
    api_id:int
    api_hash:str=field(repr=False)
    bot_token:str=field(repr=False)
    pairing_code:str=field(repr=False)
    data_dir:Path
    max_file_bytes:int=250*1024*1024
    part_bytes:int=25*1024*1024
    quota_bytes:int=2*1024*1024*1024
    max_pages:int=1000
    retention_days:int=7
    enable_ocr:bool=False
    job_timeout:int=1800

    @classmethod
    def from_environment(cls,env=None):
        env=os.environ if env is None else env
        needed=['TELEGRAM_API_ID','TELEGRAM_API_HASH','TELEGRAM_BOT_TOKEN','BOT_PAIRING_CODE']
        missing=[key for key in needed if not env.get(key)]
        if missing:raise ConfigurationError('Eksik ayarlar: '+', '.join(missing))
        try:
            if not re.fullmatch(r'[0-9]{1,12}',env['TELEGRAM_API_ID']) or int(env['TELEGRAM_API_ID'])<1:raise ValueError()
            if not re.fullmatch(r'[a-fA-F0-9]{32}',env['TELEGRAM_API_HASH']):raise ValueError()
            if not re.fullmatch(r'[0-9]{5,20}:[A-Za-z0-9_-]{20,100}',env['TELEGRAM_BOT_TOKEN']):raise ValueError()
            if not re.fullmatch(r'[A-Za-z0-9_-]{24,64}',env['BOT_PAIRING_CODE']):raise ValueError()
            limits={key:int(env.get(name,default)) for key,name,default in [
                ('max_file_bytes','BOT_MAX_FILE_MB',250),('part_bytes','BOT_PART_MB',25),('quota_bytes','BOT_QUOTA_MB',2048)]}
            if not 1<=limits['part_bytes']<=25 or not 1<=limits['max_file_bytes']<=500 or not limits['max_file_bytes']*4<=limits['quota_bytes']<=16384:raise ValueError()
            limits={key:value*1024*1024 for key,value in limits.items()}
            days=int(env.get('BOT_RETENTION_DAYS','7'));pages=int(env.get('BOT_MAX_PAGES','1000'));timeout=int(env.get('BOT_JOB_TIMEOUT','1800'))
            if not 1<=days<=30 or not 1<=pages<=2000 or not 30<=timeout<=3600 or env.get('BOT_ENABLE_OCR','0') not in ('0','1'):raise ValueError()
            return cls(int(env['TELEGRAM_API_ID']),env['TELEGRAM_API_HASH'],env['TELEGRAM_BOT_TOKEN'],env['BOT_PAIRING_CODE'],Path(env.get('BOT_DATA_DIR','/data')).resolve(),**limits,max_pages=pages,retention_days=days,enable_ocr=env.get('BOT_ENABLE_OCR','0')=='1',job_timeout=timeout)
        except (ValueError,TypeError):raise ConfigurationError('Telegram veya dosya sınırı ayarlarının biçimi geçersiz. Değerler günlüğe yazılmadı.') from None
