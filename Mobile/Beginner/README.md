# Name

Parking Chair

## Author

@justinforbes

## Overview

After every big snow, Pittsburgh's one true law kicks in: shovel out a spot, put a lawn chair in it, and it's yours. A guy on Dobson Street turned the tradition into an Android app. The chair on spot #14 only moves for the owner's code, and the receipt it prints when it moves is exactly what you're after.

You don't need a phone. An .apk is just a zip of compiled Java, so open it in jadx (jadx-gui) and read what the app is really doing.

## Setup

File challenge. Attach `files/parking_chair.apk`. No device or emulator is needed: players open the APK in jadx-gui, follow the button in `MainActivity` to `ChairLock`, and read the owner code (`SNOWMAGEDDON-2010`) and the flag straight out of the decompiled Java. Anyone who sideloads it on an Android 8+ phone can also type the code and get the flag on screen.

Players need jadx (https://github.com/skylot/jadx, needs Java 11+). Tell them to install it before arriving, since nothing can be downloaded at the venue.

`build/build.sh` rebuilds the APK from `build/app/` with the Android SDK in a pinned Docker image (aapt2, javac, d8, zipalign, apksigner, no Gradle); the output is byte-for-byte reproducible. It is signed with `build/debug.keystore`, a throwaway key made for this event (store and key password `android`). Solution notes are in `Walkthrough.md`.

## Flag

BarSides{the_chair_was_hardcoded}
