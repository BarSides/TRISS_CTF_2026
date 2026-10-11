#!/usr/bin/env python3
"""Reference solver: disassembles cheat.rom and recovers the cheat code.

Usage: python3 solve.py ../files/cheat.rom [--disasm]
Uses only what a player can learn from the emulator (opcode table) and the ROM.
"""
import sys

# opcode: (name, operand bytes)
ISA = {0x10: ("HALT", 0), 0x21: ("PRINT", 2), 0x32: ("READ", 0), 0x43: ("LDI", 2),
       0x54: ("LDIN", 2), 0x65: ("XOR", 1), 0x76: ("ADD", 1), 0x87: ("ROL", 2),
       0x98: ("MUL", 1), 0xA9: ("CHK", 2), 0xBA: ("MOV", 1), 0xCB: ("LEN", 1),
       0xDC: ("JERR", 2), 0xED: ("JMP", 2)}


def disasm(mem):
    pc, out = 0, []
    while pc < len(mem) and mem[pc] in ISA:
        name, n = ISA[mem[pc]]
        ops = mem[pc + 1:pc + 1 + n]
        out.append((pc, name, ops))
        pc += 1 + n
        if name == "HALT" and pc < len(mem) and mem[pc] not in ISA:
            break
    return out


def rol8(v, k):
    k &= 7
    return ((v << k) | (v >> ((8 - k) & 7))) & 0xFF


def solve(prog):
    """Symbolically walk the straight-line check and brute-force each character."""
    known = []                     # recovered characters, in order
    reg = [0, 0, 0, 0]
    pending = None                 # index of the character r0 was loaded from
    snapshot = None
    for _, name, ops in prog:
        if name == "LDI":
            reg[ops[0] & 3] = ops[1]
        elif name == "LDIN" and (ops[0] & 3) == 0:
            pending, snapshot, ops_after = ops[1], list(reg), []
            continue
        elif name == "LDIN":
            reg[ops[0] & 3] = known[ops[1]]
        if pending is None:
            continue
        if name != "CHK":
            ops_after.append((name, ops))
            continue
        # CHK r0, expected: try every byte for the pending character.
        for c in range(256):
            r = list(snapshot)
            r[0] = c
            for n, o in ops_after:
                d, s = (o[0] >> 4) & 3, o[0] & 3
                if n == "LDI": r[o[0] & 3] = o[1]
                elif n == "XOR": r[d] ^= r[s]
                elif n == "ADD": r[d] = (r[d] + r[s]) & 0xFF
                elif n == "MUL": r[d] = (r[d] * r[s]) & 0xFF
                elif n == "ROL": r[o[0] & 3] = rol8(r[o[0] & 3], o[1])
                elif n == "MOV": r[d] = r[s]
            if r[0] == ops[1]:
                known.append(c)
                reg = r
                break
        else:
            raise SystemExit(f"no byte satisfies character {pending}")
        pending = None
    return bytes(known).decode()


if __name__ == "__main__":
    rom = open(sys.argv[1], "rb").read()
    assert rom[:8] == b"STLBOX87"
    prog = disasm(rom[8:])
    if "--disasm" in sys.argv:
        for pc, name, ops in prog:
            print(f"{pc:04x}  {name:<5} {ops.hex(' ')}")
    print(solve(prog))
