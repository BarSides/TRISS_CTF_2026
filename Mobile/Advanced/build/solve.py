#!/usr/bin/env python3
"""Reference solve for Ride All Day: undo the native wristband check.

check (from libwristband.so): x = code[i] ^ PUNCH[i % 8]; x = rotl8(x, 3); x = (x + 17*i) & 0xff; x must equal EXPECTED[i]
"""
PUNCH = b"KENNYWD!"
EXPECTED = bytes.fromhex(
    "4832031bc5ee6f0909f2238c4de6f7f25172839c8486f7c9d1f242ac5d8607a1c04a23ac45c6"
)


def rotr8(x, n):
    return ((x >> n) | (x << (8 - n))) & 0xFF


print("".join(chr(rotr8((e - 17 * i) & 0xFF, 3) ^ PUNCH[i % 8]) for i, e in enumerate(EXPECTED)))
