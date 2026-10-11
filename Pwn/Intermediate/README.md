# Name

Skybox

## Author

@justinforbes

## Overview

The suite level at Acrisure Stadium has its own access terminal: punch in your code and it decides whether you belong up there. The code goes into a fixed-size buffer with no bounds check, so a long enough entry runs right off the end and over the address the program planned to return to. Somewhere in the binary is an `open_skybox` routine that the normal path never calls. Point the return address at it and the suite is yours.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

The service listens on port 8013 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `EVENT_HOST:8013` (raw TCP, reach it with `nc` or pwntools, not a web browser).

Attach `files/skybox` (the exact 64-bit Linux binary the server runs). Players find the address of `open_skybox` with `nm`, `objdump`, or Ghidra, work out that the return address sits 72 bytes into the input, and overwrite it. The binary is built `-fno-stack-protector -no-pie -O0`, so there is no stack canary and `open_skybox` lives at a fixed address; `open_skybox` is marked `force_align_arg_pointer` so a straight return into it works without a separate alignment gadget. The real flag lives in `flag.txt` next to the binary on the server only. Source is kept at `skybox.c` (not attached). Solution notes are in `Walkthrough.md`.

## Flag

BarSides{returned_to_the_skybox}
