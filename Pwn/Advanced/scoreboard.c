/*
 * Acrisure Stadium -- Scoreboard operator console
 * TRISS CTF 2026 : Pwn / Advanced  (format string)
 *
 * The console echoes whatever message you queue straight through printf()
 * with no format string of its own, so your input IS the format string.
 * A global "override" starts at 0; the jumbotron only shows the secret
 * cheer (the flag) once override holds the operator code 1337. Use the
 * format-string bug to write that value, then ask for the flag.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int override = 0;        /* global -> fixed address (no PIE) */

void setup(void) {
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void show_flag(void) {
    char flag[128];
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("(No flag.txt here -- run your exploit against the live server.)");
        return;
    }
    if (fgets(flag, sizeof flag, f))
        fputs(flag, stdout);
    fclose(f);
}

int main(void) {
    char line[256];
    setup();

    puts("=========================================");
    puts("  Acrisure Stadium -- Scoreboard Console");
    puts("=========================================");
    puts("Type a message to put it on the jumbotron.");
    puts("Type 'flag' to show the secret cheer (operator override required).");

    while (1) {
        printf("\nmsg> ");
        if (!fgets(line, sizeof line, stdin))
            break;
        line[strcspn(line, "\n")] = '\0';

        if (strcmp(line, "flag") == 0) {
            if (override == 1337) {
                puts("Override accepted. Lighting up the jumbotron:");
                show_flag();
            } else {
                printf("Override not set (override = %d). Access denied.\n", override);
            }
            continue;
        }
        if (strcmp(line, "quit") == 0)
            break;

        printf("jumbotron: ");
        printf(line);      /* the vulnerable format string */
        printf("\n");
    }
    return 0;
}
