# Name

Rigged Race

## Author

@justinforbes

## Overview

Somebody leaked the winner of Thursday's Great Pierogi Race before the race was even run. The stadium's security team pulled a packet capture from the in-game entertainment office around the time it happened.

Find out what was downloaded and recover the leaked results.

## Setup

Attach `files/stadium_office.pcap` as a CTFd download. No hosted service is needed. Players solve it with Wireshark (File > Export Objects > HTTP); `tshark --export-objects http,<dir>` or NetworkMiner also work.

The flag is drawn inside a PNG, so `strings` or `grep` on the capture does not find it. The image has to be pulled out of the HTTP traffic.

`build/make_capture.py` regenerates the capture byte for byte (Pillow and the DejaVu fonts required). It is for organizers only; do not attach it.

## Flag

BarSides{plain_http_spills_the_pierogies}
