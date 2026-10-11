/*
 * Acrisure Stadium -- Will Call window
 * TRISS CTF 2026 : Pwn / Beginner
 *
 * Reads the name on the reservation into a 32-byte buffer, then checks a
 * "vip" flag that sits right after that buffer in memory. Overflow the buffer
 * and the extra bytes spill onto the vip flag.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void print_flag(void) {
    char flag[128];
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("(No flag.txt here -- run the same input against the live "
             "server to get the real flag.)");
        return;
    }
    if (fgets(flag, sizeof flag, f))
        fputs(flag, stdout);
    fclose(f);
}

int main(void) {
    struct {
        char name[32];
        int  vip;
    } gate;

    setup();
    gate.vip = 0;

    puts("====================================");
    puts("   Acrisure Stadium -- Will Call");
    puts("====================================");
    puts("Pick up your tickets at the window.");
    puts("General admission is open to everyone. VIP field passes are not.");
    printf("\nName on the reservation: ");

    read(0, gate.name, 64);

    if (gate.vip != 0) {
        puts("\nVIP on file. Welcome back! Here are your field passes:");
        print_flag();
    } else {
        printf("\nThanks, that name is general admission. Enjoy the game, yinz!\n");
    }
    return 0;
}
