#!/usr/bin/env python3
"""Generate files/postcard.jpg for the Nesting Dolls challenge.

Organizer only: do not attach this script in CTFd. It is kept so the file can
be rebuilt (for example with a new flag). Requires Pillow and the `zip` CLI
(Python's zipfile cannot write password-protected archives).

Layers, outside in:
  1. A "Greetings from Pittsburgh" postcard, a normal viewable JPEG.
  2. Its EXIF ImageDescription carries the ZIP password.
  3. A ZipCrypto-encrypted ZIP appended after the JPEG's end-of-image marker.
     Viewers stop reading at that marker, so the image still opens normally.
     `zip -A` fixes the offsets so the whole file also opens as a ZIP.
  4. Inside the ZIP, the back of the postcard, which holds the flag.
"""
import os
import random
import subprocess
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FLAG = "BarSides{postcards_have_two_sides}"
PASSWORD = "incline1877"
OUT = Path(__file__).resolve().parent.parent / "files" / "postcard.jpg"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
W, H = 1200, 780

BACK = f"""\
            P O S T   C A R D
-------------------------------------------
 Dear Yinz,

 Rode the Duquesne Incline up Mount
 Washington today. Best view of the Point
 there is: three rivers, a dozen bridges,
 and a skyline that used to be all smoke.

 You found the back of the card, so you
 earned this:

     {FLAG}

 Wish you were here,
 The Bridge Keeper
-------------------------------------------
"""


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def draw_front(rng):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    # dusk sky gradient
    for y in range(H):
        t = y / H
        d.line((0, y, W, y), fill=(int(250 - 90 * t), int(170 - 60 * t), int(110 + 60 * t)))
    d.ellipse((1030, 80, 1130, 180), fill=(255, 226, 150))
    # Mount Washington on the left with the incline track
    d.polygon([(0, 330), (260, 360), (420, 520), (420, H), (0, H)], fill=(58, 74, 52))
    d.line((90, 345, 400, 560), fill=(40, 40, 40), width=8)
    d.rectangle((210, 412, 262, 448), fill=(170, 40, 36))
    # skyline across the river
    x = 460
    while x < W:
        bw, bh = rng.randint(40, 90), rng.randint(120, 330)
        shade = rng.randint(40, 75)
        d.rectangle((x, 560 - bh, x + bw, 560), fill=(shade, shade, shade + 20))
        for wy in range(560 - bh + 12, 550, 22):
            for wx in range(x + 8, x + bw - 8, 16):
                if rng.random() < 0.45:
                    d.rectangle((wx, wy, wx + 6, wy + 10), fill=(255, 214, 120))
        x += bw + rng.randint(4, 14)
    # rivers
    d.rectangle((420, 560, W, H), fill=(52, 92, 132))
    for i in range(60):
        y = rng.randint(575, H - 10)
        x0 = rng.randint(430, W - 60)
        d.line((x0, y, x0 + rng.randint(20, 60), y), fill=(120, 160, 200), width=2)
    # a yellow bridge
    d.rectangle((520, 600, W, 612), fill=(240, 190, 30))
    for i in range(9):
        cx = 560 + i * 80
        d.arc((cx - 40, 560, cx + 40, 640), 180, 360, fill=(240, 190, 30), width=5)
    # postcard border and lettering
    d.rectangle((0, 0, W - 1, H - 1), outline=(250, 244, 230), width=24)
    d.text((60, 50), "Greetings from", font=font("DejaVuSerif.ttf", 54), fill=(255, 250, 240))
    big = font("DejaVuSerif-Bold.ttf", 120)
    d.text((54, 112), "PITTSBURGH", font=big, fill=(30, 30, 30))
    d.text((48, 106), "PITTSBURGH", font=big, fill=(255, 196, 0))
    d.text((60, H - 80), "View of the Point from the Duquesne Incline",
           font=font("DejaVuSans.ttf", 26), fill=(240, 240, 240))
    return img


def main():
    rng = random.Random(1022)
    img = draw_front(rng)
    exif = Image.Exif()
    exif[0x010F] = "Kodak"                       # Make
    exif[0x0110] = "Instamatic 1922"             # Model
    exif[0x013B] = "The Bridge Keeper"           # Artist
    exif[0x010E] = f"Back of the card is locked. Password: {PASSWORD}"  # ImageDescription
    exif[0x8298] = "Wish you were here"          # Copyright

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        jpg = tmp / "front.jpg"
        img.save(jpg, quality=88, exif=exif.tobytes())
        back = tmp / "postcard_back.txt"
        back.write_text(BACK)
        stamp = time.mktime((2026, 10, 22, 9, 0, 0, 0, 0, -1))  # event day
        os.utime(back, (stamp, stamp))
        subprocess.run(["zip", "-q", "-X", "-P", PASSWORD, "back.zip", "postcard_back.txt"],
                       cwd=tmp, check=True)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(jpg.read_bytes() + (tmp / "back.zip").read_bytes())
    # Shift the ZIP's internal offsets to account for the JPEG in front, so
    # the whole file is also a valid ZIP (rename to .zip, or CyberChef Unzip).
    subprocess.run(["zip", "-q", "-A", str(OUT)], check=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
