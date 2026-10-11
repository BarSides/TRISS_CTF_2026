/*
 * Acrisure Stadium -- Skybox access terminal
 * TRISS CTF 2026 : Pwn / Intermediate  (ret2win)
 *
 * vuln() reads the pass code into a 64-byte buffer with no bounds check, so you
 * can overwrite the saved return address and redirect execution to open_skybox(),
 * a function that is compiled in but never called on the normal path.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void setup(void) {
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

/* force_align_arg_pointer realigns the stack on entry, so jumping straight here
 * with a return-address overwrite works without needing a separate ret gadget. */
__attribute__((force_align_arg_pointer))
void open_skybox(void) {
    char flag[128];
    FILE *f = fopen("flag.txt", "r");
    puts("\n*** SKYBOX UNLOCKED ***");
    if (!f) {
        puts("(No flag.txt here -- run the same input against the live server.)");
        return;
    }
    if (fgets(flag, sizeof flag, f))
        fputs(flag, stdout);
    fclose(f);
}

void vuln(void) {
    char code[64];
    puts("Skybox access is restricted to suite holders.");
    printf("Enter your access code: ");
    read(0, code, 200);          /* 200 bytes into a 64-byte buffer */
    printf("Checking code \"%s\"... denied.\n", code);
}

int main(void) {
    setup();
    puts("====================================");
    puts("   Acrisure Stadium -- Suite Level");
    puts("====================================");
    vuln();
    puts("Have a nice day down in general admission.");
    return 0;
}
