# Name

Pothole Patrol

## Author

@justinforbes

## Overview

Pittsburgh's pothole reporting app lets anyone file a crater and watch it join a repair queue that never moves. Version 2.3 shipped with a supervisor console for crew bosses, but the sign-in screen got cut, so nobody can open it. The repair authorization it shows is still inside the app, sealed so it won't turn up in a simple search.

Open the APK in jadx, find the console, and unseal the authorization yourself. No phone needed.

## Setup

File challenge. Attach `files/pothole_patrol.apk`. No device or emulator is needed, and running the app doesn't help, because nothing in the app calls the supervisor console. The flag is never in the APK as text. `SupervisorConsole` holds it as a `SEALED` byte array that is XORed with the `dispatch_key` string resource (`CRATER-CREW-412`, in `res/values/strings.xml`). Players read both out of jadx and undo the XOR in CyberChef (From Decimal, then XOR with a UTF8 key) or a few lines of Python.

Players need jadx (https://github.com/skylot/jadx, needs Java 11+), plus the local CyberChef or Python 3. Tell them to install jadx before arriving, since nothing can be downloaded at the venue.

`build/build.sh` rebuilds the APK from `build/app/` with the same pinned Android SDK Docker image as Mobile Beginner; the output is byte-for-byte reproducible and signed with the throwaway event key in `build/debug.keystore` (password `android`). Solution notes are in `Walkthrough.md`.

## Flag

BarSides{potholes_patched_at_runtime}
