# Name

Ride All Day

## Author

@justinforbes

## Overview

Kennywood's gate staff scan ride-all-day wristbands with this app. After someone pulled the check out of last year's version with a decompiler, the night crew moved it into native code. Now the Java just hands your code to a C library and waits for a yes or no.

The only wristband code the gate accepts is the flag. Work out what the native check wants and run it backwards. No phone needed.

## Setup

File challenge. Attach `files/ride_all_day.apk`. In jadx, `Gate.scan(String)` is a `native` method loaded from `libwristband`. The APK carries that library for `arm64-v8a` and `x86_64` under `lib/`. Players unzip the APK, open `lib/x86_64/libwristband.so` (or the arm64 one) in Ghidra, and reverse `Java_org_barsides_rideallday_Gate_scan`. It checks that the input is 38 bytes long, then for each byte computes `rotl8(code[i] ^ "KENNYWD!"[i % 8], 3) + 17*i` and compares the result to a 38-byte table in `.rodata`. Inverting that per byte gives the flag. The flag never appears as text anywhere in the APK.

Players need jadx (https://github.com/skylot/jadx) and Ghidra (https://ghidra-sre.org), both needing Java, plus Python 3 or CyberChef for the inversion. Tell them to install these before arriving, since nothing can be downloaded at the venue.

`build/build.sh` compiles `build/native/wristband.c` freestanding (no NDK or libc, with a tiny hand-written JNI header) using clang and lld, then packages the APK with the same pinned Android SDK Docker image as the other Mobile challenges. The library is stripped and built at `-O1` without vectorizing, so the loop stays readable in Ghidra. The committed APK was built with Ubuntu clang 18.1.3 and is byte-for-byte reproducible with that version. `build/solve.py` is the reference solve, and solution notes are in `Walkthrough.md`.

## Flag

BarSides{native_code_still_rides_free}
