#!/usr/bin/env python3
"""446 Bridges, a Pittsburgh bridge directory (TRISS CTF 2026, Web Intermediate).

The search box pastes the query straight into SQL, so players can UNION SELECT
from sqlite_master to find a hidden table and dump the flag from it.
The database is rebuilt in memory at start and queried read only, one statement
at a time, with a time limit. Standard library only.
"""
import html
import os
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

FLAG = os.environ.get("FLAG", "BarSides{union_select_the_city_of_bridges}")
STATIC = Path(__file__).with_name("static")
DB_URI = "file:bridges?mode=memory&cache=shared"
MAX_ROWS = 100
TIME_LIMIT = 1.0

BRIDGES = [
    ("Roberto Clemente Bridge", "Allegheny", 1928),
    ("Andy Warhol Bridge", "Allegheny", 1926),
    ("Rachel Carson Bridge", "Allegheny", 1928),
    ("Fort Duquesne Bridge", "Allegheny", 1969),
    ("David McCullough (16th Street) Bridge", "Allegheny", 1923),
    ("31st Street Bridge", "Allegheny", 1928),
    ("40th Street Bridge", "Allegheny", 1924),
    ("Highland Park Bridge", "Allegheny", 1938),
    ("Veterans Bridge", "Allegheny", 1987),
    ("Fort Pitt Bridge", "Monongahela", 1959),
    ("Smithfield Street Bridge", "Monongahela", 1883),
    ("Liberty Bridge", "Monongahela", 1928),
    ("Panhandle Bridge", "Monongahela", 1903),
    ("10th Street Bridge", "Monongahela", 1933),
    ("Birmingham Bridge", "Monongahela", 1976),
    ("Hot Metal Bridge", "Monongahela", 1887),
    ("Glenwood Bridge", "Monongahela", 1966),
    ("Homestead Grays Bridge", "Monongahela", 1937),
    ("West End Bridge", "Ohio", 1932),
    ("McKees Rocks Bridge", "Ohio", 1931),
]

CREW_NOTES = [
    (1, "Repaint the Clemente Bridge Aztec Gold before opening day."),
    (2, "Pigeons are back under the Smithfield Street Bridge. Again."),
    (3, f"Gate code for the Liberty Bridge maintenance catwalk: {FLAG}"),
    (4, "Do NOT let the public search this table."),
]


def build_db() -> sqlite3.Connection:
    keeper = sqlite3.connect(DB_URI, uri=True, check_same_thread=False)
    keeper.executescript("""
        CREATE TABLE bridges (name TEXT, river TEXT, year_opened INTEGER);
        CREATE TABLE maintenance_crew_notes (id INTEGER PRIMARY KEY, note TEXT);
    """)
    keeper.executemany("INSERT INTO bridges VALUES (?, ?, ?)", BRIDGES)
    keeper.executemany("INSERT INTO maintenance_crew_notes VALUES (?, ?)", CREW_NOTES)
    keeper.commit()
    return keeper  # must stay open or the shared in-memory database disappears


def search(q: str):
    """Return (sql, rows, error). Deliberately vulnerable."""
    sql = f"SELECT name, river, year_opened FROM bridges WHERE name LIKE '%{q}%' ORDER BY name"
    conn = sqlite3.connect(DB_URI, uri=True)
    try:
        conn.execute("PRAGMA query_only = ON")
        deadline = time.monotonic() + TIME_LIMIT
        conn.set_progress_handler(lambda: time.monotonic() > deadline, 10000)
        rows = conn.execute(sql).fetchmany(MAX_ROWS)
        return sql, rows, None
    except sqlite3.Error as e:
        return sql, [], str(e)
    finally:
        conn.close()


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
<header><a href="/" class="brand">446 Bridges</a><span>The unofficial directory of the City of Bridges</span></header>
<main>
{body}
</main>
<footer>Pittsburgh has 446 bridges. We have listed a few. Data maintained by the bridge crew.</footer>
</body>
</html>
""".encode()


def render(q: str | None) -> bytes:
    form = f"""
<form action="/search" method="get">
  <label for="q">Search bridges by name</label>
  <div class="row"><input id="q" name="q" value="{html.escape(q or '')}" placeholder="e.g. Clemente" autofocus><button>Search</button></div>
</form>"""
    if q is None:
        return page("446 Bridges", form + "<p>Try searching for a bridge, or leave the box empty to list them all.</p>")
    sql, rows, error = search(q)
    out = [form]
    if error:
        out.append(f'<p class="error">Database error: {html.escape(error)}</p>')
    elif not rows:
        out.append("<p>No bridges found.</p>")
    else:
        out.append(f"<p>{len(rows)} result(s)</p><table><thead><tr><th>Bridge</th><th>River</th><th>Opened</th></tr></thead><tbody>")
        for row in rows:
            out.append("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>")
        out.append("</tbody></table>")
    return page("Search | 446 Bridges", "".join(out))


class Handler(BaseHTTPRequestHandler):
    server_version = "446Bridges/1.0"
    sys_version = ""

    def send(self, status: int, body: bytes, ctype: str = "text/html; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/":
            return self.send(200, render(None))
        if url.path == "/search":
            q = parse_qs(url.query, keep_blank_values=True).get("q", [""])[0][:500]
            return self.send(200, render(q))
        if url.path == "/static/style.css":
            return self.send(200, (STATIC / "style.css").read_bytes(), "text/css; charset=utf-8")
        return self.send(404, page("Not found", "<h1>404</h1><p>That bridge is out.</p>"))

    do_HEAD = do_GET

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    _keeper = build_db()
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
