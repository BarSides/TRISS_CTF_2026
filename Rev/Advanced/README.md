# Name

Blow on the Cartridge

## Author

@justinforbes

## Overview

Found in a Homestead basement: a STEELBOX 87, the 8-bit console nobody remembers, and a cartridge of "Mill Hunk 2: Return to Homestead". The game asks for a cheat code at the title screen. Legend says the code gives you 99 lives.

We dumped the cartridge to `cheat.rom` and wrote down the console's emulator, `steelbox`. The console's CPU is not anything you have seen before. Learn its instruction set from the emulator, read the cartridge, and recover the cheat code. The cheat code is the flag.

Run it on Linux (Kali, Ubuntu 22.04 or newer, or WSL): `./steelbox cheat.rom`

## Setup

Attach `files/steelbox` and `files/cheat.rom` as CTFd downloads. No hosted service is needed. `steelbox` is a stripped 64-bit Linux ELF (glibc 2.34 or newer).

This is a custom virtual machine challenge:

- `steelbox` is an interpreter for a made-up 14-instruction 8-bit CPU (four registers, an error latch, PRINT/READ for I/O). The opcode values are not sequential, so players have to read each switch case in Ghidra.
- `cheat.rom` holds the program. It checks the length, then for each character computes `ROL(c ^ previous, k) * m + a` (mod 256, `m` odd) with different constants per position, and latches any mismatch against an expected byte. Mismatches are latched, not branched on, so timing or instruction counting does not reveal which character is wrong.
- Neither file contains the flag. Players write a disassembler, then solve each character in order (brute force over 256 values, or invert the multiply with a modular inverse).

`build/steelbox.c` is the emulator source, `build/asm.py` assembles the ROM from the flag with fixed per-position constants (seed 1987), `build/build.sh` rebuilds both files byte for byte, and `build/solve.py` is the reference disassembler and solver. These are for organizers only; do not attach them.

## Flag

BarSides{eight_bit_cheat_codes_never_die}
