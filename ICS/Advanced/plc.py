#!/usr/bin/env python3
"""Simulated Modbus/TCP PLC for the Point Bridge Vault (TRISS CTF 2026, ICS Advanced).

Python standard library only. The controller runs a small state-machine lock in
PLC logic. The exported program (vault_lock.scl) is given to players; they must
read it, compute the four-step entry code, and drive the state machine over
Modbus to release the flag. Any wrong entry resets the sequence.
"""
import os
import socketserver
import struct

FLAG = os.environ.get("FLAG", "BarSides{i_read_the_ladder_and_walked_right_in}")
PORT = int(os.environ.get("PORT", "502"))

# --- the lock logic, matching vault_lock.scl exactly ----------------------
SEED = 0x5A
STEP = 100
K = [0x12, 0x34, 0x56, 0x78]


def expected(i):
    return ((K[i] ^ SEED) + i * STEP) & 0xFFFF


# --- process image --------------------------------------------------------
# Coils:        0 RUN mode (must be 1 to accept entries), 1 reset sequence
# Holding regs: 30 entry register (write the code here, one step at a time)
#               40 current step (read-only: 0..4, 4 = unlocked)
# Discrete in:  0 power ok, 1 locked, 2 unlocked
coils = {0: 0, 1: 0}
holding = {30: 0, 40: 0}
state = {"step": 0}

FLAG_BASE = 200
NOTE_LEN = 64


def flag_regs():
    data = FLAG.encode()
    if len(data) % 2:
        data += b"\x00"
    regs = list(struct.unpack(">%dH" % (len(data) // 2), data))
    return regs + [0] * (NOTE_LEN - len(regs))


def feed(value):
    """Scan logic: process one entry write into HR[30]."""
    if coils[0] != 1:  # not in RUN
        state["step"] = 0
    elif state["step"] < 4 and value == expected(state["step"]):
        state["step"] += 1
    else:
        state["step"] = 0
    holding[40] = state["step"]


def unlocked():
    return state["step"] >= 4


def read_coil(a):
    return coils.get(a, 0)


def read_discrete(a):
    return {0: 1, 1: 0 if unlocked() else 1, 2: 1 if unlocked() else 0}.get(a, 0)


def read_holding(a):
    if a in holding:
        return holding[a]
    if unlocked() and FLAG_BASE <= a < FLAG_BASE + NOTE_LEN:
        return flag_regs()[a - FLAG_BASE]
    return 0


def pack_bits(bits):
    out = bytearray((len(bits) + 7) // 8)
    for i, b in enumerate(bits):
        if b:
            out[i // 8] |= 1 << (i % 8)
    return bytes(out)


def handle_pdu(pdu):
    fc = pdu[0]
    try:
        if fc in (1, 2, 3, 4):
            start, count = struct.unpack(">HH", pdu[1:5])
            limit = 2000 if fc in (1, 2) else 125
            if not 1 <= count <= limit:
                return bytes([fc | 0x80, 3])
            if start + count > 0x10000:
                return bytes([fc | 0x80, 2])
            if fc == 1:
                body = pack_bits([read_coil(a) for a in range(start, start + count)])
            elif fc == 2:
                body = pack_bits([read_discrete(a) for a in range(start, start + count)])
            else:
                src = read_holding if fc == 3 else (lambda a: read_holding(a) if a < 41 else 0)
                body = b"".join(struct.pack(">H", src(a) & 0xFFFF) for a in range(start, start + count))
            return bytes([fc, len(body)]) + body

        if fc == 5:
            addr, val = struct.unpack(">HH", pdu[1:5])
            if addr not in coils:
                return bytes([fc | 0x80, 2])
            coils[addr] = 1 if val == 0xFF00 else 0
            if addr == 1 and coils[1] == 1:  # reset button
                state["step"] = 0
                holding[40] = 0
                coils[1] = 0
            return pdu[:5]

        if fc == 6:
            addr, val = struct.unpack(">HH", pdu[1:5])
            if addr == 40:
                return bytes([fc | 0x80, 2])  # step counter is read-only
            if addr != 30:
                return bytes([fc | 0x80, 2])
            holding[30] = val
            feed(val)
            return pdu[:5]

        if fc == 16:
            addr, count = struct.unpack(">HH", pdu[1:5])
            raw = pdu[6:]
            for i in range(count):
                if (addr + i) == 30:
                    v = struct.unpack(">H", raw[2 * i:2 * i + 2])[0]
                    holding[30] = v
                    feed(v)
                elif (addr + i) == 40:
                    return bytes([fc | 0x80, 2])
            return pdu[:5]
    except struct.error:
        return bytes([fc | 0x80, 3])
    return bytes([fc | 0x80, 1])


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(60)
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
                self.request.sendall(struct.pack(">HHHB", tid, 0, len(reply) + 1, unit) + reply)
        except OSError:
            return

    def _read(self, n):
        buf = b""
        while len(buf) < n:
            c = self.request.recv(n - len(buf))
            if not c:
                return None
            buf += c
        return buf


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print(f"Point Bridge Vault PLC listening on Modbus/TCP port {PORT}", flush=True)
    Server(("0.0.0.0", PORT), Handler).serve_forever()
