#!/usr/bin/env python3
"""Simulated Modbus/TCP PLC for the Herrs Island Pump Station (TRISS CTF 2026, ICS Beginner).

Python standard library only. Read-only: function codes 1-4 are answered,
anything else gets an "illegal function" exception.
"""
import os
import random
import socketserver
import struct
import time

FLAG = os.environ.get("FLAG", "BarSides{plcs_will_tell_anyone_who_asks}")
PORT = int(os.environ.get("PORT", "502"))

NOTE_START = 100
NOTE_LEN = 64  # registers reserved for the maintenance note

START = time.time()


def note_registers():
    data = FLAG.encode()
    if len(data) % 2:
        data += b"\x00"
    regs = list(struct.unpack(">%dH" % (len(data) // 2), data))
    return regs + [0] * (NOTE_LEN - len(regs))


NOTE = note_registers()


def holding(addr):
    """Holding registers, 40001-style address minus 40001."""
    t = time.time() - START
    if addr == 0:  # wet well level, tenths of a foot
        phase = (t / 20) % 2  # slow fill and drain between 12.0 and 15.0 ft
        return 120 + int(30 * (phase if phase < 1 else 2 - phase))
    if addr == 1:  # pump 1 speed, rpm
        return 1750 + random.randint(-5, 5)
    if addr == 2:  # pump 2 speed, rpm (standby)
        return 0
    if addr == 3:  # discharge pressure, psi x10
        return 642 + random.randint(-3, 3)
    if addr == 4:  # high level alarm setpoint, tenths of a foot
        return 180
    if addr == 5:  # low level cutoff, tenths of a foot
        return 60
    if NOTE_START <= addr < NOTE_START + NOTE_LEN:
        return NOTE[addr - NOTE_START]
    return 0


def inputs(addr):
    """Input registers mirror the analog values."""
    return holding(addr) if addr < 6 else 0


def coils(addr):
    return {0: 1, 1: 0, 2: 1}.get(addr, 0)  # pump 1 run, pump 2 run, intake gate open


def discretes(addr):
    return {0: 1, 1: 1, 2: 0}.get(addr, 0)  # power ok, door closed, high level alarm


def pack_bits(bits):
    out = bytearray((len(bits) + 7) // 8)
    for i, b in enumerate(bits):
        if b:
            out[i // 8] |= 1 << (i % 8)
    return bytes(out)


def handle_pdu(pdu):
    fc = pdu[0]
    if fc in (1, 2, 3, 4):
        if len(pdu) != 5:
            return bytes([fc | 0x80, 3])
        start, count = struct.unpack(">HH", pdu[1:5])
        limit = 2000 if fc in (1, 2) else 125
        if not 1 <= count <= limit:
            return bytes([fc | 0x80, 3])
        if start + count > 0x10000:
            return bytes([fc | 0x80, 2])
        if fc in (1, 2):
            src = coils if fc == 1 else discretes
            body = pack_bits([src(a) for a in range(start, start + count)])
        else:
            src = holding if fc == 3 else inputs
            body = b"".join(struct.pack(">H", src(a) & 0xFFFF) for a in range(start, start + count))
        return bytes([fc, len(body)]) + body
    return bytes([fc | 0x80, 1])  # this PLC is in RUN mode with writes locked


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        sock = self.request
        sock.settimeout(60)
        try:
            while True:
                hdr = self._read(7)
                if not hdr:
                    return
                tid, proto, length, unit = struct.unpack(">HHHB", hdr)
                if proto != 0 or not 2 <= length <= 254:
                    return
                pdu = self._read(length - 1)
                if not pdu:
                    return
                reply = handle_pdu(pdu)
                sock.sendall(struct.pack(">HHHB", tid, 0, len(reply) + 1, unit) + reply)
        except OSError:
            return

    def _read(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.request.recv(n - len(buf))
            if not chunk:
                return None
            buf += chunk
        return buf


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print(f"Herrs Island Pump Station PLC listening on Modbus/TCP port {PORT}", flush=True)
    Server(("0.0.0.0", PORT), Handler).serve_forever()
