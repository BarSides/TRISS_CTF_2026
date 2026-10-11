#!/bin/sh
# Rebuilds files/steelbox (Linux x86-64, stripped) and files/cheat.rom.
set -e
cd "$(dirname "$0")"
gcc -O1 -o ../files/steelbox steelbox.c
strip ../files/steelbox
chmod +x ../files/steelbox
python3 asm.py
