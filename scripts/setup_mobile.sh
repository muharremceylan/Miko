#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$repo_root/scripts/mobile_env.sh"
flutter_commit=abaf9c523780a608bd46686fd5e53740a07077f8
if [[ ! -d /workspace/.tools/flutter/.git ]]; then
  git clone --depth 1 --branch 3.47.7 https://github.com/flutter/flutter.git /workspace/.tools/flutter
fi
if [[ "$(git -C /workspace/.tools/flutter rev-parse HEAD)" != "$flutter_commit" ]]; then
  echo 'Flutter checkout differs from the pinned 3.47.7 SDK. Preserve it and review the toolchain instead of resetting it.' >&2
  exit 1
fi
# Official SDK tooling downloads Dart/engine artifacts using normal TLS verification.
# storage.googleapis.com must be enabled in environment network settings.
flutter --suppress-analytics --version
python "$repo_root/scripts/setup_android.py"
flutter --suppress-analytics config --android-sdk /workspace/.tools/android-sdk
flutter --suppress-analytics precache --android
cd "$repo_root/apps/mobile"
if [[ -f pubspec.lock ]]; then
  flutter --suppress-analytics pub get --enforce-lockfile
else
  flutter --suppress-analytics pub get
fi
