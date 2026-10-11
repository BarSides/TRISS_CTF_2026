#!/usr/bin/env python3
"""Tiny Modbus/TCP reader. Python 3 standard library only.

usage: python3 modbus_read.py HOST PORT TABLE START COUNT

TABLE is one of:
  coils      function code 1  (on/off outputs)
  discrete   function code 2  (on/off inputs)
  holding    function code 3  (16-bit read/write registers)
  input      function code 4  (16-bit read-only registers)

START is the zero-based address (holding register 40001 is address 0).
example: python3 modbus_read.py 10.0.0.5 8007 holding 0 6
"""
import socket
import struct
import sys

TABLES = {"coils": 1, "discrete": 2, "holding": 3, "input": 4}


def main():
    if len(sys.argv) != 6 or sys.argv[3] not in TABLES:
        sys.exit(__doc__)
    host, port, table = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    start, count = int(sys.argv[4]), int(sys.argv[5])
    fc = TABLES[table]

    with socket.create_connection((host, port), timeout=5) as s:
        s.sendall(struct.pack(">HHHBBHH", 1, 0, 6, 1, fc, start, count))
        hdr = s.recv(7)
        _, _, length, _ = struct.unpack(">HHHB", hdr)
        pdu = b""
        while len(pdu) < length - 1:
            pdu += s.recv(length - 1 - len(pdu))

    if pdu[0] & 0x80:
        sys.exit(f"PLC returned exception code {pdu[1]}")
    data = pdu[2:]
    if fc in (1, 2):
        for i in range(count):
            print(f"{start + i:5d}  {(data[i // 8] >> (i % 8)) & 1}")
    else:
        for i in range(count):
            (v,) = struct.unpack(">H", data[2 * i:2 * i + 2])
            print(f"{start + i:5d}  {v:5d}  0x{v:04x}")


if __name__ == "__main__":
    main()
