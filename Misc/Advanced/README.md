# Name

Detour

## Author

@justinforbes

## Overview

Every road crew in Pittsburgh picked the same week. The city's detour dispatcher reads out which roads are still open and asks for the fastest way between two neighborhoods, over and over, with a stopwatch running.

Get 30 crews home on time in a row and dispatch hands over the flag. The maps grow fast and you get 5 seconds per round, so nobody does this by hand. A starter client is attached.

## Setup

Hosted challenge. `docker compose up -d` in this folder; players connect with `nc EVENT_HOST 8011` or the attached `files/dispatch_client.py` (raw TCP, not a web page).

Each round sends a fresh random map: `ROADS n`, then n lines of `PlaceA PlaceB minutes` (roads work both ways), then `FROM X TO Y` and a `minutes>` prompt. The answer is the shortest path total. Round r has 4+2r places and twice that many roads (round 30: 64 places, 128 roads). Any wrong answer, or an answer later than 5 seconds, ends the connection, so players have to write a script: parse the round, run Dijkstra (or Bellman-Ford, or Floyd-Warshall; all are fast enough), send the number back.

Maps come from `random.SystemRandom` per connection, so a transcript can't be replayed. Each connection is a forked child; the container runs as an unprivileged user with a read-only filesystem. The flag is read from `flag.txt` in the image and is not in `dispatch.py`.

`files/dispatch_client.py` connects, prints each round and sends what the player types, with a marked spot for their solver. `build/solve.py` is the organizers' reference solver (stdlib only); do not attach it.

## Flag

BarSides{dijkstra_knows_every_detour}
