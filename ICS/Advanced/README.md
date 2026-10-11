# Name

Crack the Vault

## Author

@justinforbes

## Overview

The Point Bridge Vault is guarded by a small combination lock that runs inside the PLC itself. Maintenance left behind an export of the controller's program. Read the logic, work out the four-step entry code, and drive the lock over Modbus to open the vault.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

The PLC listens on port 8009 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `EVENT_HOST:8009` (raw Modbus/TCP, not HTTP).

Attach `files/vault_lock.scl` (the exported PLC program, IEC 61131-3 Structured Text) and `files/modbus_client.py` (the read/write Modbus client). The challenge is reverse engineering: the program computes each step's expected value as `(K[i] XOR SEED) + i * STEP_GAIN` with `SEED = 0x5A`, `STEP_GAIN = 100`, `K = [0x12, 0x34, 0x56, 0x78]`, giving the code `[72, 210, 212, 334]`. Players set RUN (coil 1), write those four values in order to holding register 40031, and the step counter (40041) advances to 4, exposing the flag in registers 40201+. Any wrong value resets the sequence. `plc.py` is Python standard library on Alpine, so it runs fully offline. The flag can be changed with the `FLAG` environment variable. Solution notes are in `Walkthrough.md`.

## Flag

BarSides{i_read_the_ladder_and_walked_right_in}
