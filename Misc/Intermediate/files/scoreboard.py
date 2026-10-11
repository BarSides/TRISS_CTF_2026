#!/usr/bin/env python3
"""Pierogies scoreboard math console: a Python eval jail over raw TCP."""
import builtins
import os
import resource
import signal
import socketserver

PORT = int(os.environ.get("PORT", "1337"))

BANNER = b"""\
================================================
  PIEROGIES PARK SCOREBOARD CONSOLE
  Math helper for the scoreboard operator
================================================
Type a math expression and press Enter.
Examples:  3*7+2   round(149/532, 3)   sum([4, 2, 7])
Words that could hurt the scoreboard are blocked.
Type quit to leave.
"""

BLOCKED = [
    "import", "open", "os", "system", "exec", "eval", "compile",
    "flag", "subprocess", "breakpoint", "help", "input",
]
MAX_LEN = 120


def blocked_word(line):
    lower = line.lower()
    for word in BLOCKED:
        if word in lower:
            return word
    return None


def calculate(line):
    word = blocked_word(line)
    if word:
        return f"Blocked: '{word}' is not allowed on the scoreboard."
    if len(line) > MAX_LEN:
        return f"Too long: keep it under {MAX_LEN} characters."
    # Runaway math (9**9**9) kills this connection only; each one is a forked child.
    signal.alarm(5)
    try:
        result = eval(line, {"__builtins__": builtins}, {})
    except Exception as exc:
        return f"Error: {type(exc).__name__}: {exc}"
    finally:
        signal.alarm(0)
    return repr(result)[:2000]


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        self.connection.settimeout(300)
        resource.setrlimit(resource.RLIMIT_AS, (256 << 20, 256 << 20))
        self.wfile.write(BANNER)
        while True:
            self.wfile.write(b"\nscore> ")
            try:
                raw = self.rfile.readline(4096)
            except OSError:
                return
            if not raw:
                return
            line = raw.decode("utf-8", "replace").strip()
            if line in ("quit", "exit"):
                self.wfile.write(b"Go Pierogies!\n")
                return
            if not line:
                continue
            self.wfile.write(calculate(line).encode() + b"\n")


class Server(socketserver.ForkingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    print(f"scoreboard console listening on {PORT}", flush=True)
    Server(("0.0.0.0", PORT), Handler).serve_forever()
