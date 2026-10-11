#!/usr/bin/env python3
"""Reference solver for Detour (organizers only). Usage: python3 solve.py HOST PORT"""
import heapq
import socket
import sys


def fastest(lines):
    graph = {}
    for line in lines:
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
            return d
        if d > best[here]:
            continue
        for there, w in graph[here]:
            if d + w < best.get(there, float("inf")):
                best[there] = d + w
                heapq.heappush(queue, (d + w, there))


def main():
    sock = socket.create_connection((sys.argv[1], int(sys.argv[2])))
    buf = b""
    while True:
        chunk = sock.recv(65536)
        if not chunk:
            print(buf.decode())
            return
        buf += chunk
        if buf.endswith(b"minutes> "):
            text = buf.decode()
            rnd = text[text.rfind("ROUND"):]
            sock.sendall(f"{fastest(rnd.splitlines())}\n".encode())
            print(rnd.splitlines()[0], "->", fastest(rnd.splitlines()))
            buf = b""


if __name__ == "__main__":
    main()
