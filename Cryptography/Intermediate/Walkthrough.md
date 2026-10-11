# Bridge Keeper's Revenge: walkthrough

The note is an affine cipher, `E(x) = (5x + 8) mod 26`, with A=0 ... Z=25. Case, punctuation and braces are kept, so the flag line `NipUwxcu{qelzwfly_zrcv_urwhz}` lines up with `BarSides{...}`.

1. Known plaintext: `a` (0) encrypts to `i` (8), so `5*0 + b = 8` gives **b = 8**.
2. `B` (1) encrypts to `N` (13), so `a*1 + 8 = 13` gives **a = 5**.
3. Check with another pair: `r` (17) gives `5*17 + 8 = 93 = 15 mod 26`, which is `p`. It matches.
4. In CyberChef, use **Affine Cipher Decode** with a = 5, b = 8.

Without the algebra: there are only 12 valid values of a (those coprime with 26) and 26 of b, so a short script trying all 312 keys for the crib `BarSides` also works.

```python
c = open("bridge_keeper_2.txt").read()
for a in [1,3,5,7,9,11,15,17,19,21,23,25]:
    inv = pow(a, -1, 26)
    for b in range(26):
        p = "".join(chr(inv*(ord(ch)-o-b) % 26 + o) if ch.isalpha() else ch
                    for ch in c for o in [65 if ch.isupper() else 97])
        if "BarSides" in p:
            print(a, b); print(p)
```

Flag: `BarSides{multiply_then_shift}`
