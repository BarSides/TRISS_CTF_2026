# Name

Scoreboard Math

## Author

@justinforbes

## Overview

The Pierogies' scoreboard operator got tired of doing batting averages in their head, so the IT intern wrote them a little math console. It runs real Python, but the intern blocked every word that could "hurt the scoreboard", so it's totally safe.

The intern also left `flag.txt` next to the console on the server. The console's source is attached. Connect to it and read the flag.

## Setup

Hosted challenge. `docker compose up -d` in this folder; players connect with `nc EVENT_HOST 8010` (raw TCP, not a web page). Attach `files/scoreboard.py` as a CTFd download so players can read the blocklist.

The console `eval`s each line with Python's builtins available, after rejecting any line containing `import`, `open`, `os`, `system`, `exec`, `eval`, `compile`, `flag`, `subprocess`, `breakpoint`, `help` or `input` (case insensitive), and lines over 120 characters. The filter only checks the text the player typed, so building the blocked words out of pieces gets past it:

```
getattr(__builtins__, 'op'+'en')('fl'+'ag.txt').read()
```

Each connection is a forked child with a 5 second limit per expression and a 256 MB memory cap, so runaway math like `9**9**9` only drops that player's connection. The container runs as an unprivileged user with a read-only filesystem, so players can't delete or rewrite the flag. If someone kills the server process the container exits and `restart: unless-stopped` brings it back.

`flag.txt` is the only copy of the flag inside the image; `files/scoreboard.py` is the same as the server's `scoreboard.py` and contains no flag.

## Flag

BarSides{string_glue_beats_word_filters}
