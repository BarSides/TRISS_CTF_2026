# Name

Keys to the Incline

## Author

@justinforbes

## Overview

The cash fares at the incline ticket office haven't added up for months. Investigators suspected the office manager and plugged a USB sniffer in between the office PC and its keyboard and mouse.

By the time they seized the PC, the evidence had been zipped up with a password and the original deleted. All they have is the sniffer's capture and the encrypted zip. What was in it?

## Setup

Attach `files/keyboard.pcap` and `files/vault.zip` as CTFd downloads. No hosted service is needed. Players need Wireshark or tshark to pull out the USB data and Python 3 (or patience and a HID usage table) to decode it. Any unzip tool that handles ZipCrypto opens the zip (`unzip`, 7-Zip, CyberChef **Unzip**, Python `zipfile`).

The capture is a Linux usbmon capture with a keyboard (device 2) and a mouse (device 3). The keyboard types a `zip -e vault.zip ledger.txt` session. The password `Monongahela_R1ver!1758` is typed twice: the first time with an `e` inserted using the Left Arrow and End keys, the second time with three Backspaces. Decoders that ignore cursor movement get `Monongahlae_R1ver!1758` for the first entry, which doesn't open the zip; the two entries disagreeing is the player's cue.

`build/make_capture.py` regenerates both files byte for byte (standard library only, including the ZipCrypto encryption). `build/solve.py` is a reference decoder. Both are for organizers only; do not attach them.

## Flag

BarSides{arrow_keys_rewrite_history}
