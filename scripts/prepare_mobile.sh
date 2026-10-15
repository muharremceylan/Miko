#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$repo_root/scripts/mobile_env.sh"
cd "$repo_root/apps/mobile"
# Generate missing platform hosts from the official SDK without overwriting Dart.
if [[ ! -f android/app/src/main/AndroidManifest.xml || ! -f ios/Runner/Info.plist ]]; then
  flutter --suppress-analytics create --empty --no-pub --platforms=android,ios --org=dev.akademiai --project-name=akademi_ai .
fi
python "$repo_root/scripts/configure_mobile_hosts.py"
if [[ -f pubspec.lock ]]; then
  flutter --suppress-analytics pub get --enforce-lockfile
else
  flutter --suppress-analytics pub get
fi
flutter --suppress-analytics analyze
flutter --suppress-analytics test
# Debug-only APK; it is not a store release or production-signed artifact.
flutter --suppress-analytics build apk --debug
