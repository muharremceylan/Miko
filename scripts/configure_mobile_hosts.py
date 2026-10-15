#!/usr/bin/env python3
"""Apply only the required display name / permission metadata to generated hosts."""
from pathlib import Path
import plistlib
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1] / 'apps/mobile'
plist = root / 'ios/Runner/Info.plist'
if not plist.exists():
    raise RuntimeError('Generate mobile hosts with Flutter before configuring permissions.')
with plist.open('rb') as f:
    data = plistlib.load(f)
data['CFBundleDisplayName'] = 'Akademi AI'
data['NSCameraUsageDescription'] = 'Soru fotoğrafını çekmek için kamerana erişim gerekir. Bu demo fotoğrafı AI servisine göndermez.'
data['NSPhotoLibraryUsageDescription'] = 'Soru görselini seçmek için fotoğraf arşivine erişim gerekir.'
with plist.open('wb') as f:
    plistlib.dump(data, f, sort_keys=False)
manifest = root / 'android/app/src/main/AndroidManifest.xml'
namespace = 'http://schemas.android.com/apk/res/android'
ET.register_namespace('android', namespace)
tree = ET.parse(manifest)
app = tree.getroot().find('application')
app.set('{' + namespace + '}label', 'Akademi AI')
queries = tree.getroot().find('queries')
if queries is None:
    queries = ET.SubElement(tree.getroot(), 'queries')
action = 'android.intent.action.TTS_SERVICE'
if not any(e.get('{' + namespace + '}name') == action for e in queries.iter('action')):
    intent = ET.SubElement(queries, 'intent')
    ET.SubElement(intent, 'action', {'{' + namespace + '}name': action})
# image_picker uses the system camera/photo picker; no broad storage permission.
tree.write(manifest, encoding='utf-8', xml_declaration=True)
print('Android/iOS display name and permission descriptions configured.')
