#!/usr/bin/env python3
"""Detour: a fastest-route speed quiz over raw TCP. Players must script it."""
import heapq
import os
import random
import socketserver
import time

PORT = int(os.environ.get("PORT", "1337"))
FLAG = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "flag.txt")).read().strip()

ROUNDS = 30
SECONDS_PER_ROUND = 5

PLACES = """
Allentown Arlington Banksville Beechview Beltzhoover Bloomfield Bluff Brighton_Heights
Brookline Carrick Central_Lawrenceville Chartiers Chateau Crafton_Heights Crawford-Roberts
Downtown East_Allegheny East_Carnegie East_Hills East_Liberty Elliott Esplen Fairywood
Fineview Friendship Garfield Glen_Hazel Greenfield Hays Hazelwood Highland_Park Homewood
Knoxville Larimer Lincoln_Place Lower_Lawrenceville Manchester Marshall-Shadeland
Morningside Mount_Washington Mount_Oliver North_Oakland North_Shore Northview_Heights
Oakwood Overbrook Perry_North Perry_South Point_Breeze Polish_Hill Regent_Square
Ridgemont Shadyside Sheraden South_Oakland South_Side_Flats South_Side_Slopes
Spring_Garden Spring_Hill Squirrel_Hill_North Squirrel_Hill_South Stanton_Heights
Strip_District Summer_Hill Swisshelm_Park Terrace_Village Troy_Hill Upper_Hill
Upper_Lawrenceville West_End Westwood Windgap
""".split()

BANNER = """\
==========================================================
  PITTSBURGH DETOUR DISPATCH
  Every road crew in the city picked the same week.
==========================================================
Each round lists the roads that are still open and how many
minutes each one takes (both directions). Reply with the
fastest total time, in minutes, between the two places asked.

Answer {rounds} rounds in a row. You get {secs} seconds per round,
and the maps grow fast. Nobody does this by hand.
"""


def make_round(rng, n_places, n_extra):
    places = rng.sample(PLACES, n_places)
    roads = {}
    # Random spanning tree keeps the map connected, extra roads add choices.
    for i in range(1, n_places):
        a, b = places[i], places[rng.randrange(i)]
        roads[frozenset((a, b))] = rng.randint(2, 25)
    while len(roads) < n_places - 1 + n_extra:
        a, b = rng.sample(places, 2)
        roads.setdefault(frozenset((a, b)), rng.randint(2, 25))
    start, end = rng.sample(places, 2)
    road_list = [(*sorted(k), v) for k, v in roads.items()]
    rng.shuffle(road_list)
    return road_list, start, end


def fastest(road_list, start, end):
    graph = {}
    for a, b, w in road_list:
        graph.setdefault(a, []).append((b, w))
        graph.setdefault(b, []).append((a, w))
    best = {start: 0}
    queue = [(0, start)]
    while queue:
        d, here = heapq.heappop(queue)
        if here == end:
            return d
        if d > best[here]:
            continue
        for there, w in graph[here]:
            nd = d + w
            if nd < best.get(there, nd + 1):
                best[there] = nd
                heapq.heappush(queue, (nd, there))
    raise ValueError("disconnected")


class Handler(socketserver.StreamRequestHandler):
    def send(self, text):
        self.wfile.write(text.encode())

    def handle(self):
        self.connection.settimeout(SECONDS_PER_ROUND + 1)
        rng = random.SystemRandom()
        self.send(BANNER.format(rounds=ROUNDS, secs=SECONDS_PER_ROUND))
        for r in range(1, ROUNDS + 1):
            n_places = min(4 + 2 * r, len(PLACES))
            road_list, start, end = make_round(rng, n_places, n_extra=n_places)
            answer = fastest(road_list, start, end)
            lines = [f"\nROUND {r}/{ROUNDS}", f"ROADS {len(road_list)}"]
            lines += [f"{a} {b} {w}" for a, b, w in road_list]
            lines.append(f"FROM {start} TO {end}")
            self.send("\n".join(lines) + "\nminutes> ")
            began = time.monotonic()
            try:
                raw = self.rfile.readline(64)
            except OSError:
                self.send("\nToo slow. The detour signs changed again.\n")
                return
            if not raw:
                return
            if time.monotonic() - began > SECONDS_PER_ROUND:
                self.send("Too slow. The detour signs changed again.\n")
                return
            reply = raw.decode("ascii", "replace").strip()
            if reply != str(answer):
                self.send(f"Wrong. The fastest way was {answer} minutes.\n")
                return
            self.send("Correct!\n")
        self.send(f"\nYou got every crew home on time. Dispatch says thanks: {FLAG}\n")


class Server(socketserver.ForkingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    print(f"detour dispatch listening on {PORT}", flush=True)
    Server(("0.0.0.0", PORT), Handler).serve_forever()
