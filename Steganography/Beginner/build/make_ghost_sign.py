#!/usr/bin/env python3
"""Generate files/ghost_sign.png for the Ghost Sign challenge.

Organizer only: do not attach this script in CTFd. It is kept so the image
can be rebuilt (for example with a new flag). Requires Pillow.

A brick wall carries a faded painted advertisement. The sign's background is
one flat colour, and the flag is painted on it in a colour exactly one step
brighter in each channel, which is invisible to the eye but shows up with a
paint bucket, levels/curves, CyberChef's "Randomise Colour Palette", or any
bit plane 0 viewer (the panel colour is even, the flag colour is odd).
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

FLAG = "BarSides{faded_but_not_forgotten}"
OUT = Path(__file__).resolve().parent.parent / "files" / "ghost_sign.png"

W, H = 1400, 900
BRICK_W, BRICK_H, MORTAR = 70, 30, 6
PANEL = (212, 198, 172)            # flat sign background, every channel even
HIDDEN = tuple(c + 1 for c in PANEL)  # the flag colour, one step brighter
PAINT_RED = (168, 92, 80)          # faded red lettering
PAINT_DARK = (96, 84, 76)          # faded dark lettering

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def brick_wall(rng):
    img = Image.new("RGB", (W, H), (150, 145, 138))
    px = img.load()
    for row, y in enumerate(range(0, H, BRICK_H + MORTAR)):
        offset = 0 if row % 2 == 0 else -(BRICK_W + MORTAR) // 2
        for x in range(offset, W, BRICK_W + MORTAR):
            base = (rng.randint(120, 165), rng.randint(52, 72), rng.randint(40, 58))
            for by in range(y, min(y + BRICK_H, H)):
                for bx in range(max(x, 0), min(x + BRICK_W, W)):
                    n = rng.randint(-12, 12)
                    px[bx, by] = tuple(max(0, min(255, c + n)) for c in base)
    # mortar noise
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            if (r, g, b) == (150, 145, 138):
                n = rng.randint(-10, 10)
                px[x, y] = (r + n, g + n, b + n)
    return img


def centred(draw, y, text, fnt, fill, x0, x1):
    width = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - width) / 2, y), text, font=fnt, fill=fill)


def main():
    rng = random.Random(1022)  # event date, so rebuilds are identical
    img = brick_wall(rng)
    draw = ImageDraw.Draw(img)

    # The painted panel. Chips of paint have flaked off along its edges,
    # showing the bricks underneath.
    wall = img.copy()
    x0, y0, x1, y1 = 140, 110, W - 140, H - 110
    draw.rectangle((x0, y0, x1, y1), fill=PANEL)
    for _ in range(260):
        side = rng.randrange(4)
        if side < 2:
            ex = x0 + rng.randint(-4, 26) if side == 0 else x1 - rng.randint(-4, 26)
            ey = rng.randint(y0, y1)
        else:
            ex = rng.randint(x0, x1)
            ey = y0 + rng.randint(-4, 20) if side == 2 else y1 - rng.randint(-4, 20)
        w, h = rng.randint(4, 22), rng.randint(3, 12)
        box = (ex, ey, ex + w, ey + h)
        img.paste(wall.crop(box), box[:2])

    # Visible faded advertisement (fictional brand).
    centred(draw, 150, "DRINK", font("DejaVuSerif-Bold.ttf", 70), PAINT_DARK, x0, x1)
    centred(draw, 230, "SMOKY CITY", font("DejaVuSerif-Bold.ttf", 128), PAINT_RED, x0, x1)
    centred(draw, 400, "SODA POP", font("DejaVuSerif-Bold.ttf", 120), PAINT_RED, x0, x1)
    centred(draw, 560, "ICE COLD  •  5¢  •  SINCE 1922",
            font("DejaVuSans-Bold.ttf", 48), PAINT_DARK, x0, x1)

    # The ghost text: drawn without anti-aliasing so every flag pixel is
    # exactly HIDDEN on top of exactly PANEL.
    ghost = Image.new("1", (W, H), 0)
    gdraw = ImageDraw.Draw(ghost)
    gdraw.fontmode = "1"
    gfont = font("DejaVuSansMono-Bold.ttf", 46)
    centred(gdraw, 660, FLAG, gfont, 1, x0, x1)
    centred(gdraw, 600 + 140, "some signs fade, but they never really leave",
            font("DejaVuSansMono.ttf", 26), 1, x0, x1)
    gpx, px = ghost.load(), img.load()
    for y in range(660, 790):
        for x in range(x0, x1):
            if gpx[x, y]:
                if px[x, y] != PANEL:
                    sys.exit(f"ghost text at {x},{y} is not on the flat panel")
                px[x, y] = HIDDEN

    meta = PngImagePlugin.PngInfo()
    meta.add_text("Title", "Ghost sign, Strip District")
    meta.add_text("Comment", "Painted 1922. Painted over 1968. Still there if you look hard enough.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, pnginfo=meta, optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
