/*
 * Blow on the Cartridge: TRISS CTF 2026, Rev Advanced.
 * Organizer source. Do not attach; players get the stripped emulator and cheat.rom.
 *
 * STEELBOX is a made-up 8-bit console. The emulator implements a small
 * custom instruction set; the cheat code check lives in the ROM, so players
 * reverse the emulator to learn the opcodes, then disassemble the ROM.
 *
 * ROM: "STLBOX87" magic, then code/data loaded at address 0, entry point 0.
 * Registers r0-r3 (8 bit), an error latch, a 16-bit pc, a 64-byte input line.
 * Operand byte for two-register ops is (rd << 4) | rs. Opcodes are listed in asm.py.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MEM_SIZE 4096
#define MAX_STEPS 100000

static unsigned char mem[MEM_SIZE];
static unsigned char reg[4];
static unsigned char err;
static unsigned char line[64];
static unsigned char line_len;

static unsigned char fetch(unsigned short *pc)
{
    if (*pc >= MEM_SIZE) {
        fputs("STEELBOX: bus error\n", stderr);
        exit(2);
    }
    return mem[(*pc)++];
}

static unsigned short fetch16(unsigned short *pc)
{
    unsigned short lo = fetch(pc);
    return (unsigned short)(lo | (fetch(pc) << 8));
}

static int run(void)
{
    unsigned short pc = 0;
    long steps;

    for (steps = 0; steps < MAX_STEPS; steps++) {
        unsigned char op = fetch(&pc), a, b;
        unsigned short addr;

        switch (op) {
        case 0x10:                                  /* HALT */
            return 0;
        case 0x21:                                  /* PRINT addr16 */
            addr = fetch16(&pc);
            while (addr < MEM_SIZE && mem[addr])
                putchar(mem[addr++]);
            fflush(stdout);
            break;
        case 0x32:                                  /* READ */
            if (!fgets((char *)line, sizeof(line), stdin))
                line[0] = '\0';
            line[strcspn((char *)line, "\r\n")] = '\0';
            line_len = (unsigned char)strlen((char *)line);
            break;
        case 0x43:                                  /* LDI r, imm8 */
            a = fetch(&pc);
            reg[a & 3] = fetch(&pc);
            break;
        case 0x54:                                  /* LDIN r, idx */
            a = fetch(&pc);
            b = fetch(&pc);
            reg[a & 3] = b < line_len ? line[b] : 0;
            break;
        case 0x65:                                  /* XOR rd, rs */
            a = fetch(&pc);
            reg[(a >> 4) & 3] ^= reg[a & 3];
            break;
        case 0x76:                                  /* ADD rd, rs */
            a = fetch(&pc);
            reg[(a >> 4) & 3] += reg[a & 3];
            break;
        case 0x87:                                  /* ROL r, imm3 */
            a = fetch(&pc);
            b = fetch(&pc) & 7;
            reg[a & 3] = (unsigned char)((reg[a & 3] << b) | (reg[a & 3] >> ((8 - b) & 7)));
            break;
        case 0x98:                                  /* MUL rd, rs */
            a = fetch(&pc);
            reg[(a >> 4) & 3] = (unsigned char)(reg[(a >> 4) & 3] * reg[a & 3]);
            break;
        case 0xA9:                                  /* CHK r, imm8: latch any difference */
            a = fetch(&pc);
            err |= reg[a & 3] ^ fetch(&pc);
            break;
        case 0xBA:                                  /* MOV rd, rs */
            a = fetch(&pc);
            reg[(a >> 4) & 3] = reg[a & 3];
            break;
        case 0xCB:                                  /* LEN r */
            a = fetch(&pc);
            reg[a & 3] = line_len;
            break;
        case 0xDC:                                  /* JERR addr16 */
            addr = fetch16(&pc);
            if (err)
                pc = addr;
            break;
        case 0xED:                                  /* JMP addr16 */
            pc = fetch16(&pc);
            break;
        default:
            fprintf(stderr, "STEELBOX: illegal opcode %02X at %04X\n", op, pc - 1);
            return 2;
        }
    }
    fputs("STEELBOX: watchdog reset\n", stderr);
    return 2;
}

int main(int argc, char **argv)
{
    FILE *f;
    unsigned char magic[8];
    size_t n;

    if (argc != 2) {
        fprintf(stderr, "usage: %s cartridge.rom\n", argv[0]);
        return 1;
    }
    f = fopen(argv[1], "rb");
    if (!f) {
        perror(argv[1]);
        return 1;
    }
    if (fread(magic, 1, 8, f) != 8 || memcmp(magic, "STLBOX87", 8) != 0) {
        fputs("STEELBOX: no cartridge detected. Try blowing on it.\n", stderr);
        return 1;
    }
    n = fread(mem, 1, MEM_SIZE, f);
    fclose(f);
    if (n == 0) {
        fputs("STEELBOX: empty cartridge\n", stderr);
        return 1;
    }
    return run();
}
