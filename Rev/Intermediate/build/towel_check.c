/*
 * Twirl the Towel: TRISS CTF 2026, Rev Intermediate.
 * Organizer source. Do not attach; players get only the stripped binary.
 *
 * The activation key is the flag. Each byte is rotated left 3, XORed with
 * "TOWEL", and has 7*i added, then compared with expected[]. There is no
 * strcmp to ltrace and nothing to pull from memory: players have to read
 * the loop and run it backwards. expected[] comes from gen.py.
 */
#include <stdio.h>
#include <string.h>

static const unsigned char expected[] = {
    0x46, 0x4b, 0xd2, 0xf4, 0x23, 0x9a, 0x8e, 0xfd, 0xd6, 0x2e, 0x35, 0x51,
    0x18, 0x81, 0xc9, 0xe0, 0x25, 0x93, 0x64, 0x3b, 0xd3, 0xd7, 0xe6, 0xbf,
    0x9f, 0x0e, 0x92, 0x31, 0xa2, 0x81, 0x31, 0x15, 0x54, 0xa6, 0xf5, 0xec,
    0xb1, 0xef, 0x48, 0xf0, 0x27, 0x83, 0x9a, 0xdb,
};

static const char key[] = "TOWEL";

static unsigned char twirl(unsigned char c, size_t i)
{
    c = (unsigned char)((c << 3) | (c >> 5));
    c ^= (unsigned char)key[i % 5];
    c = (unsigned char)(c + 7 * i);
    return c;
}

static int check(const char *s)
{
    size_t i, n = strlen(s);
    int bad = 0;
    if (n != sizeof(expected))
        return 0;
    for (i = 0; i < n; i++)
        bad |= twirl((unsigned char)s[i], i) ^ expected[i];
    return bad == 0;
}

int main(void)
{
    char input[128];

    puts("+--------------------------------------------+");
    puts("|   TWIRL-O-MATIC SMART TOWEL  (Black+Gold)  |");
    puts("|  Activation required before first twirl    |");
    puts("+--------------------------------------------+");
    printf("Activation key: ");
    fflush(stdout);

    if (!fgets(input, sizeof(input), stdin))
        return 1;
    input[strcspn(input, "\r\n")] = '\0';

    if (check(input)) {
        puts("Activated! Here we go, here we go. Your key is your flag.");
        return 0;
    }
    puts("Activation failed. This towel stays folded.");
    return 1;
}
