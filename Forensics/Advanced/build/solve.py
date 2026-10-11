#!/usr/bin/env python3
"""Reference solver for Forensics Advanced: decode keyboard.pcap (organizers only).

Usage: python3 solve.py keyboard.pcap
Reads the usbmon capture, keeps 8-byte completions from device 2 (the
keyboard), and replays them through a tiny line editor that honours Shift,
Backspace, Left/Right, Home/End and Delete.
"""
import struct
import sys

LOWER = "abcdefghijklmnopqrstuvwxyz1234567890"
SHIFT_DIGITS = "!@#$%^&*()"
PUNCT = {44: (" ", " "), 45: ("-", "_"), 46: ("=", "+"), 47: ("[", "{"), 48: ("]", "}"),
         49: ("\\", "|"), 51: (";", ":"), 52: ("'", '"'), 53: ("`", "~"), 54: (",", "<"),
         55: (".", ">"), 56: ("/", "?")}


def reports(path):
    data = open(path, "rb").read()
    pos = 24
    while pos < len(data):
        _, _, incl, _ = struct.unpack_from("<IIII", data, pos)
        rec = data[pos + 16: pos + 16 + incl]
        pos += 16 + incl
        kind, dev, caplen = rec[8:9], rec[11], struct.unpack_from("<I", rec, 36)[0]
        if kind == b"C" and dev == 2 and caplen == 8:
            yield rec[64:72]


def decode(path):
    lines, buf, cur, held = [], [], 0, set()
    for r in reports(path):
        shift = r[0] & 0x22
        keys = [k for k in r[2:] if k]
        for k in keys:
            if k in held:
                continue
            if 4 <= k <= 39:
                ch = LOWER[k - 4]
                if shift:
                    ch = ch.upper() if ch.isalpha() else SHIFT_DIGITS[k - 30]
                buf.insert(cur, ch); cur += 1
            elif k in PUNCT:
                buf.insert(cur, PUNCT[k][1 if shift else 0]); cur += 1
            elif k == 40:
                lines.append("".join(buf)); buf, cur = [], 0
            elif k == 42 and cur:
                del buf[cur - 1]; cur -= 1
            elif k == 76 and cur < len(buf):
                del buf[cur]
            elif k == 80:
                cur = max(0, cur - 1)
            elif k == 79:
                cur = min(len(buf), cur + 1)
            elif k == 74:
                cur = 0
            elif k == 77:
                cur = len(buf)
        held = set(keys)
    return lines


if __name__ == "__main__":
    for line in decode(sys.argv[1]):
        print(line)
