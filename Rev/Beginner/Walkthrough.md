# Skip the Line walkthrough

1. `chmod +x skip_the_line && ./skip_the_line`. It asks for a fast pass code.
2. `strings skip_the_line` shows `PHANTOM`. Entering it gets "That test pass was switched off after the 2025 season." The real code is not in the strings output.
3. Pick any of these:
   - **ltrace:** `ltrace ./skip_the_line`, type anything, and the second `strcmp` call shows your input next to `"KENNYWOOD1898"`.
   - **gdb:** `gdb ./skip_the_line`, `break decode_fast_pass`, `run`, type anything, `finish`, then `x/s $rdi` prints `KENNYWOOD1898`.
   - **Ghidra:** open the binary, auto-analyze, and read `decode_fast_pass`: each byte of `encoded_code` is XORed with `0x5A`. Copy the 13 bytes (`11 1f 14 14 03 0d 15 15 1e 6b 62 63 62`) into CyberChef, From Hex, XOR with key `5A`, and get `KENNYWOOD1898`.
4. Run the kiosk again and enter `KENNYWOOD1898`.

```
  *** FAST PASS ACCEPTED ***
  Your ride ticket: BarSides{skipped_the_line_at_kennywood}
```

Patching the `jne` after the `strcmp` does not work: the flag is decrypted with the code you typed, so a wrong code prints garbage.

Flag: `BarSides{skipped_the_line_at_kennywood}`
