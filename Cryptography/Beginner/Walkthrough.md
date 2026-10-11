# Steel City Shift: walkthrough

The note is a Caesar cipher with a shift of 7 (decrypt with a shift of 19, or ROT -7). Letter case, punctuation, digits and braces are left alone, so the flag's shape `XxxXxxxx{...}` is still visible on the line `IhyZpklz{aoyll_ypclyz_vul_zopma}`.

1. Open the local CyberChef and paste in `bridge_keeper.txt`.
2. Add **ROT13 Brute Force**, set **Crib** to `BarSides`.
3. The only matching result is amount 19, which shows the plain note and the flag.

By hand: `I` should be `B`, which is 7 letters back, so shift every letter back by 7.

Flag: `BarSides{three_rivers_one_shift}`
