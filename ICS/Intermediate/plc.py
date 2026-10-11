#!/usr/bin/env python3
"""Simulated Modbus/TCP PLC for the Lawrenceville Flood Gate (TRISS CTF 2026, ICS Intermediate).

Python standard library only. Read AND write: function codes 1-4 read,
5/6/15/16 write. The flag is only revealed once the gate is actually opened,
which the interlock blocks until the operator clears it the way the manual says.
"""
import os
import socketserver
import struct

FLAG = os.environ.get("FLAG", "BarSides{interlocks_are_only_as_strong_as_the_logic}")
PORT = int(os.environ.get("PORT", "502"))

# ---- process image -------------------------------------------------------
# Coils (FC 1/5/15)
#   0  gate open command      operator sets this to open the sluice gate
#   1  maintenance mode        must be ON before the gate will move
# Holding registers (FC 3/6/16)
#   0  gate position, percent  0 closed .. 100 open  (read-only effect)
#   1  local/remote key        must equal 0x1977 (remote) to accept a move
#   2  high-water alarm, 0.1ft
#   10 operator passcode entry  must be written with 1878
# Discrete inputs (FC 2): 0 power ok, 1 gate fully closed, 2 interlock tripped
coils = {0: 0, 1: 0}
holding = {0: 0, 1: 0x1977, 2: 214, 10: 0}

FLAG_BASE = 200  # flag appears in holding registers 200+ once the gate opens
NOTE_LEN = 64


def flag_regs():
    data = FLAG.encode()
    if len(data) % 2:
        data += b"\x00"
    regs = list(struct.unpack(">%dH" % (len(data) // 2), data))
    return regs + [0] * (NOTE_LEN - len(regs))


def gate_open():
    """The interlock: the gate only travels to 100% when every condition is met."""
    return (
        coils[1] == 1  # maintenance mode engaged
        and holding[1] == 0x1977  # key in REMOTE
        and holding[10] == 1878  # correct passcode entered
        and coils[0] == 1  # open command given
    )


def recompute():
    holding[0] = 100 if gate_open() else 0


def read_coil(a):
    if a in coils:
        return coils[a]
    return 0


def read_discrete(a):
    return {0: 1, 1: 1 if holding[0] == 0 else 0, 2: 0 if coils[1] else 1}.get(a, 0)


def read_holding(a):
    if a in holding:
        return holding[a]
    if gate_open() and FLAG_BASE <= a < FLAG_BASE + NOTE_LEN:
        return flag_regs()[a - FLAG_BASE]
    return 0


def read_input(a):
    return read_holding(a) if a < 3 else 0


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
                src = read_holding if fc == 3 else read_input
                body = b"".join(struct.pack(">H", src(a) & 0xFFFF) for a in range(start, start + count))
            return bytes([fc, len(body)]) + body

        if fc == 5:  # write single coil
            addr, val = struct.unpack(">HH", pdu[1:5])
            if addr not in coils:
                return bytes([fc | 0x80, 2])
            coils[addr] = 1 if val == 0xFF00 else 0
            recompute()
            return pdu[:5]

        if fc == 6:  # write single holding register
            addr, val = struct.unpack(">HH", pdu[1:5])
            if addr not in holding:
                return bytes([fc | 0x80, 2])
            holding[addr] = val
            recompute()
            return pdu[:5]

        if fc == 15:  # write multiple coils
            addr, count = struct.unpack(">HH", pdu[1:5])
            raw = pdu[6:]
            for i in range(count):
                if (addr + i) in coils:
                    coils[addr + i] = (raw[i // 8] >> (i % 8)) & 1
            recompute()
            return pdu[:5]

        if fc == 16:  # write multiple holding registers
            addr, count = struct.unpack(">HH", pdu[1:5])
            raw = pdu[6:]
            for i in range(count):
                if (addr + i) in holding:
                    holding[addr + i] = struct.unpack(">H", raw[2 * i:2 * i + 2])[0]
            recompute()
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
    print(f"Lawrenceville Flood Gate PLC listening on Modbus/TCP port {PORT}", flush=True)
    Server(("0.0.0.0", PORT), Handler).serve_forever()
