#!/usr/bin/env python3
"""Build the Android debug APK with the cloud machine's existing HTTPS proxy."""
from pathlib import Path
import os
import shlex
import subprocess
import urllib.parse

root = Path(__file__).resolve().parents[1]
env = os.environ.copy()
env['ANDROID_HOME'] = '/workspace/.tools/android-sdk'
env['ANDROID_SDK_ROOT'] = env['ANDROID_HOME']
env['ANDROID_USER_HOME'] = '/workspace/.tools/android-user'
env['JAVA_HOME'] = '/workspace/.tools/jdk21'
env['PATH'] = env['JAVA_HOME'] + '/bin:' + env.get('PATH', '')
env['GRADLE_USER_HOME'] = '/workspace/.tools/gradle-cache'
Path('/workspace/.tools/java-user').mkdir(parents=True, exist_ok=True)
args = ['./gradlew', '--no-daemon', '--max-workers=2', '-Duser.home=/workspace/.tools/java-user', '-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts', 'assembleDebug']
jvm = ['-Duser.home=/workspace/.tools/java-user', '-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts']
proxy = urllib.parse.urlsplit(env.get('HTTPS_PROXY') or env.get('https_proxy') or '')
if proxy.hostname:
    for protocol in ['http', 'https']:
        jvm += [f'-D{protocol}.proxyHost={proxy.hostname}', f'-D{protocol}.proxyPort={proxy.port or 80}']
    if proxy.username or proxy.password:
        raise RuntimeError('Authenticated Java proxy needs supported secure configuration; credentials are not copied to build files.')
env['JAVA_OPTS'] = env.get('JAVA_OPTS', '') + ' ' + shlex.join(jvm)
subprocess.run(args, cwd=root / 'android', env=env, check=True)
