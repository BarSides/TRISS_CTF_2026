/*
 * Skip the Line: TRISS CTF 2026, Rev Beginner.
 * Organizer source. Do not attach; players get only the compiled binary.
 *
 * The fast-pass code is stored XORed with 0x5A so `strings` does not show it,
 * and the flag is XORed with the code itself, so patching the check prints garbage.
 * Encoded arrays come from gen.py.
 */
#include <stdio.h>
#include <string.h>

#define KEY 0x5A

/* Old test pass left in by a lazy developer. `strings` finds this one. */
static const char *TEST_PASS = "PHANTOM";

static const unsigned char encoded_code[] = {
    0x11, 0x1f, 0x14, 0x14, 0x03, 0x0d, 0x15, 0x15, 0x1e, 0x6b, 0x62, 0x63, 0x62
};

static const unsigned char encoded_flag[] = {
    0x09, 0x24, 0x3c, 0x1d, 0x30, 0x33, 0x2a, 0x3c, 0x3f, 0x42, 0x53, 0x50, 0x48,
    0x3b, 0x20, 0x2a, 0x11, 0x2d, 0x3f, 0x2a, 0x10, 0x28, 0x58, 0x56, 0x5c, 0x67,
    0x2a, 0x31, 0x11, 0x25, 0x3c, 0x39, 0x21, 0x36, 0x33, 0x5e, 0x57, 0x5d, 0x45
};

void decode_fast_pass(char *out)
{
    size_t i;
    for (i = 0; i < sizeof(encoded_code); i++)
        out[i] = encoded_code[i] ^ KEY;
    out[i] = '\0';
}

void print_ride_ticket(const char *code)
{
    size_t n = strlen(code);
    char flag[sizeof(encoded_flag) + 1];
    size_t i;
    for (i = 0; i < sizeof(encoded_flag); i++)
        flag[i] = encoded_flag[i] ^ code[i % n];
    flag[i] = '\0';
    printf("\n  *** FAST PASS ACCEPTED ***\n  Your ride ticket: %s\n\n", flag);
}

int main(void)
{
    char input[64];
    char fast_pass[sizeof(encoded_code) + 1];

    puts("==============================================");
    puts("   KENNYWOOD FAST PASS KIOSK  (ride: Phantom)  ");
    puts("   Wait time in the regular line: 140 minutes  ");
    puts("==============================================");
    printf("Enter your fast pass code: ");
    fflush(stdout);

    if (!fgets(input, sizeof(input), stdin))
        return 1;
    input[strcspn(input, "\r\n")] = '\0';

    if (strcmp(input, TEST_PASS) == 0) {
        puts("That test pass was switched off after the 2025 season. Nice try.");
        return 1;
    }

    decode_fast_pass(fast_pass);
    if (strcmp(input, fast_pass) == 0) {
        print_ride_ticket(input);
        return 0;
    }

    puts("Invalid code. Please return to the regular line.");
    return 1;
}
