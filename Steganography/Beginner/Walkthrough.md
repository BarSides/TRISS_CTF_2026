# Ghost Sign: walkthrough

The sign's background is one flat colour, RGB (212, 198, 172). Below the ad, the flag is painted in RGB (213, 199, 173), one step brighter in every channel. The difference is invisible to the eye, but any tool that treats each exact colour separately shows it at once.

**CyberChef (local copy):**

1. Drag `ghost_sign.png` into the input.
2. Add **Randomise Colour Palette**. Each distinct colour gets a random new one, so the two near-identical creams become two very different colours and the flag appears.
3. Alternatively, add **View Bit Plane** with colour Red and bit 0. The background colour is even and the flag colour is odd, so the flag shows white on black.

**Image editor (GIMP, Paint.NET, even MS Paint):** use the paint bucket with tolerance/threshold 0 on the blank part of the sign. The fill stops at the flag's letters. Pushing levels or curves hard on that area works too.

The PNG comment ("Still there if you look hard enough") is just a nudge for players who run `strings` or `exiftool`; the flag is not in the metadata.

Flag: `BarSides{faded_but_not_forgotten}`
