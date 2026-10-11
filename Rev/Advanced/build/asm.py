#!/usr/bin/env python3
"""Assembles ../files/cheat.rom for the STEELBOX emulator (organizers only).

The ROM reads a cheat code and checks it one character at a time:

    r1 = 0x42
    for i, c in enumerate(code):
        r0 = ROL(c ^ r1, k[i]) * m[i] + a[i]     (all mod 256, m[i] odd)
        CHK r0, e[i]                             (latches any difference)
        r1 = c

Errors are latched, not branched on, so counting instructions does not leak
which character was wrong. Per-position constants come from a fixed seed, so
the ROM rebuilds byte for byte.
"""
import random
from pathlib import Path

FLAG = b"BarSides{eight_bit_cheat_codes_never_die}"
SEED = 1987

OP = dict(HALT=0x10, PRINT=0x21, READ=0x32, LDI=0x43, LDIN=0x54, XOR=0x65, ADD=0x76,
          ROL=0x87, MUL=0x98, CHK=0xA9, MOV=0xBA, LEN=0xCB, JERR=0xDC, JMP=0xED)

BANNER = (b"\n  ####  STEELBOX 87  ####\n"
          b"  MILL HUNK 2: RETURN TO HOMESTEAD\n"
          b"  (C) 1987 ALLEGHENY SOFTWORKS\n\n"
          b"  PRESS START... ENTER CHEAT CODE: \0")
GOOD = b"\n  CHEAT ACCEPTED! 99 LIVES. THE CODE YOU ENTERED IS YOUR FLAG.\n\0"
BAD = b"\n  NOTHING HAPPENS. GAME OVER.\n\0"


def rol8(v, k):
    return ((v << k) | (v >> (8 - k))) & 0xFF


def params():
    rng = random.Random(SEED)
    for _ in FLAG:
        yield rng.randint(1, 7), rng.randrange(1, 256, 2), rng.randrange(256)


def build():
    code = bytearray()
    fixups = []  # (offset, label)

    def emit(*bs):
        code.extend(bs)

    def addr(label):
        fixups.append((len(code), label))
        emit(0, 0)

    emit(OP["PRINT"]); addr("banner")
    emit(OP["READ"])
    emit(OP["LEN"], 0); emit(OP["CHK"], 0, len(FLAG))
    emit(OP["JERR"]); addr("bad")
    emit(OP["LDI"], 1, 0x42)

    prev = 0x42
    for i, (k, m, a) in enumerate(params()):
        c = FLAG[i]
        e = (rol8(c ^ prev, k) * m + a) & 0xFF
        emit(OP["LDIN"], 0, i)
        emit(OP["XOR"], 0x01)          # r0 ^= r1
        emit(OP["ROL"], 0, k)
        emit(OP["LDI"], 2, m)
        emit(OP["MUL"], 0x02)          # r0 *= r2
        emit(OP["LDI"], 3, a)
        emit(OP["ADD"], 0x03)          # r0 += r3
        emit(OP["CHK"], 0, e)
        emit(OP["LDIN"], 1, i)         # r1 = this character, chains into the next
        prev = c

    emit(OP["JERR"]); addr("bad")
    emit(OP["PRINT"]); addr("good")
    emit(OP["HALT"])
    labels = {}
    labels["bad"] = len(code); emit(OP["PRINT"]); addr("bad_msg"); emit(OP["HALT"])
    for name, text in (("banner", BANNER), ("good", GOOD), ("bad_msg", BAD)):
        labels[name] = len(code)
        code.extend(text)
    for off, label in fixups:
        code[off:off + 2] = labels[label].to_bytes(2, "little")
    return b"STLBOX87" + bytes(code)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "files" / "cheat.rom"
    rom = build()
    out.write_bytes(rom)
    print(f"wrote {out} ({len(rom)} bytes)")
