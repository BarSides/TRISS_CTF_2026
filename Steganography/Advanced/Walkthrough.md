# Scatter Shot: walkthrough

`scatter.py` hides a message in the least significant bit of 16-bit mono samples. Which samples it uses comes from an xorshift32 PRNG seeded from a 4-digit PIN, so the bits are scattered through the file instead of sitting in the first few samples. The payload is a 2-byte big-endian length followed by the message, written most significant bit first.

The weakness is the key space: a 4-digit PIN is only 10,000 possibilities, and we know the plaintext starts with `BarSides{`.

1. Read the script and note the details a decoder must match: `seed_from_pin`, the xorshift step, `% n_samples` with duplicates skipped, low byte at `frames[2*i]`, MSB-first bits, 2-byte length prefix.
2. Write `unhide(frames, pin, nbytes)` that walks `positions(pin, n)` and collects LSBs. Copying `XorShift32`, `seed_from_pin` and `positions` straight out of `scatter.py` is fine.
3. Loop `pin` over 0 to 9999. For each, decode 11 bytes (length plus `BarSides{`) and keep the PIN whose bytes 2 to 10 match. Remember PIN 0412 is the integer 412.
4. Re-decode with that PIN using the real length to get the whole message.

`build/solve.py` does exactly this and finds PIN `0412` (Pittsburgh's area code) almost instantly:

```
$ python3 build/solve.py files/voicemail.wav
PIN 0412: BarSides{four_digits_is_not_a_key}
```

Things that trip people up: reading high bytes instead of low bytes, LSB-first bit order, forgetting the length prefix (then the prefix check is off by two bytes), or reseeding the PRNG per bit.

Flag: `BarSides{four_digits_is_not_a_key}`
