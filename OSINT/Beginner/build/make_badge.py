#!/usr/bin/env python3
"""Draw the lost TRISS badge photo for OSINT Beginner: Lost Badge.

The badge shows the speaker's first name and the start of their Yinzr handle;
a thumb covers the rest, so players have to search for lookalike accounts.
Needs Pillow and DejaVu fonts. Writes ../static/badge.jpg (committed, so the
Docker image does not need Pillow).
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent.parent / "static" / "badge.jpg"
FONTS = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def main():
    rng = random.Random(1022)
    w, h = 900, 680
    img = Image.new("RGB", (w, h), (92, 58, 33))
    d = ImageDraw.Draw(img)

    # Bar-top wood grain.
    for y in range(0, h, 3):
        shade = rng.randint(-14, 14)
        d.line([(0, y), (w, y + rng.randint(-6, 6))], fill=(92 + shade, 58 + shade // 2, 33 + shade // 3), width=3)
    # Beer ring from a pint glass.
    d.ellipse([620, 70, 820, 270], outline=(70, 42, 22), width=9)

    # Lanyard running off the top of the photo.
    d.polygon([(380, 0), (430, 0), (455, 150), (415, 150)], fill=(18, 40, 96))
    d.polygon([(560, 0), (510, 0), (490, 150), (530, 150)], fill=(18, 40, 96))
    for x0 in (395, 535):
        d.text((x0 - 10, 40), "BS", font=font("DejaVuSans-Bold.ttf", 18), fill=(253, 184, 39))

    # Badge card, slightly rotated later.
    card = Image.new("RGBA", (420, 560), (0, 0, 0, 0))
    c = ImageDraw.Draw(card)
    c.rounded_rectangle([0, 0, 419, 559], radius=22, fill=(250, 248, 240))
    c.rounded_rectangle([0, 0, 419, 130], radius=22, fill=(39, 37, 31))
    c.rectangle([0, 100, 419, 130], fill=(39, 37, 31))
    c.ellipse([190, 18, 230, 38], fill=(250, 248, 240))  # punch hole
    c.text((210, 80), "TRISS 2026", font=font("DejaVuSans-Bold.ttf", 40), fill=(253, 184, 39), anchor="mm")
    c.text((210, 160), "Three Rivers Information Security Symposium", font=font("DejaVuSans.ttf", 13), fill=(80, 80, 80), anchor="mm")
    c.rectangle([0, 190, 419, 240], fill=(176, 30, 45))
    c.text((210, 215), "SPEAKER", font=font("DejaVuSans-Bold.ttf", 34), fill="white", anchor="mm")
    c.text((210, 320), "Rosie K.", font=font("DejaVuSans-Bold.ttf", 54), fill=(39, 37, 31), anchor="mm")
    c.text((210, 380), "Talk: Rust Belt Red Teaming", font=font("DejaVuSans.ttf", 20), fill=(60, 60, 60), anchor="mm")
    c.text((40, 455), "Yinzr: @pierogi_pa", font=font("DejaVuSansMono.ttf", 30), fill=(39, 37, 31), anchor="lm")
    c.text((210, 525), "BarSides presents TRISS", font=font("DejaVuSans.ttf", 14), fill=(120, 120, 120), anchor="mm")
    card = card.rotate(-4, resample=Image.BICUBIC, expand=True)

    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 110), mask=card.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.paste(shadow, (258, 130), shadow)
    img.paste(card, (240, 110), card)

    # Someone's thumb holding the badge down, covering the end of the handle.
    thumb = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    t = ImageDraw.Draw(thumb)
    t.ellipse([560, 520, 760, 640], fill=(224, 172, 140, 255))
    t.polygon([(640, 560), (900, 600), (900, 680), (700, 680)], fill=(214, 160, 128, 255))
    t.ellipse([610, 535, 690, 585], fill=(240, 205, 185, 255))  # nail
    thumb = thumb.filter(ImageFilter.GaussianBlur(1.5))
    img.paste(thumb, (0, 0), thumb)

    img = img.filter(ImageFilter.GaussianBlur(0.6))
    OUT.parent.mkdir(exist_ok=True)
    img.save(OUT, quality=88)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
