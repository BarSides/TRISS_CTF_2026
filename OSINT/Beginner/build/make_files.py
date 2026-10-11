#!/usr/bin/env python3
"""Build the player files for OSINT Beginner: Where Was This?

files/pregame.jpg         a bar photo whose EXIF GPS points at Stinky's (4901 Hatfield St)
files/lawrenceville_map.png  a simplified offline map with a lat/lon grid and house numbers

The map is drawn here, not taken from a map service: only Stinky's position is
anchored to real coordinates, and the streets around it are a simplified sketch
of the Lawrenceville grid. Needs Pillow and DejaVu fonts.
"""
import math
import random
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, TiffImagePlugin

FILES = Path(__file__).resolve().parent.parent / "files"
FONTS = Path("/usr/share/fonts/truetype/dejavu")

# Stinky's Bar & Grill, 4901 Hatfield St, Pittsburgh, PA 15201.
STINKYS = (40.477684, -79.957717)

# Map bounds and size: about 0.32 m per pixel both ways.
LAT_MIN, LAT_MAX = 40.4757, 40.4793
LON_MIN, LON_MAX = -79.9604, -79.9550
W, H = 1600, 1350
GRID = 0.0005
MINOR = 0.0001

M_PER_DEG_LAT = 111_000
M_PER_DEG_LON = 111_000 * math.cos(math.radians(STINKYS[0]))

# Lawrenceville's grid: Butler and Hatfield run northeast, numbered streets cross them.
ALONG = (math.sin(math.radians(50)), math.cos(math.radians(50)))   # northeast, east/north metres
PERP = (-ALONG[1], ALONG[0])                                        # northwest, toward the river
BLOCK = 85          # metres between numbered streets
STREET_GAP = 75     # Hatfield to Butler
HALF_STREET = 5
LOT_W, LOT_D, LOT_START, LOTS = 11, 22, 6.5, 7


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def local(along, perp):
    """Metres along/perpendicular from the 49th St & Hatfield St corner -> (lat, lon)."""
    # Stinky's lot centre sits 12 m up Hatfield from 49th and 16 m in from the kerb.
    a = along - (LOT_START + LOT_W / 2)
    p = perp - (HALF_STREET + LOT_D / 2)
    x = a * ALONG[0] + p * PERP[0]
    y = a * ALONG[1] + p * PERP[1]
    return STINKYS[0] + y / M_PER_DEG_LAT, STINKYS[1] + x / M_PER_DEG_LON


def px(lat, lon):
    return ((lon - LON_MIN) / (LON_MAX - LON_MIN) * W, (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * H)


def pt(along, perp):
    return px(*local(along, perp))


def quad(a0, a1, p0, p1):
    return [pt(a0, p0), pt(a1, p0), pt(a1, p1), pt(a0, p1)]


def rotated_text(img, xy, text, fnt, angle, fill):
    l, t, r, b = fnt.getbbox(text)
    tile = Image.new("RGBA", (r - l + 6, b - t + 6), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((3 - l, 3 - t), text, font=fnt, fill=fill)
    tile = tile.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.paste(tile, (int(xy[0] - tile.width / 2), int(xy[1] - tile.height / 2)), tile)


def make_map():
    img = Image.new("RGB", (W, H), (244, 241, 232))
    d = ImageDraw.Draw(img)
    street_angle = math.degrees(math.atan2(ALONG[1], ALONG[0]))   # on screen, counter-clockwise
    lot_angle = street_angle - 90
    lot_font = font("DejaVuSans.ttf", 15)

    streets = {"Hatfield St": 0, "Butler St": -STREET_GAP}
    cross = range(46, 53)
    far = 400

    # Lots: odd numbers on the river (northwest) side, even on the hill side.
    for perp0 in streets.values():
        for k in cross:
            for side in (1, -1):
                for i in range(LOTS):
                    a0 = (k - 49) * BLOCK + LOT_START + i * LOT_W
                    p_near = perp0 + side * HALF_STREET
                    p_far = perp0 + side * (HALF_STREET + LOT_D)
                    poly = quad(a0 + 0.6, a0 + LOT_W - 0.6, p_near, p_far)
                    d.polygon(poly, fill=(226, 220, 205), outline=(170, 160, 140))
                    num = k * 100 + 4 * i + (1 if side == 1 else 0)
                    c = pt(a0 + LOT_W / 2, perp0 + side * (HALF_STREET + LOT_D / 2))
                    if -40 < c[0] < W + 40 and -40 < c[1] < H + 40:
                        rotated_text(img, c, str(num), lot_font, lot_angle, (70, 64, 55))

    # Streets drawn over the lot edges.
    for perp0 in streets.values():
        d.polygon(quad(-far, far, perp0 - HALF_STREET, perp0 + HALF_STREET), fill=(255, 255, 255))
    for k in cross:
        a = (k - 49) * BLOCK
        d.polygon(quad(a - HALF_STREET, a + HALF_STREET, -far, far), fill=(255, 255, 255))
    for name, perp0 in streets.items():
        for a in (-150, 120):
            rotated_text(img, pt(a + 42.5, perp0), name.upper(), font("DejaVuSans-Bold.ttf", 15), street_angle, (90, 90, 90))
    for k in cross:
        for p in (-STREET_GAP / 2, 40):
            rotated_text(img, pt((k - 49) * BLOCK, p), f"{k}TH ST", font("DejaVuSans-Bold.ttf", 14), lot_angle, (90, 90, 90))

    # Toward the river.
    river = pt(-60, 95)
    rotated_text(img, river, "TOWARD THE ALLEGHENY RIVER  →", font("DejaVuSans-Bold.ttf", 16), lot_angle + 180, (60, 110, 160))

    # Faint minor grid every 0.0001 degrees, then the labelled major grid.
    for i in range(round((LAT_MAX - LAT_MIN) / MINOR) + 1):
        y = px(LAT_MIN + i * MINOR, LON_MIN)[1]
        d.line([(0, y), (W, y)], fill=(236, 190, 190), width=1)
    for i in range(round((LON_MAX - LON_MIN) / MINOR) + 1):
        x = px(LAT_MIN, LON_MIN + i * MINOR)[0]
        d.line([(x, 0), (x, H)], fill=(236, 190, 190), width=1)
    gfont = font("DejaVuSansMono.ttf", 15)
    lat = math.ceil(LAT_MIN / GRID) * GRID
    while lat < LAT_MAX:
        y = px(lat, LON_MIN)[1]
        d.line([(0, y), (W, y)], fill=(200, 60, 60), width=1)
        for x, anchor in ((6, "lb"), (W - 6, "rb")):
            d.text((x, y - 2), f"{lat:.4f}", font=gfont, fill=(180, 40, 40), anchor=anchor)
        lat += GRID
    lon = math.ceil(LON_MIN / GRID) * GRID
    while lon < LON_MAX:
        x = px(LAT_MIN, lon)[0]
        d.line([(x, 0), (x, H)], fill=(200, 60, 60), width=1)
        for y, anchor in ((6, "lt"), (H - 6, "lb")):
            d.text((x + 4, y), f"{lon:.4f}", font=gfont, fill=(180, 40, 40), anchor=anchor)
        lon += GRID

    # Legend box.
    d.rectangle([W - 470, H - 190, W - 20, H - 40], fill=(255, 255, 255), outline=(60, 60, 60), width=2)
    d.text((W - 455, H - 180), "Lawrenceville, Pittsburgh", font=font("DejaVuSans-Bold.ttf", 22), fill=(30, 30, 30))
    d.text((W - 455, H - 148), "Red lines: lat / lon every 0.0005, faint every 0.0001", font=font("DejaVuSans.ttf", 14), fill=(30, 30, 30))
    d.text((W - 455, H - 128), "Lots show house numbers. Simplified sketch,", font=font("DejaVuSans.ttf", 14), fill=(30, 30, 30))
    d.text((W - 455, H - 110), "not survey accurate. North is up.", font=font("DejaVuSans.ttf", 14), fill=(30, 30, 30))
    bar = 50 / ((LON_MAX - LON_MIN) * M_PER_DEG_LON) * W
    d.rectangle([W - 455, H - 75, W - 455 + bar, H - 67], fill=(30, 30, 30))
    d.text((W - 455 + bar + 8, H - 80), "50 m", font=font("DejaVuSans.ttf", 14), fill=(30, 30, 30))
    d.polygon([(W - 60, H - 150), (W - 72, H - 120), (W - 48, H - 120)], fill=(30, 30, 30))
    d.text((W - 60, H - 112), "N", font=font("DejaVuSans-Bold.ttf", 16), fill=(30, 30, 30), anchor="mt")
    img.save(FILES / "lawrenceville_map.png", optimize=True)


def to_dms(value):
    value = abs(value)
    deg = int(value)
    minutes = int((value - deg) * 60)
    seconds = round((value - deg - minutes / 60) * 3600, 2)
    return tuple(TiffImagePlugin.IFDRational(Fraction(v).limit_denominator(100)) for v in (deg, minutes, seconds))


def make_photo():
    rng = random.Random(4901)
    w, h = 1200, 900
    img = Image.new("RGB", (w, h), (28, 22, 20))
    d = ImageDraw.Draw(img)

    # Window and neon behind the bar.
    d.rectangle([80, 60, 1120, 470], fill=(16, 22, 38))
    for x in (420, 780):
        d.rectangle([x, 60, x + 18, 470], fill=(40, 30, 26))
    glow = Image.new("RGB", (w, h), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.text((180, 130), "OPEN", font=font("DejaVuSans-Bold.ttf", 110), fill=(255, 40, 90))
    g.text((820, 160), "WINGS", font=font("DejaVuSans-Bold.ttf", 70), fill=(60, 200, 255))
    img.paste(Image.blend(img, glow.filter(ImageFilter.GaussianBlur(14)), 0.6), (0, 0))
    img.paste(glow, (0, 0), glow.convert("L").point(lambda v: 255 if v > 40 else 0))
    d = ImageDraw.Draw(img)

    # Bar top.
    d.rectangle([0, 470, w, h], fill=(96, 60, 34))
    for y in range(470, h, 4):
        s = rng.randint(-12, 12)
        d.line([(0, y), (w, y + rng.randint(-3, 3))], fill=(96 + s, 60 + s // 2, 34 + s // 3), width=4)

    # Coaster with a BarSides doodle.
    d.ellipse([560, 690, 900, 860], fill=(236, 230, 214), outline=(180, 170, 150), width=3)
    d.text((730, 775), "BarSides", font=font("DejaVuSerif-Bold.ttf", 44), fill=(39, 37, 31), anchor="mm")
    d.text((730, 822), "pre-game crew", font=font("DejaVuSans.ttf", 20), fill=(90, 80, 70), anchor="mm")

    # Pint glass.
    d.polygon([(300, 330), (500, 330), (480, 800), (320, 800)], fill=(214, 140, 36))
    d.polygon([(300, 330), (500, 330), (496, 400), (304, 400)], fill=(250, 244, 226))
    d.line([(330, 420), (345, 780)], fill=(245, 196, 110), width=10)
    d.ellipse([318, 785, 482, 815], fill=(190, 120, 30))

    # Basket of wings.
    d.rounded_rectangle([880, 520, 1150, 660], radius=20, fill=(176, 30, 45))
    for i in range(7):
        x, y = 905 + i * 34 + rng.randint(-6, 6), 545 + rng.randint(-8, 30)
        d.ellipse([x, y, x + 46, y + 30], fill=(180, 70, 20), outline=(120, 40, 10))

    img = img.filter(ImageFilter.GaussianBlur(0.8))

    exif = Image.Exif()
    exif[0x010F] = "Google"
    exif[0x0110] = "Pixel 8"
    exif[0x0131] = "HDR+ 1.0.641377693zd"
    exif[0x0132] = "2026:10:15 19:12:44"
    exif.get_ifd(0x8769)[0x9003] = "2026:10:15 19:12:44"
    gps = exif.get_ifd(0x8825)
    gps[0x0000] = b"\x02\x02\x00\x00"
    gps[0x0001] = "N"
    gps[0x0002] = to_dms(STINKYS[0])
    gps[0x0003] = "W"
    gps[0x0004] = to_dms(STINKYS[1])
    img.save(FILES / "pregame.jpg", quality=90, exif=exif)


if __name__ == "__main__":
    FILES.mkdir(exist_ok=True)
    make_map()
    make_photo()
    print(f"wrote {FILES / 'lawrenceville_map.png'} and {FILES / 'pregame.jpg'}")
