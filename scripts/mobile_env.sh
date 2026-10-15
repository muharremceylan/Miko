#!/usr/bin/env bash
# Source this file in the current terminal; do not replace HOME.
export PATH="/workspace/.tools/flutter/bin:/workspace/.tools/android-sdk/platform-tools:$PATH"
export ANDROID_HOME=/workspace/.tools/android-sdk
export ANDROID_SDK_ROOT=/workspace/.tools/android-sdk
export ANDROID_USER_HOME=/workspace/.tools/android-user
export PUB_CACHE=/workspace/.tools/pub-cache
export GRADLE_USER_HOME=/workspace/.tools/gradle-cache
export XDG_CONFIG_HOME=/workspace/.tools/config
export XDG_CACHE_HOME=/workspace/.tools/cache
export GRADLE_OPTS="-Duser.home=/workspace/.tools/java-user"
mkdir -p "$PUB_CACHE" "$GRADLE_USER_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" /workspace/.tools/java-user
