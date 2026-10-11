#!/usr/bin/env python3
"""Build files/dkowalski_firefox_profile.zip for Forensics Intermediate.

Organizers only; do not attach. Standard library only. The URLs live in
browsing.tsv: they are browser history data, never fetched.

The flag only exists XORed with "yinz" and Base64 encoded, typed into the
paste site's form (formhistory.sqlite). The key and the order of operations
are in a CyberChef URL in places.sqlite.
"""
import base64
import hashlib
import io
import random
import sqlite3
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

FLAG = "BarSides{the_recipe_was_in_the_url}"
KEY = b"yinz"
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "files" / "dkowalski_firefox_profile.zip"
PROFILE = "x7k2m9qa.default-release"
START = datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)  # 08:00 EDT
rng = random.Random(1878)


def prtime(minute, jitter=True):
    secs = START.timestamp() + minute * 60 + (rng.randint(0, 50) if jitter else 0)
    return int(secs * 1_000_000) + rng.randint(0, 999_999)


def guid():
    return base64.urlsafe_b64encode(rng.randbytes(9)).decode()


def encoded_flag():
    x = bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(FLAG.encode()))
    return base64.b64encode(x).decode()


def load_visits():
    rows = []
    for line in (HERE / "browsing.tsv").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        minute, vtype, url, title = line.split("\t")
        rows.append((int(minute), int(vtype), url, title))
    return rows


def build_places(path, visits):
    db = sqlite3.connect(path)
    db.executescript("""
    PRAGMA user_version = 77;
    CREATE TABLE moz_origins (id INTEGER PRIMARY KEY, prefix TEXT NOT NULL, host TEXT NOT NULL,
        frecency INTEGER NOT NULL, recalc_frecency INTEGER NOT NULL DEFAULT 0,
        alt_frecency INTEGER, recalc_alt_frecency INTEGER NOT NULL DEFAULT 0, UNIQUE (prefix, host));
    CREATE TABLE moz_places (id INTEGER PRIMARY KEY, url LONGVARCHAR, title LONGVARCHAR,
        rev_host LONGVARCHAR, visit_count INTEGER DEFAULT 0, hidden INTEGER DEFAULT 0 NOT NULL,
        typed INTEGER DEFAULT 0 NOT NULL, frecency INTEGER DEFAULT -1 NOT NULL,
        last_visit_date INTEGER, guid TEXT, foreign_count INTEGER DEFAULT 0 NOT NULL,
        url_hash INTEGER DEFAULT 0 NOT NULL, description TEXT, preview_image_url TEXT,
        site_name TEXT, origin_id INTEGER REFERENCES moz_origins(id),
        recalc_frecency INTEGER NOT NULL DEFAULT 0, alt_frecency INTEGER,
        recalc_alt_frecency INTEGER NOT NULL DEFAULT 0);
    CREATE TABLE moz_historyvisits (id INTEGER PRIMARY KEY, from_visit INTEGER, place_id INTEGER,
        visit_date INTEGER, visit_type INTEGER, session INTEGER, source INTEGER DEFAULT 0 NOT NULL,
        triggeringPlaceId INTEGER);
    CREATE TABLE moz_inputhistory (place_id INTEGER NOT NULL, input LONGVARCHAR NOT NULL,
        use_count INTEGER, PRIMARY KEY (place_id, input));
    CREATE TABLE moz_bookmarks (id INTEGER PRIMARY KEY, type INTEGER, fk INTEGER DEFAULT NULL,
        parent INTEGER, position INTEGER, title LONGVARCHAR, keyword_id INTEGER, folder_type TEXT,
        dateAdded INTEGER, lastModified INTEGER, guid TEXT, syncStatus INTEGER NOT NULL DEFAULT 0,
        syncChangeCounter INTEGER NOT NULL DEFAULT 1);
    CREATE TABLE moz_anno_attributes (id INTEGER PRIMARY KEY, name VARCHAR(32) UNIQUE NOT NULL);
    CREATE TABLE moz_annos (id INTEGER PRIMARY KEY, place_id INTEGER NOT NULL,
        anno_attribute_id INTEGER, content LONGVARCHAR, flags INTEGER DEFAULT 0,
        expiration INTEGER DEFAULT 0, type INTEGER DEFAULT 0, dateAdded INTEGER DEFAULT 0,
        lastModified INTEGER DEFAULT 0);
    CREATE INDEX moz_places_url_hashindex ON moz_places (url_hash);
    CREATE INDEX moz_historyvisits_placedateindex ON moz_historyvisits (place_id, visit_date);
    """)
    origins, places, last_visit = {}, {}, None
    for minute, vtype, url, title in visits:
        u = urlsplit(url)
        okey = (u.scheme + "://", u.hostname)
        if okey not in origins:
            cur = db.execute("INSERT INTO moz_origins (prefix, host, frecency) VALUES (?,?,?)",
                             (okey[0], okey[1], rng.randint(100, 2000)))
            origins[okey] = cur.lastrowid
        when = prtime(minute)
        if url not in places:
            cur = db.execute(
                "INSERT INTO moz_places (url, title, rev_host, visit_count, typed, frecency, "
                "last_visit_date, guid, url_hash, origin_id) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (url, title, u.hostname[::-1] + ".", 0, int(vtype == 2), rng.randint(50, 3000),
                 when, guid(), int.from_bytes(hashlib.sha1(url.encode()).digest()[:6], "big"),
                 origins[okey]))
            places[url] = cur.lastrowid
        pid = places[url]
        db.execute("UPDATE moz_places SET visit_count = visit_count + 1, last_visit_date = ? "
                   "WHERE id = ?", (when, pid))
        from_visit = last_visit if vtype in (1, 5) else 0
        cur = db.execute("INSERT INTO moz_historyvisits (from_visit, place_id, visit_date, "
                         "visit_type, session, source) VALUES (?,?,?,?,0,0)",
                         (from_visit or 0, pid, when, vtype))
        last_visit = cur.lastrowid

    # Typed URL bar input that led to pages.
    for suffix, text in [("//yinzpaste.example/", "yinzp"), ("//www.mlb.com/pirates", "mlb")]:
        pid = next(i for u, i in places.items() if u.endswith(suffix))
        db.execute("INSERT INTO moz_inputhistory VALUES (?,?,?)", (pid, text, 1))

    # Bookmarks: standard roots plus a toolbar with the mail link.
    now = prtime(0, False)
    roots = [(1, 2, None, 0, 0, "", "root________"), (2, 2, None, 1, 0, "menu", "menu________"),
             (3, 2, None, 1, 1, "toolbar", "toolbar_____"), (4, 2, None, 1, 2, "tags", "tags________"),
             (5, 2, None, 1, 3, "unfiled", "unfiled_____"), (6, 2, None, 1, 4, "mobile", "mobile______")]
    for r in roots:
        db.execute("INSERT INTO moz_bookmarks (id, type, fk, parent, position, title, dateAdded, "
                   "lastModified, guid) VALUES (?,?,?,?,?,?,?,?,?)", r[:6] + (now, now, r[6]))
    for pos, host in enumerate(["mail.signalco.local", "intranet.signalco.local"]):
        url = next(u for u in places if urlsplit(u).hostname == host)
        db.execute("INSERT INTO moz_bookmarks (type, fk, parent, position, title, dateAdded, "
                   "lastModified, guid) VALUES (1,?,3,?,?,?,?,?)",
                   (places[url], pos, None, now, now, guid()))
        db.execute("UPDATE moz_places SET foreign_count = foreign_count + 1 WHERE id = ?", (places[url],))

    # A download record (Firefox keeps these as annotations on the source page).
    db.executemany("INSERT INTO moz_anno_attributes (id, name) VALUES (?,?)",
                   [(1, "downloads/destinationFileURI"), (2, "downloads/metaData")])
    src = next(i for u, i in places.items() if u.endswith("/Gen4-Bid/pricing/export"))
    t = prtime(196)
    db.execute("INSERT INTO moz_annos (place_id, anno_attribute_id, content, flags, expiration, "
               "type, dateAdded, lastModified) VALUES (?,?,?,0,4,3,?,?)",
               (src, 1, "file:///C:/Users/dkowalski/Downloads/Gen4_Bid_Pricing_FINAL.xlsx", t, t))
    db.execute("INSERT INTO moz_annos (place_id, anno_attribute_id, content, flags, expiration, "
               "type, dateAdded, lastModified) VALUES (?,?,?,0,4,3,?,?)",
               (src, 2, '{"state":1,"deleted":false,"endTime":%d,"fileSize":48213}' % (t // 1000), t, t))
    db.commit()
    db.execute("VACUUM")
    db.close()


def build_formhistory(path):
    db = sqlite3.connect(path)
    db.executescript("""
    PRAGMA user_version = 5;
    CREATE TABLE moz_formhistory (id INTEGER PRIMARY KEY, fieldname TEXT NOT NULL,
        value TEXT NOT NULL, timesUsed INTEGER, firstUsed INTEGER, lastUsed INTEGER, guid TEXT);
    CREATE TABLE moz_deleted_formhistory (id INTEGER PRIMARY KEY, timeDeleted INTEGER, guid TEXT);
    CREATE TABLE moz_sources (id INTEGER PRIMARY KEY, source TEXT NOT NULL);
    CREATE TABLE moz_history_to_sources (history_id INTEGER, source_id INTEGER,
        PRIMARY KEY (history_id, source_id));
    CREATE INDEX moz_formhistory_index ON moz_formhistory (fieldname);
    """)
    entries = [
        ("searchbar-history", "liberty ave traffic signal timing", 55),
        ("username", "dkowalski", 3),
        ("searchbar-history", "pirates score", 120),
        ("searchbar-history", "lunch near smithfield st", 240),
        ("searchbar-history", "how to send a file without work email", 1462),
        ("searchbar-history", "paste site that deletes after reading", 1464),
        ("searchbar-history", "hide text from dlp scanner", 1470),
        ("searchbar-history", "cyberchef", 1473),
        ("paste_title", "bid numbers for TRTS", 1485),
        ("paste_body", encoded_flag(), 1485),
        ("paste_expire", "burn after reading", 1485),
        ("email", "dana.k.pgh@webmail.example", 1490),
        ("searchbar-history", "how to clear firefox history", 1500),
    ]
    for field, value, minute in entries:
        t = prtime(minute)
        db.execute("INSERT INTO moz_formhistory (fieldname, value, timesUsed, firstUsed, lastUsed, "
                   "guid) VALUES (?,?,1,?,?,?)", (field, value, t, t, guid()))
    db.commit()
    db.execute("VACUUM")
    db.close()


PREFS = """// Mozilla User Preferences

// DO NOT EDIT THIS FILE.
user_pref("browser.startup.homepage_override.mstone", "131.0");
user_pref("browser.download.dir", "C:\\\\Users\\\\dkowalski\\\\Downloads");
user_pref("browser.download.lastDir", "C:\\\\Users\\\\dkowalski\\\\Downloads");
user_pref("browser.search.region", "US");
user_pref("browser.sessionstore.resume_from_crash", true);
user_pref("privacy.sanitize.sanitizeOnShutdown", false);
"""


def main():
    visits = load_visits()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        build_places(tmp / "places.sqlite", visits)
        build_formhistory(tmp / "formhistory.sqlite")
        files = {
            "places.sqlite": (tmp / "places.sqlite").read_bytes(),
            "formhistory.sqlite": (tmp / "formhistory.sqlite").read_bytes(),
            "prefs.js": PREFS.encode(),
            "times.json": b'{"created":1693502400000,"firstUse":null}',
            "compatibility.ini": b"[Compatibility]\nLastVersion=131.0_20241001000000/20241001000000\nLastOSABI=WINNT_x86_64-msvc\n",
        }
    OUT.parent.mkdir(exist_ok=True)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(files):
            info = zipfile.ZipInfo(f"{PROFILE}/{name}", date_time=(2026, 9, 30, 9, 15, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, files[name])
    OUT.write_bytes(buf.getvalue())
    print(f"wrote {OUT} ({len(visits)} visits); paste_body = {encoded_flag()}")


if __name__ == "__main__":
    main()
