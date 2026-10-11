# Name

Pump Station Gossip

## Author

@justinforbes

## Overview

The Herrs Island Pump Station keeps the Allegheny out of the North Side's basements, and its PLC sits on the plant network talking Modbus/TCP to anyone who connects. The night operator swears they left a maintenance note "in the PLC" before going home. Connect to the PLC, read its registers, and find the note.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

The PLC listens on port 8007 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `EVENT_HOST:8007` (it is raw Modbus/TCP, not HTTP).

Attach `files/tag_list.csv` (the station's tag sheet) and `files/modbus_read.py` (a tiny Python 3 standard library Modbus client). Players can also use mbpoll, pymodbus, or Wireshark-style tools if they have them.

The tag sheet says the maintenance note lives in holding registers 40101-40164, two ASCII characters per register. Reading holding registers starting at address 100 returns the flag as 16-bit big-endian words; the hex column decodes with CyberChef's From Hex. `plc.py` is a read-only Modbus/TCP server (function codes 1-4, writes return "illegal function") in the Python standard library on Alpine, so it runs fully offline. The flag can be changed with the `FLAG` environment variable. Solution notes are in `Walkthrough.md`.

## Flag

BarSides{plcs_will_tell_anyone_who_asks}
