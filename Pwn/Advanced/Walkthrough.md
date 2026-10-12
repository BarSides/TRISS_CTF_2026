# Walkthrough: Jumbotron

The lesson is the **format-string write**: when user input is passed as the
format string to `printf`, `%n` lets you write to memory, not just read it.

1. Look at the binary. The loop prints your message with `printf(line)` (no
   format string of its own), so `%p`/`%x` leak the stack and `%n` writes to
   it. `flag` prints the flag only when the global `override == 1337`; nothing
   ever sets `override`.

2. Find where your own input sits in the varargs. Send a marker plus some
   `%p`s and count:

   ```
   msg> AAAAAAAA.%p.%p.%p.%p.%p.%p.%p
   jumbotron: AAAAAAAA.0x....-.(nil)...0x4141414141414141...
   ```

   The `0x4141414141414141` shows up at argument **offset 6**.

3. Find the address of `override` (fixed, since the binary is not PIE):

   ```
   nm scoreboard | grep override      # 000000000040408c B override
   ```

4. Write `1337` to that address with a format-string write, then ask for the
   flag. Easiest with pwntools:

   ```python
   from pwn import *
   e = ELF('./scoreboard')
   io = remote('EVENT_HOST', 8014)
   io.recvuntil(b'msg> ')
   io.sendline(fmtstr_payload(6, {e.sym['override']: 1337}))
   io.recvuntil(b'msg> ')
   io.sendline(b'flag')
   io.interactive()
   ```

   The console answers:

   ```
   Override accepted. Lighting up the jumbotron:
   BarSides{the_jumbotron_reads_your_mind}
   ```

Notes:

- By hand the write is `%<N>c%<k>$n`-style: print exactly 1337 characters, then
  `%n` stores the running count at the address you placed on the stack. The
  format string itself starts at argument offset 6, but on 64-bit the target
  address has null bytes, so it goes at the *end* of the payload and is reached
  with the positional specifier for wherever it actually lands (a slot or two
  past 6, once the leading directives and padding are counted; `%8$n` in a
  typical build). pwntools' `fmtstr_payload(6, ...)` computes that index and
  handles the padding, chunking and placement for you, which is why it is the
  tool of choice here.
- No PIE means `override` has a fixed address, so no leak of the binary base
  is needed; no canary is involved because nothing is overflowed.
- This is the final step of the Pwn series: Beginner overwrote an adjacent
  variable by overflowing a buffer, Intermediate overwrote the return address
  (ret2win), and this one writes to arbitrary memory through a format string.
