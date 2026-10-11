# Name

Twirl the Towel

## Author

@justinforbes

## Overview

Somebody made a "smart" Terrible Towel that won't twirl until you activate it, and the activation key is printed on a receipt nobody kept. All we have is the activation program.

The program checks your key without ever storing it. Figure out what it does to your key, run it backwards, and the key you recover is the flag.

The program runs on Linux (Kali, Ubuntu 22.04 or newer, or WSL).

## Setup

Attach `files/towel_check` as a CTFd download. No hosted service is needed. It is a stripped 64-bit Linux ELF (glibc 2.34 or newer).

What makes it a step up from Skip the Line:

- The binary is stripped, so players find the check by following string references in Ghidra.
- The key is the flag, and it is never stored. Each byte is rotated left 3, XORed with `TOWEL` (repeating), and has `7 * position` added, then compared with a 44-byte table. A wrong length fails before the loop.
- There is no `strcmp` for ltrace and nothing to read out of memory in gdb, so players have to understand the loop and invert it (usually a few lines of Python).

`build/towel_check.c` is the source, `build/build.sh` rebuilds the binary with gcc (byte for byte), `build/gen.py` produces the table and `build/solve.py` is the reference solver. These are for organizers only; do not attach them.

## Flag

BarSides{twirled_it_backwards_and_it_worked}
