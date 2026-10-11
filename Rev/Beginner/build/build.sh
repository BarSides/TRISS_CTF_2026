#!/bin/sh
# Rebuilds files/skip_the_line (Linux x86-64, dynamically linked, symbols kept).
set -e
cd "$(dirname "$0")"
gcc -O0 -fno-stack-protector -o ../files/skip_the_line skip_the_line.c
chmod +x ../files/skip_the_line
