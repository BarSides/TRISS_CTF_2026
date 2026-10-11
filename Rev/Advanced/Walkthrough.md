# Blow on the Cartridge walkthrough

1. `./steelbox cheat.rom` shows a title screen and asks for a cheat code. Wrong codes print "GAME OVER". `strings` on both files shows the screen text and nothing else useful.
2. Open `steelbox` in Ghidra. `main` checks for the `STLBOX87` magic, reads up to 4096 bytes into a global buffer, and calls the interpreter: a loop that fetches a byte and switches on it.
3. Read each case and write down the instruction set. Two-register instructions take one byte, `(rd << 4) | rs`. Addresses are 16-bit little endian.

   | Opcode | Instruction | Effect |
   |---|---|---|
   | 10 | HALT | stop |
   | 21 aa aa | PRINT addr | print the string at addr |
   | 32 | READ | read a line of input |
   | 43 r ii | LDI r, imm | r = imm |
   | 54 r ii | LDIN r, idx | r = input[idx] |
   | 65 ds | XOR rd, rs | rd ^= rs |
   | 76 ds | ADD rd, rs | rd += rs |
   | 87 r k | ROL r, k | rotate r left by k |
   | 98 ds | MUL rd, rs | rd *= rs (mod 256) |
   | A9 r ii | CHK r, imm | error latch \|= r ^ imm |
   | BA ds | MOV rd, rs | rd = rs |
   | CB r | LEN r | r = input length |
   | DC aa aa | JERR addr | jump if the error latch is set |
   | ED aa aa | JMP addr | jump |

4. Write a disassembler for the ROM (skip the 8-byte header; code starts at address 0). The program is:

   ```
   PRINT banner ; READ
   LEN r0 ; CHK r0, 0x29          ; must be 41 characters
   JERR bad
   LDI r1, 0x42
   ; repeated 41 times with different constants:
   LDIN r0, i ; XOR r0, r1 ; ROL r0, k ; LDI r2, m ; MUL r0, r2 ; LDI r3, a ; ADD r0, r3
   CHK r0, expected ; LDIN r1, i
   JERR bad ; PRINT good ; HALT
   ```

5. Each character depends on the one before it (`r1`), starting from `0x42`. Solve them in order: for position `i`, try all 256 values of `c`, compute `ROL(c ^ prev, k) * m + a` mod 256, and keep the one equal to `expected`. (Or invert it: subtract `a`, multiply by the inverse of `m` mod 256, which exists because `m` is odd, rotate right by `k`, XOR with `prev`.)
6. `build/solve.py` does steps 4 and 5. Check the answer with `echo '<code>' | ./steelbox cheat.rom`.

Flag: `BarSides{eight_bit_cheat_codes_never_die}`
