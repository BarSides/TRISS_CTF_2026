# Detour walkthrough

1. Connect with `nc EVENT_HOST 8011` and read round 1. It is a tiny weighted map:

   ```
   ROUND 1/30
   ROADS 10
   Shadyside Squirrel_Hill_South 6
   ...
   FROM Chartiers TO South_Side_Slopes
   minutes>
   ```

   Round 1 can be done on paper, but the maps grow by two places a round and there are only 5 seconds to answer.
2. This is the shortest path problem. Dijkstra's algorithm solves it: keep a priority queue of (time so far, place), always expand the cheapest place next, and stop when you pop the destination.
3. Fill in `ask_human()` in the attached `dispatch_client.py` so it parses the round and returns the answer:

   ```python
   import heapq

   def ask_human(round_text):
       text = round_text[round_text.rfind("ROUND"):]
       graph = {}
       for line in text.splitlines():
           parts = line.split()
           if len(parts) == 3 and parts[2].isdigit():
               a, b, w = parts[0], parts[1], int(parts[2])
               graph.setdefault(a, []).append((b, w))
               graph.setdefault(b, []).append((a, w))
           elif parts[:1] == ["FROM"]:
               start, end = parts[1], parts[3]
       best, queue = {start: 0}, [(0, start)]
       while queue:
           d, here = heapq.heappop(queue)
           if here == end:
               return str(d)
           if d > best[here]:
               continue
           for there, w in graph[here]:
               if d + w < best.get(there, float("inf")):
                   best[there] = d + w
                   heapq.heappush(queue, (d + w, there))
   ```

   Take the text from the last `ROUND` onward, because the client's buffer also holds "Correct!" and the banner. Python's `networkx.shortest_path_length(G, s, t, weight="weight")` also works if players have it installed.
4. Run it. After round 30 the dispatcher prints the flag.

Flag: `BarSides{dijkstra_knows_every_detour}`
