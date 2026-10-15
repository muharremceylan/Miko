#!/usr/bin/env python3
"""Install official Android command-line tools, with repository checksum checks."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

root = Path('/workspace/.tools')
sdk = root / 'android-sdk'
tools = sdk / 'cmdline-tools' / '19.0'
archive_path = root / 'downloads' / 'commandlinetools-linux-13114758_latest.zip'
expected = '5fdcc763663eefb86a5b8879697aa6088b041e70'
if not (tools / 'bin/sdkmanager').exists():
    url = 'https://dl.google.com/android/repository/repository2-3.xml'
    with urllib.request.urlopen(url, timeout=60) as response:
        repository = ET.fromstring(response.read())
    package = next(p for p in repository if p.attrib.get('path') == 'cmdline-tools;19.0')
    archive = next(a for a in package.findall('archives/archive') if a.findtext('host-os') == 'linux')
    if archive.findtext('complete/checksum') != expected:
        raise RuntimeError('Official repository checksum differs from the pinned toolchain; review before updating.')
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    if not archive_path.exists():
        with urllib.request.urlopen('https://dl.google.com/android/repository/' + archive.findtext('complete/url'), timeout=60) as source, archive_path.open('wb') as dest:
            shutil.copyfileobj(source, dest)
    if hashlib.sha1(archive_path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Android tools checksum mismatch; do not use this archive.')
    temp = root / 'downloads' / 'android-tools-extracted'
    temp.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive_path) as z:
        for entry in z.infolist():
            if not (temp / entry.filename).resolve().is_relative_to(temp.resolve()):
                raise RuntimeError('Unsafe archive entry')
        z.extractall(temp)
    tools.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(temp / 'cmdline-tools'), str(tools))
    for p in (tools / 'bin').iterdir():
        p.chmod(p.stat().st_mode | 0o111)
os.environ['ANDROID_USER_HOME'] = str(root / 'android-user')
(root / 'android-user').mkdir(exist_ok=True)
manager = str(tools / 'bin/sdkmanager')
command = [manager, '--sdk_root=' + str(sdk)]
# SDK licenses are prerequisites of the requested Android development toolchain.
subprocess.run(command + ['--licenses'], input='y\n' * 100, text=True, check=True)
subprocess.run(command + ['platform-tools', 'platforms;android-36', 'build-tools;36.0.0', 'build-tools;35.0.0'], check=True)
print('Android SDK prerequisites installed at', sdk)
