# The Bridge Keeper's Last Note: walkthrough

The note is a **Hill cipher** with a 2x2 key, mod 26 (A=0 ... Z=25). Only the letters are encrypted. They are read in order, ignoring spaces and punctuation, and taken two at a time. Each pair `(x, y)` becomes `K · (x, y)`. Case and non-letters stay where they were, so the flag line `DcbUhfou{...}` still lines up with `BarSides{...}`, and the flag starts on a pair boundary.

Key: `K = [[3, 3], [2, 5]]`, so `u = 3x + 3y`, `v = 2x + 5y` (mod 26).

## Known plaintext

The crib `BarSides` gives four pairs:

| plain | cipher |
|---|---|
| b a = (1, 0) | d c = (3, 2) |
| r s = (17, 18) | b u = (1, 20) |
| i d = (8, 3) | h f = (7, 5) |
| e s = (4, 18) | o u = (14, 20) |

Pick two plaintext pairs whose 2x2 matrix is invertible mod 26 (its determinant must be odd and not divisible by 13). `ba` and `id` work: `P = [[1, 8], [0, 3]]`, det 3. Then `K = C · P⁻¹ mod 26`, which gives `[[3, 3], [2, 5]]`. Invert K mod 26 and apply it to every letter pair to decrypt.

The pair `ba` alone gives the first column of K straight away: `K · (1, 0)` is just `(K[0][0], K[1][0]) = (3, 2)`.

## Brute force

There are only 26⁴ = 456,976 matrices, so trying them all against the crib takes a few seconds in Python.

```python
import itertools, sys

c = open(sys.argv[1] if len(sys.argv) > 1 else "bridge_keeper_3.txt").read()

def apply(M, text):
    idx = [i for i, ch in enumerate(text) if ch.isalpha()]
    out = list(text)
    for j in range(0, len(idx), 2):
        i1, i2 = idx[j], idx[j + 1]
        x, y = ord(text[i1].lower()) - 97, ord(text[i2].lower()) - 97
        u = (M[0][0] * x + M[0][1] * y) % 26
        v = (M[1][0] * x + M[1][1] * y) % 26
        out[i1] = chr(u + 97).upper() if text[i1].isupper() else chr(u + 97)
        out[i2] = chr(v + 97).upper() if text[i2].isupper() else chr(v + 97)
    return "".join(out)

def inverse(M):
    a, b, c_, d = M[0][0], M[0][1], M[1][0], M[1][1]
    di = pow((a * d - b * c_) % 26, -1, 26)  # raises ValueError if not invertible
    return [[d * di % 26, -b * di % 26], [-c_ * di % 26, a * di % 26]]

for a, b, cc, d in itertools.product(range(26), repeat=4):
    try:
        D = inverse([[a, b], [cc, d]])
    except ValueError:
        continue
    p = apply(D, c)
    if "BarSides{" in p:
        print("key", [[a, b], [cc, d]])
        print(p)
        break
```

Flag: `BarSides{two_by_two_matrix_mod_twenty_six}`
