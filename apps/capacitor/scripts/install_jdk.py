#!/usr/bin/env python3
"""Download a pinned Temurin JDK from its official release and verify SHA-256."""
from pathlib import Path
import hashlib
import shutil
import tarfile
import urllib.request

root = Path('/workspace/.tools')
java = root / 'jdk21'
if (java / 'bin/javac').exists():
    print('Pinned JDK compiler already available.')
    raise SystemExit(0)
base = 'https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/'
name = 'OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz'
with urllib.request.urlopen(base + name + '.sha256.txt', timeout=60) as response:
    checksum = response.read().decode().split()[0]
if len(checksum) != 64 or any(c not in '0123456789abcdef' for c in checksum):
    raise RuntimeError('Invalid official checksum response')
archive = root / 'downloads' / name
archive.parent.mkdir(parents=True, exist_ok=True)
if not archive.exists():
    with urllib.request.urlopen(base + name, timeout=120) as source, archive.open('wb') as destination:
        shutil.copyfileobj(source, destination)
if hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest() != checksum:
    raise RuntimeError('JDK checksum mismatch; archive must not be used')
staging = root / 'downloads' / 'jdk21-extracted'
staging.mkdir(exist_ok=True)
with tarfile.open(archive) as tar:
    tar.extractall(staging, filter='data')
source = next(p for p in staging.iterdir() if (p / 'bin/javac').exists())
shutil.move(str(source), str(java))
print('Official Temurin JDK 21.0.12.1+1 installed and SHA-256 verified.')
