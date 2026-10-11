# Name

Open the Flood Gate

## Author

@justinforbes

## Overview

The Allegheny is cresting and the Lawrenceville flood gate is stuck closed because its safety interlock is tripped. The operator is off shift and left the manual behind. Clear the interlock and open the gate the way the manual says. The controller will post a maintenance release note once the gate actually moves.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

The PLC listens on port 8008 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `EVENT_HOST:8008` (raw Modbus/TCP, not HTTP).

Attach `files/operator_manual.txt` (the tag list and the gate-opening procedure) and `files/modbus_client.py` (a stdlib Python 3 Modbus client that can read and write). mbpoll or pymodbus also work.

This is a write challenge: players must send Modbus writes to engage maintenance mode (coil 2), enter passcode 1878 into holding register 40011, and set the open command (coil 1), after confirming the key switch reads REMOTE. Only when all four conditions hold does the PLC drive the gate to 100% and expose the flag in holding registers 40201+ (ASCII, two characters per register). `plc.py` is Python standard library on Alpine, read and write, so it runs fully offline. The flag can be changed with the `FLAG` environment variable. Solution notes are in `Walkthrough.md`.

## Flag

BarSides{interlocks_are_only_as_strong_as_the_logic}
