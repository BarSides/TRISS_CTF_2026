#!/usr/bin/env python3
"""Reference solver for Scatter Shot: brute-force the 4-digit PIN.

Usage: python3 solve.py ../files/voicemail.wav
Standard library only. Re-implements scatter.py's PRNG rather than importing
it, the way a player would.
"""
import sys
import wave


def xorshift(seed):
    x = seed & 0xFFFFFFFF or 0x1BADB002
    while True:
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        yield x


def positions(pin, n):
    used = set()
    for r in xorshift((pin * 2654435761 ^ 0x5EED5EED) & 0xFFFFFFFF):
        i = r % n
        if i not in used:
            used.add(i)
            yield i


def read(frames, pos, nbytes):
    out = bytearray()
    for _ in range(nbytes):
        b = 0
        for _ in range(8):
            b = (b << 1) | (frames[2 * next(pos)] & 1)
        out.append(b)
    return bytes(out)


def main():
    with wave.open(sys.argv[1], "rb") as w:
        frames = w.readframes(w.getnframes())
    n = len(frames) // 2
    for pin in range(10000):
        pos = positions(pin, n)
        length = int.from_bytes(read(frames, pos, 2), "big")
        if length > 200 or read(frames, pos, 9) != b"BarSides{":
            continue
        pos = positions(pin, n)
        read(frames, pos, 2)
        print(f"PIN {pin:04d}: {read(frames, pos, length).decode()}")
        return
    print("no PIN found")


if __name__ == "__main__":
    main()
