#!/bin/sh
# Rebuilds files/towel_check (Linux x86-64, dynamically linked, stripped).
set -e
cd "$(dirname "$0")"
gcc -O1 -o ../files/towel_check towel_check.c
strip ../files/towel_check
chmod +x ../files/towel_check
