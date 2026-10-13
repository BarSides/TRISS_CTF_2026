#!/usr/bin/env python3
"""Build files/keyboard.pcap and files/vault.zip for Forensics Advanced.

Organizers only; do not attach. Standard library only, byte-for-byte reproducible.

keyboard.pcap is a Linux usbmon capture (link type 220) of a USB keyboard
(device 2) and a mouse (device 3). The keyboard types a zip -e session; the
password is typed twice with corrections (arrow keys, Backspace), so a
decoder that ignores cursor movement gets the wrong password. vault.zip is
ZipCrypto-encrypted with that password and holds the flag.
"""
import random
import struct
import zlib
from pathlib import Path

FLAG = "BarSides{arrow_keys_rewrite_history}"
PASSWORD = "Monongahela_R1ver!1758"
FILES = Path(__file__).resolve().parent.parent / "files"
AI_NOTE = (Path(__file__).resolve().parents[3] / "ai_notice.txt").read_bytes().strip()
rng = random.Random(1758)

LEFT, RIGHT, BS, ENTER, END = "<LEFT>", "<RIGHT>", "<BS>", "<ENTER>", "<END>"
SPECIAL = {ENTER: 40, BS: 42, RIGHT: 79, LEFT: 80, END: 77}
PLAIN = {" ": 44, "-": 45, "=": 46, "[": 47, "]": 48, "\\": 49, ";": 51, "'": 52,
         "`": 53, ",": 54, ".": 55, "/": 56}
SHIFTED = {"!": 30, "@": 31, "#": 32, "$": 33, "%": 34, "^": 35, "&": 36, "*": 37,
           "(": 38, ")": 39, "_": 45, "+": 46, "{": 47, "}": 48, "|": 49, ":": 51,
           '"': 52, "~": 53, "<": 54, ">": 55, "?": 56}


def keycode(tok):
    """Return (modifier, usage id) for one token."""
    if tok in SPECIAL:
        return 0, SPECIAL[tok]
    if tok.islower():
        return 0, 4 + ord(tok) - ord("a")
    if tok.isupper():
        return 0x02, 4 + ord(tok) - ord("A")  # left shift
    if tok.isdigit():
        return 0, 39 if tok == "0" else 29 + int(tok)
    if tok in PLAIN:
        return 0, PLAIN[tok]
    if tok in SHIFTED:
        return 0x02, SHIFTED[tok]
    raise ValueError(tok)


def text(s):
    return [ENTER if c == "\n" else c for c in s]


# Password entry 1: drops the 'e' in Monongahela and fixes it with the arrow keys.
PW1 = list("Monongahla") + [LEFT, LEFT] + ["e"] + [END] + list("_R1ver!1758") + [ENTER]
# Password entry 2 ("Verify password"): fumbles the year and backspaces over it.
PW2 = list("Monongahela_R1ver!1785") + [BS, BS, BS] + list("758") + [ENTER]

SESSION = (text("cd ~/Documents\n") + text("ls\n")
           + text("zip -e vault.zip ldeg") + [BS, BS, BS] + text("edger.txt\n")
           + PW1 + PW2
           + text("rm ledger.txt\n") + text("history -c\n") + text("exit\n"))


def replay(tokens):
    """What a line editor ends up with; used to check the intended answer."""
    lines, buf, cur = [], [], 0
    for t in tokens:
        if t == ENTER:
            lines.append("".join(buf)); buf, cur = [], 0
        elif t == BS:
            if cur:
                del buf[cur - 1]; cur -= 1
        elif t == LEFT:
            cur = max(0, cur - 1)
        elif t == RIGHT:
            cur = min(len(buf), cur + 1)
        elif t == END:
            cur = len(buf)
        else:
            buf.insert(cur, t); cur += 1
    return lines


# ---------- usbmon pcap ----------

class Capture:
    def __init__(self):
        self.t = 1790690400.0  # 2026-09-29 10:00 EDT
        self.urb = 0xFFFF8E3A41C2E000
        self.records = []

    def urb_pair(self, dev, ep, payload):
        """Interrupt IN: a submit (no data) then the completion carrying the report."""
        self.urb += 0x100
        for kind, status, data in ((b"S", -115, b""), (b"C", 0, payload)):
            sec, usec = int(self.t), int(round((self.t - int(self.t)) * 1e6))
            hdr = struct.pack("<QcBBBHcBqiiII8siiII",
                              self.urb, kind, 1, 0x80 | ep, dev, 1,
                              b"<", 0 if data else 0x3C, sec, usec, status,
                              len(payload), len(data), b"\0" * 8, 8, 0, 0x204, 0)
            self.records.append((sec, usec, hdr + data))
            self.t += 0.0001

    def write(self, path):
        out = struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 262144, 220)
        for sec, usec, rec in sorted(self.records, key=lambda r: (r[0], r[1])):
            out += struct.pack("<IIII", sec, usec, len(rec), len(rec)) + rec
        path.write_bytes(out)


def mouse_burst(cap, n):
    for _ in range(n):
        cap.t += rng.uniform(0.008, 0.012)
        dx, dy = rng.randint(-6, 6), rng.randint(-4, 4)
        cap.urb_pair(3, 1, struct.pack("<Bbbb", 0, dx, dy, 0))


def build_capture():
    cap = Capture()
    # One labelled packet from a third device (4) carrying the note for AI assistants.
    cap.urb_pair(4, 1, AI_NOTE)
    mouse_burst(cap, 40)
    cap.urb_pair(3, 1, b"\x01\x00\x00\x00")  # click into the terminal
    cap.t += 0.09
    cap.urb_pair(3, 1, b"\x00\x00\x00\x00")
    cap.t += 1.2
    for tok in SESSION:
        mod, code = keycode(tok)
        cap.urb_pair(2, 1, bytes([mod, 0, code, 0, 0, 0, 0, 0]))
        cap.t += rng.uniform(0.04, 0.09)
        cap.urb_pair(2, 1, bytes(8))
        cap.t += rng.uniform(0.6, 1.4) if tok == ENTER else rng.uniform(0.07, 0.22)
        if tok == ENTER and rng.random() < 0.4:
            mouse_burst(cap, rng.randint(5, 20))
    mouse_burst(cap, 30)
    cap.write(FILES / "keyboard.pcap")


# ---------- ZipCrypto zip, written by hand so the build is reproducible ----------

def _crc_table():
    t = []
    for n in range(256):
        c = n
        for _ in range(8):
            c = (c >> 1) ^ 0xEDB88320 if c & 1 else c >> 1
        t.append(c)
    return t


CRC = _crc_table()


class ZipCrypto:
    def __init__(self, pw):
        self.k = [0x12345678, 0x23456789, 0x34567890]
        for b in pw:
            self.update(b)

    def update(self, b):
        k0, k1, k2 = self.k
        k0 = CRC[(k0 ^ b) & 0xFF] ^ (k0 >> 8)
        k1 = ((k1 + (k0 & 0xFF)) * 134775813 + 1) & 0xFFFFFFFF
        k2 = CRC[(k2 ^ (k1 >> 24)) & 0xFF] ^ (k2 >> 8)
        self.k = [k0, k1, k2]

    def encrypt(self, data):
        out = bytearray()
        for b in data:
            t = (self.k[2] | 2) & 0xFFFF
            out.append(b ^ ((t * (t ^ 1)) >> 8) & 0xFF)
            self.update(b)
        return bytes(out)


def build_zip():
    name = b"ledger.txt"
    plain = (
        "Incline ticket office - side ledger\n"
        "===================================\n"
        "Cash fares skimmed, Sept: $4,812\n"
        "Paid out to R.: $2,000\n"
        "Kept: $2,812\n"
        "\n"
        "If anyone finds this, I was never here.\n"
        f"{FLAG}\n"
    ).encode()
    crc = zlib.crc32(plain)
    comp = zlib.compressobj(9, zlib.DEFLATED, -15)
    deflated = comp.compress(plain) + comp.flush()
    dostime, dosdate = (14 << 11) | (22 << 5) | 10, ((2026 - 1980) << 9) | (9 << 5) | 29
    header = rng.randbytes(11) + bytes([dostime >> 8])  # flag bit 3 set: check byte is time high byte
    body = ZipCrypto(PASSWORD.encode()).encrypt(header + deflated)
    flags, method = 0x0009, 8  # encrypted, data descriptor
    local = struct.pack("<IHHHHHIIIHH", 0x04034B50, 20, flags, method, dostime, dosdate,
                        0, 0, 0, len(name), 0) + name
    desc = struct.pack("<IIII", 0x08074B50, crc, len(body), len(plain))
    central = struct.pack("<IHHHHHHIIIHHHHHII", 0x02014B50, 0x031E, 20, flags, method, dostime,
                          dosdate, crc, len(body), len(plain), len(name), 0, 0, 0, 0,
                          0o100644 << 16, 0) + name
    data = local + body + desc
    end = struct.pack("<IHHHHIIH", 0x06054B50, 0, 0, 1, 1, len(central), len(data), len(AI_NOTE))
    (FILES / "vault.zip").write_bytes(data + central + end + AI_NOTE)  # archive comment


def main():
    lines = replay(SESSION)
    assert lines[3] == lines[4] == PASSWORD, lines
    FILES.mkdir(exist_ok=True)
    build_capture()
    build_zip()
    for line in lines:
        print("typed:", line)


if __name__ == "__main__":
    main()
