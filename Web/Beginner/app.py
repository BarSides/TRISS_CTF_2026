#!/usr/bin/env python3
"""Pierogi Race fan site (TRISS CTF 2026, Web Beginner: Staff Only).

robots.txt points at a hidden /backstage/ page. The page trusts a plain
staff=false cookie, so flipping it to true shows the flag. Standard library only.
"""
import html
import os
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

FLAG = os.environ.get("FLAG", "BarSides{robots_txt_is_a_map_not_a_lock}")
STATIC = Path(__file__).with_name("static")

ROBOTS = """# Robots, please stay out of the staff area.
User-agent: *
Disallow: /backstage/
"""

RACERS = [
    ("Cheese Chester", "Defending champ. Never skips leg day."),
    ("Sauerkraut Saul", "Slow off the line, strong finish."),
    ("Jalape&ntilde;o Hannah", "Spicy. Has been known to trip rivals."),
    ("Oliver Onion", "Brings tears to the competition."),
    ("Bacon Burt", "Crowd favorite in the bleachers."),
    ("Potato Pete", "Classic. Reliable. Mashed it in '24."),
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
<header><a href="/" class="brand">The Great Pierogi Race</a><nav><a href="/">Home</a><a href="/racers">Racers</a><a href="/tickets">Tickets</a></nav></header>
<main>
{body}
</main>
<footer>Fan site, not affiliated with any ball club. Staff: the backstage pass page is not linked from here for a reason. Not even search engine robots are allowed in.</footer>
</body>
</html>
""".encode()


HOME = page("The Great Pierogi Race", """
<section class="hero">
  <h1>Six pierogies. One finish line.</h1>
  <p>Every home game in the middle of the 5th inning, six giant pierogies sprint around the warning track. Who will you cheer for?</p>
  <a class="button" href="/racers">Meet the racers</a>
</section>
""")

RACERS_PAGE = page("Racers | The Great Pierogi Race", "<h1>Meet the racers</h1><ul class=\"racers\">" + "".join(
    f"<li><strong>{name}</strong><span>{blurb}</span></li>" for name, blurb in RACERS) + "</ul>")

TICKETS_PAGE = page("Tickets | The Great Pierogi Race", """
<h1>Tickets</h1>
<p>The race is free with any ballpark ticket. Grab a seat along the first base line for the best view of the finish.</p>
""")


def backstage(is_staff: bool) -> bytes:
    if is_staff:
        return page("Backstage | The Great Pierogi Race", f"""
<h1>Backstage</h1>
<p class="ok">Welcome back, staff member! Costumes are on the rack and the race order is on the whiteboard.</p>
<p>Today's backstage pass code:</p>
<p class="flag">{html.escape(FLAG)}</p>
""")
    return page("Backstage | The Great Pierogi Race", """
<h1>Backstage</h1>
<p class="denied">STAFF ONLY. Our records say you are not staff.</p>
<p>If you are a racer, check with your supervisor. Fans, please head back to your seats.</p>
""")


class Handler(BaseHTTPRequestHandler):
    server_version = "PierogiRace/1.0"
    sys_version = ""

    def send(self, status: int, body: bytes, ctype: str = "text/html; charset=utf-8", cookie: str | None = None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/":
            return self.send(200, HOME)
        if path == "/racers":
            return self.send(200, RACERS_PAGE)
        if path == "/tickets":
            return self.send(200, TICKETS_PAGE)
        if path == "/robots.txt":
            return self.send(200, ROBOTS.encode(), "text/plain; charset=utf-8")
        if path == "/static/style.css":
            return self.send(200, (STATIC / "style.css").read_bytes(), "text/css; charset=utf-8")
        if path in ("/backstage", "/backstage/"):
            cookies = SimpleCookie()
            try:
                cookies.load(self.headers.get("Cookie", ""))
            except Exception:
                pass
            if "staff" not in cookies:
                return self.send(200, backstage(False), cookie="staff=false; Path=/")
            return self.send(200, backstage(cookies["staff"].value.strip().lower() == "true"))
        return self.send(404, page("Not found", "<h1>404</h1><p>That page ran off the warning track.</p>"))

    do_HEAD = do_GET

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
