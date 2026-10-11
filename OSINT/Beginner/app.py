#!/usr/bin/env python3
"""Yinzr, a tiny offline social network (TRISS CTF 2026, OSINT Beginner: Lost Badge).

BarSides posts a photo of a TRISS speaker badge left at Stinky's after a meetup.
The handle on the badge is half covered, so players search for @pierogi_ accounts,
work out which lookalike was actually at Stinky's that night, and find the claim
code (the flag) the owner overshared on their profile. Every person here is
fictional. Standard library only.
"""
import html
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

FLAG = os.environ.get("FLAG", "BarSides{pivot_on_the_handle}")
STATIC = Path(__file__).with_name("static")

# handle: (display name, location, bio, shown in the home feed)
USERS = {
    "barsides_pgh": ("BarSides", "Pittsburgh, PA",
                     "Pittsburgh's security meetup, and the folks behind the TRISS CTF. Usually at Stinky's in Lawrenceville.", True),
    "lawrenceville_eats": ("Lawrenceville Eats", "Lawrenceville, Pittsburgh",
                           "Butler Street, one plate at a time.", True),
    "yinzer_weather": ("Yinzer Weather", "Pittsburgh, PA", "Jagoff-free forecasts.", True),
    "pierogi_packets": ("Rosie K.", "Lawrenceville, Pittsburgh",
                        "Red teamer. Wing critic. Speaking at TRISS 2026.", False),
    "pierogi_payloads": ("Rosie Kaminski", "Columbus, OH",
                         "Pentester. Coffee in, findings out. TRISS 2026 speaker!", False),
    "pierogi_pat": ("Pat the Pierogi Fan", "South Side, Pittsburgh",
                    "Cheese Chester or bust. Every home game since '99.", False),
    "pierogi_pals": ("Pierogi Pals", "Bloomfield, Pittsburgh",
                     "Church-basement pierogies, reviewed. Not a hacker, sorry.", False),
    "pierogi_parade": ("The Pierogi Parade", "Pittsburgh, PA",
                       "Marching band. We play \"Pierogi Polka\" on request.", False),
}

# (handle, timestamp, text, image, pinned)
POSTS = [
    ("barsides_pgh", "2026-10-16 10:05",
     "Great turnout at last night's BarSides meetup at Stinky's in Lawrenceville! Someone left their "
     "TRISS 2026 speaker badge on the bar. We're holding it behind the bar. If it's yours, the bartender "
     "will ask for the claim code printed on the back.", "badge.jpg", False),
    ("barsides_pgh", "2026-10-15 17:30",
     "Meetup tonight at Stinky's Bar & Grill, 7pm. TRISS speakers, come do a dry run of your talk.", None, False),
    ("barsides_pgh", "2026-10-09 12:00",
     "TRISS 2026 is October 22. The CTF is beginner friendly, bring a laptop and a friend.", None, False),
    ("lawrenceville_eats", "2026-10-15 21:40",
     "Wing night on Butler Street was packed. Something about a hacker meetup?", None, False),
    ("yinzer_weather", "2026-10-15 06:00", "Jag-wire weather today: sun, then rain, then sun again.", None, False),

    ("pierogi_packets", "2026-10-16 09:12",
     "Note to self, since I keep losing it: if anyone turns in my TRISS badge, the claim code on the back is "
     f"{FLAG}", None, True),
    ("pierogi_packets", "2026-10-16 08:47",
     "Woke up with no speaker badge. It was definitely on the lanyard at the bar last night. Oops.", None, False),
    ("pierogi_packets", "2026-10-15 19:12",
     "Dry-running my TRISS talk at the BarSides meetup at Stinky's. Wings are on me if you find a typo in my slides.",
     None, False),
    ("pierogi_packets", "2026-10-12 14:03", "Slides for Rust Belt Red Teaming are 80% done. The other 80% is next.",
     None, False),

    ("pierogi_payloads", "2026-10-16 07:55", "Badge? Still in my bag from the hotel. Columbus coffee is not Pittsburgh coffee.",
     None, False),
    ("pierogi_payloads", "2026-10-15 19:30",
     "Stuck in Columbus all week for a client gig, so I'm missing the BarSides meetup tonight. Next time, yinz.",
     None, False),
    ("pierogi_payloads", "2026-10-10 11:20", "Accepted to speak at TRISS 2026! See you on the 22nd.", None, False),

    ("pierogi_pat", "2026-10-15 19:05", "Pierogi race in the 5th. Cheese Chester won AGAIN.", None, False),
    ("pierogi_pals", "2026-10-14 18:00", "Potato and cheese at St. Mary's this Friday. 9/10, needed more onions.",
     None, False),
    ("pierogi_parade", "2026-10-13 16:00", "Practice moved to Thursday. Bring your sousaphone.", None, False),
]


def page(title: str, body: str) -> bytes:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header><a href="/" class="brand">Yinzr</a>
<form action="/search" method="get"><input name="q" placeholder="Search people" aria-label="Search people"><button>Search</button></form>
</header>
<main>
{body}
</main>
<footer>Yinzr is a fictional social network for the TRISS CTF. Everyone on it is made up.</footer>
</body>
</html>
""".encode()


def post_html(post) -> str:
    handle, when, text, image, pinned = post
    name = USERS[handle][0]
    img = f'<img src="/static/{image}" alt="Photo attached to the post">' if image else ""
    pin = '<span class="pin">Pinned</span>' if pinned else ""
    return (f'<article class="post">{pin}<div class="who"><a href="/u/{handle}"><strong>{html.escape(name)}</strong> '
            f'@{handle}</a> <time>{when}</time></div><p>{html.escape(text)}</p>{img}</article>')


def home() -> bytes:
    feed = sorted((p for p in POSTS if USERS[p[0]][3]), key=lambda p: p[1], reverse=True)
    return page("Yinzr", "<h1>Home</h1>" + "".join(post_html(p) for p in feed))


def search(q: str) -> bytes:
    q = q.strip().lstrip("@").lower()
    if not q:
        return page("Search | Yinzr", "<h1>Search people</h1><p>Type part of a handle or name.</p>")
    hits = [h for h, u in USERS.items() if q in h or q in u[0].lower()]
    rows = "".join(f'<li><a href="/u/{h}"><strong>{html.escape(USERS[h][0])}</strong> @{h}</a>'
                   f'<span>{html.escape(USERS[h][1])}</span></li>' for h in hits)
    body = f"<h1>People matching &ldquo;{html.escape(q)}&rdquo;</h1>"
    body += f'<ul class="people">{rows}</ul>' if hits else "<p>No one found.</p>"
    return page("Search | Yinzr", body)


def profile(handle: str):
    user = USERS.get(handle)
    if not user:
        return None
    name, where, bio, _ = user
    # Pinned first, then newest first.
    posts = sorted((p for p in POSTS if p[0] == handle), key=lambda p: (p[4], p[1]), reverse=True)
    body = (f'<section class="profile"><h1>{html.escape(name)}</h1><p class="handle">@{handle} &middot; '
            f'{html.escape(where)}</p><p>{html.escape(bio)}</p></section>' + "".join(post_html(p) for p in posts))
    return page(f"{name} (@{handle}) | Yinzr", body)


class Handler(BaseHTTPRequestHandler):
    server_version = "Yinzr"
    sys_version = ""

    def send(self, code: int, body: bytes, ctype: str = "text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            return self.send(200, home())
        if url.path == "/search":
            return self.send(200, search(parse_qs(url.query).get("q", [""])[0]))
        m = re.fullmatch(r"/u/([a-z0-9_]+)/?", url.path)
        if m and (body := profile(m.group(1))):
            return self.send(200, body)
        m = re.fullmatch(r"/static/([a-z0-9_]+\.(css|jpg))", url.path)
        if m and (STATIC / m.group(1)).is_file():
            ctype = "text/css" if m.group(2) == "css" else "image/jpeg"
            return self.send(200, (STATIC / m.group(1)).read_bytes(), ctype)
        self.send(404, page("Not found | Yinzr", "<h1>Not found</h1><p>No such page on Yinzr.</p>"))

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
