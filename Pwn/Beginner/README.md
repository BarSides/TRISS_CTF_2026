# Name

Will Call

## Author

@justinforbes

## Overview

The will-call window at Acrisure Stadium hands out tickets all day long. General admission is open to everyone, but the VIP field passes are supposed to stay locked behind the guest list. The clerk's little program reads the name on your reservation, then checks a "VIP" flag before it prints the good stuff. Trouble is, the name goes into a buffer that is only so big, and the VIP flag sits right next to it. Give them a name that is a little too long and watch where the extra letters land.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

The service listens on port 8012 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `EVENT_HOST:8012` (raw TCP, reach it with `nc`, not a web browser).

Attach `files/will_call` (the exact 64-bit Linux binary the server runs) and `files/will_call.c` (its source, included so new players can see the bug). The name is read into a 32-byte buffer followed by a 4-byte `vip` integer; any input longer than 32 bytes spills into `vip` and makes it non-zero, so the program prints the flag. The real flag lives in `flag.txt` next to the binary on the server only, so players develop the overflow locally (or just send it straight at the server over `nc`) and read the real flag from the live service.

`Dockerfile` copies the committed binary and serves it with `socat`, so the download is byte-for-byte what players attack. The flag can be changed by editing the `echo` line in the `Dockerfile`. Solution notes are in `Walkthrough.md`.

## Flag

BarSides{overflowed_onto_the_vip_list}
