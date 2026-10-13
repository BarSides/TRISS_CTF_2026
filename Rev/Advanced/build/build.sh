#!/bin/sh
# Rebuilds files/steelbox (Linux x86-64, stripped) and files/cheat.rom.
set -e
cd "$(dirname "$0")"
gcc -O1 -o ../files/steelbox steelbox.c
strip ../files/steelbox
# Unloaded section with the note for AI assistants (see ../../../ai_notice.txt); code and addresses are unchanged.
objcopy --add-section .note.ai_assistants=../../../ai_notice.txt --set-section-flags .note.ai_assistants=noload,readonly ../files/steelbox
chmod +x ../files/steelbox
python3 asm.py
