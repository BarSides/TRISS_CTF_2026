#!/usr/bin/env bash
# Rebuilds files/ride_all_day.apk from app/ and native/.
# The native library is built freestanding (no NDK) with the host's clang and lld for arm64-v8a and x86_64.
# The rest uses the Android SDK in a pinned Docker image (build-tools 34, platform android-34):
# aapt2 -> javac -> d8 -> zipalign -> apksigner, no Gradle. Needs Docker and Internet once to pull the image.
# The output is byte-for-byte reproducible with the same clang version (committed APK: Ubuntu clang 18.1.3).
set -euo pipefail
cd "$(dirname "$0")"

IMAGE="alvrme/alpine-android:android-34-jdk17@sha256:0ef01cdfd4000e119a09d30932fa06d0f179e2ffbda65855688f7ac6edc14d47"
OUT=../files/ride_all_day.apk

rm -rf out && mkdir -p out/lib/arm64-v8a out/lib/x86_64
for abi in arm64-v8a:aarch64 x86_64:x86_64; do
  clang --target="${abi#*:}-linux-android26" -O1 -fno-vectorize -fno-slp-vectorize -fno-unroll-loops \
    -ffreestanding -fno-stack-protector -fPIC -fvisibility=hidden -nostdlib -shared -fuse-ld=lld -s \
    -Wl,--hash-style=both -Wl,-z,max-page-size=16384 -Wl,--build-id=none -Wl,-soname,libwristband.so \
    -Wall -Wextra -Werror -o "out/lib/${abi%%:*}/libwristband.so" native/wristband.c
done

docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/w" -w /w "$IMAGE" sh -euc '
  BT=$ANDROID_HOME/build-tools/34.0.0
  JAR=$ANDROID_HOME/platforms/android-34/android.jar
  mkdir -p out/gen out/classes out/dex
  $BT/aapt2 compile --dir app/res -o out/res.zip
  $BT/aapt2 link -o out/base.apk -I $JAR --manifest app/AndroidManifest.xml --java out/gen out/res.zip
  find app/src out/gen -name "*.java" | sort > out/sources.txt
  javac -nowarn -Xlint:-options -source 8 -target 8 -bootclasspath $JAR -d out/classes @out/sources.txt
  $BT/d8 --release --min-api 26 --lib $JAR --output out/dex $(find out/classes -name "*.class" | sort)
  cp out/base.apk out/unsigned.apk
  (cd out/dex && touch -d "1981-01-01 00:00:00" classes.dex && $BT/aapt add -v ../unsigned.apk classes.dex >/dev/null)
  (cd out && touch -d "1981-01-01 00:00:00" lib/*/libwristband.so && $BT/aapt add -v unsigned.apk lib/arm64-v8a/libwristband.so lib/x86_64/libwristband.so >/dev/null)
  $BT/zipalign -f -p 4 out/unsigned.apk out/aligned.apk
  $BT/apksigner sign --ks debug.keystore --ks-pass pass:android --ks-key-alias barsides \
    --out out/signed.apk out/aligned.apk
  $BT/apksigner verify out/signed.apk
'
cp out/signed.apk "$OUT"
rm -rf out
sha256sum "$OUT"
