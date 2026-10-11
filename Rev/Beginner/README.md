# Name

Skip the Line

## Author

@justinforbes

## Overview

The line for the Phantom's Revenge at Kennywood is 140 minutes long. The fast pass kiosk next to it just wants a code, and somebody left a copy of the kiosk program on a park laptop.

Find the fast pass code and print yourself a ride ticket.

The program runs on Linux (Kali, Ubuntu 22.04 or newer, or WSL). Run `chmod +x skip_the_line` first.

## Setup

Attach `files/skip_the_line` as a CTFd download. No hosted service is needed. It is a 64-bit Linux ELF, dynamically linked against glibc 2.34 or newer, with symbols kept so function names show up in Ghidra.

How it is built to teach the basics:

- `strings` shows a decoy test pass, `PHANTOM`, which the kiosk rejects with "switched off after the 2025 season".
- The real code is stored XORed with `0x5A`, so `strings` does not show it. It is decoded by `decode_fast_pass` just before a plain `strcmp`, so Ghidra, `ltrace` or a gdb breakpoint all reveal it.
- The flag is XORed with the code itself, so patching the comparison jump prints garbage instead of the flag.

`build/skip_the_line.c` is the source and `build/build.sh` rebuilds the binary with gcc; `build/gen.py` produces the encoded arrays. These are for organizers only; do not attach them.

## Flag

BarSides{skipped_the_line_at_kennywood}
