# Name

Jumbotron

## Author

@justinforbes

## Overview

The scoreboard operator console at Acrisure Stadium puts whatever message you queue up on the jumbotron. The catch: it hands your message straight to `printf` with no format string of its own, so your input *is* the format string. The secret cheer (the flag) only lights up once a global override holds the operator code, and the normal path never sets it. Turn the console's own format-string bug into a write, set the override, then ask for the cheer.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

The service listens on port 8014 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `EVENT_HOST:8014` (raw TCP, reach it with `nc` or pwntools, not a web browser).

Attach `files/scoreboard` (the exact 64-bit Linux binary the server runs). The console loops: a message is printed with `printf(line)` (the bug), `flag` shows the flag only when the global `override` equals `1337`, and `quit` exits. Players leak the stack to find their input's argument offset (6), then use a format-string write (`%n`, easiest with pwntools `fmtstr_payload`) to store `1337` at `override`'s fixed address, and finally type `flag`. The binary is built `-fno-stack-protector -no-pie -O0`, so `override` sits at a fixed address and there is no canary. The real flag lives in `flag.txt` next to the binary on the server only. Source is kept at `scoreboard.c` (not attached). Solution notes are in `Walkthrough.md`.

## Flag

BarSides{the_jumbotron_reads_your_mind}
