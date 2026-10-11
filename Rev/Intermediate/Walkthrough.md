# Twirl the Towel walkthrough

1. `./towel_check` asks for an activation key. `strings` shows the banner, `TOWEL`, and the pass and fail messages, but no key.
2. Open the binary in Ghidra and auto-analyze. It is stripped, so open Search > For Strings, find `Activation failed`, and follow the reference into `main`.
3. Just above the message is the check (gcc may inline it into `main`). Cleaned up, it reads:

   ```c
   if (strlen(input) != 0x2c) fail;           // 44 characters
   for (i = 0; i < 0x2c; i++) {
       c = ROL(input[i], 3);                    // shows as (c << 3) | (c >> 5)
       c ^= "TOWEL"[i % 5];
       c += i * 7;
       bad |= c ^ table[i];
   }
   ```

4. Copy the 44 table bytes from the data section (select them in the Listing, right click > Copy Special > Byte String).
5. Run the loop backwards: subtract `7 * i`, XOR with the key byte, rotate right 3.

   ```python
   table = bytes.fromhex("464bd2f4239a8efdd62e35511881c9e02593643bd3d7e6bf9f0e9231a281311554a6f5ecb1ef48f027839adb")
   key = b"TOWEL"
   out = bytes(((((t - 7*i) & 0xff) ^ key[i % 5]) >> 3 | (((t - 7*i) & 0xff) ^ key[i % 5]) << 5) & 0xff
               for i, t in enumerate(table))
   print(out.decode())
   ```

6. Check it: `echo 'BarSides{twirled_it_backwards_and_it_worked}' | ./towel_check` prints "Activated!".

Flag: `BarSides{twirled_it_backwards_and_it_worked}`
