#!/usr/bin/env python3
"""Phish Sandwich (TRISS CTF 2026, AI Intermediate).

Players must get a gift card scam past SpamSieve, a Naive Bayes mail filter.
The email has to keep the scam words, so the only way through is to pad it with
words the model associates with normal staff mail. Standard library only.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from filter import score, tokens

FLAG = os.environ.get("FLAG", "BarSides{bury_the_phish_in_good_words}")
HERE = Path(__file__).parent
MODEL = json.loads((HERE / "model.json").read_text())
MAX_LEN = 2000
INBOX = 0.01  # spam probability below this lands in the inbox
SPAM = 0.5    # at or above this goes to the spam folder; in between is held for review

REQUIRED = [
    ("urgent", {"urgent"}),
    ("gift", {"gift"}),
    ("card or cards", {"card", "cards"}),
    ("send", {"send"}),
    ("code or codes", {"code", "codes"}),
]


def check(text):
    words = tokens(text)
    missing = [label for label, options in REQUIRED if not words & options]
    prob, parts = score(MODEL, text)
    if prob >= SPAM:
        verdict = "spam"
    elif prob >= INBOX:
        verdict = "held"
    else:
        verdict = "inbox"
    result = {
        "spam_probability": round(prob, 4),
        "verdict": verdict,
        "missing": missing,
        "words": [{"word": w, "weight": wt} for w, wt in parts],
    }
    if verdict == "inbox" and not missing:
        result["flag"] = FLAG
    return result


class Handler(BaseHTTPRequestHandler):
    server_version = "SpamSieve/1.0"

    def _send(self, status, body, ctype):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, (HERE / "static" / "index.html").read_bytes(), "text/html; charset=utf-8")
        else:
            self._send(404, b"Not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/check":
            return self._send(404, b"Not found", "text/plain")
        try:
            length = min(int(self.headers.get("Content-Length", 0)), 8192)
            text = str(json.loads(self.rfile.read(length) or b"{}").get("email", ""))[:MAX_LEN]
        except (ValueError, AttributeError):
            return self._send(400, b'{"error": "bad request"}', "application/json")
        self._send(200, json.dumps(check(text)).encode(), "application/json")

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"SpamSieve is listening on port {port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
