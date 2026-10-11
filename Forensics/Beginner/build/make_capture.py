#!/usr/bin/env python3
"""Build files/stadium_office.pcap for Forensics Beginner "Rigged Race".

Organizers only; do not attach. Needs Pillow and the DejaVu fonts.
The flag is drawn into a PNG, so strings/grep on the capture won't find it;
players have to pull the image out (Wireshark File > Export Objects > HTTP).
"""
import io
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FLAG = "BarSides{plain_http_spills_the_pierogies}"
OUT = Path(__file__).resolve().parent.parent / "files" / "stadium_office.pcap"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CLIENT_MAC = bytes.fromhex("3c22fb1a2b4c")
SERVER_MAC = bytes.fromhex("00163e5d7a01")
GATEWAY_MAC = bytes.fromhex("00163e000001")
CLIENT_IP = "10.20.4.37"
SERVER_IP = "10.20.1.15"
DNS_IP = "10.20.0.2"
HOST = "racedesk.stadium.local"


# ---------- content served by the fake intranet ----------

def png_bytes(img):
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def make_logo():
    img = Image.new("RGB", (160, 60), (253, 184, 39))
    d = ImageDraw.Draw(img)
    d.text((12, 16), "RACE DESK", font=ImageFont.truetype(FONT, 22), fill=(20, 20, 20))
    return png_bytes(img)


def make_results():
    img = Image.new("RGB", (900, 520), (250, 248, 240))
    d = ImageDraw.Draw(img)
    big, mid, small = (ImageFont.truetype(FONT, s) for s in (40, 28, 22))
    reg = ImageFont.truetype(FONT_REG, 22)
    d.rectangle([0, 0, 900, 80], fill=(20, 20, 20))
    d.text((30, 18), "GREAT PIEROGI RACE - FINAL ORDER", font=big, fill=(253, 184, 39))
    d.text((30, 100), "Thursday home game, 5th inning. DO NOT SHARE.", font=reg, fill=(150, 30, 30))
    order = ["1. Sauerkraut Saul", "2. Cheese Chester", "3. Jalapeno Hannah",
             "4. Potato Pete", "5. Bacon Burt", "6. Oliver Onion"]
    for i, row in enumerate(order):
        d.text((60, 150 + i * 40), row, font=mid, fill=(20, 20, 20))
    d.rectangle([30, 420, 870, 490], outline=(20, 20, 20), width=3)
    d.text((50, 440), FLAG, font=small, fill=(20, 20, 20))
    return png_bytes(img)


INDEX = f"""<!doctype html>
<html><head><title>Race Desk</title><link rel="stylesheet" href="/style.css"></head>
<body>
<img src="/img/logo.png" alt="Race Desk">
<h1>Race Desk intranet</h1>
<p>Internal site for the in-game entertainment crew.</p>
<ul>
  <li><a href="/schedule.html">Race schedule</a></li>
  <li><a href="/notes.txt">Crew notes</a></li>
</ul>
</body></html>
""".encode()

STYLE = b"""body { font-family: sans-serif; background: #fafaf0; margin: 2em; }
h1 { color: #141414; border-bottom: 4px solid #fdb827; }
a { color: #8a1c1c; }
"""

SCHEDULE = b"""<!doctype html>
<html><head><title>Race schedule</title><link rel="stylesheet" href="/style.css"></head>
<body>
<h1>Pierogi race schedule</h1>
<table>
<tr><th>Date</th><th>Opponent</th><th>Inning</th></tr>
<tr><td>Tue</td><td>Cincinnati</td><td>5th</td></tr>
<tr><td>Wed</td><td>Cincinnati</td><td>5th</td></tr>
<tr><td>Thu</td><td>Milwaukee</td><td>5th</td></tr>
</table>
<p>Winners are decided by the crew ahead of time. Keep the final order off the public site.</p>
</body></html>
"""

NOTES = b"""Crew notes
----------
- Costumes back to the cage after every game.
- Saul's left shoe needs re-gluing.
- Thursday's final order is uploaded as /private/race_results.png
  The /private folder is NOT linked from anywhere, so nobody will find it. Right?
"""


# ---------- packet building ----------

def ip2b(ip):
    return bytes(int(x) for x in ip.split("."))


def csum(data):
    if len(data) % 2:
        data += b"\0"
    s = sum(struct.unpack(f"!{len(data) // 2}H", data))
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF


class Capture:
    def __init__(self):
        self.t = 1760551200.0  # arbitrary fixed start time so builds are reproducible
        self.packets = []
        self.ip_id = 0x1a2b

    def tick(self, dt):
        self.t += dt

    def ip(self, src, dst, proto, payload, src_mac, dst_mac):
        self.ip_id = (self.ip_id + 1) & 0xFFFF
        hdr = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(payload), self.ip_id,
                          0x4000, 64, proto, 0, ip2b(src), ip2b(dst))
        hdr = hdr[:10] + struct.pack("!H", csum(hdr)) + hdr[12:]
        frame = dst_mac + src_mac + b"\x08\x00" + hdr + payload
        self.packets.append((self.t, frame))
        self.tick(0.0004)

    def udp(self, src, sport, dst, dport, data, src_mac, dst_mac):
        seg = struct.pack("!HHHH", sport, dport, 8 + len(data), 0) + data
        pseudo = ip2b(src) + ip2b(dst) + struct.pack("!BBH", 0, 17, len(seg))
        seg = seg[:6] + struct.pack("!H", csum(pseudo + seg)) + seg[8:]
        self.ip(src, dst, 17, seg, src_mac, dst_mac)

    def tcp(self, src, sport, dst, dport, seq, ack, flags, data, src_mac, dst_mac):
        hdr = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, 5 << 4, flags, 64240, 0, 0)
        pseudo = ip2b(src) + ip2b(dst) + struct.pack("!BBH", 0, 6, len(hdr) + len(data))
        c = csum(pseudo + hdr + data)
        hdr = hdr[:16] + struct.pack("!H", c) + hdr[18:]
        self.ip(src, dst, 6, hdr + data, src_mac, dst_mac)

    def write(self, path):
        out = struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
        for t, frame in self.packets:
            sec = int(t)
            usec = int(round((t - sec) * 1e6))
            out += struct.pack("<IIII", sec, usec, len(frame), len(frame)) + frame
        path.write_bytes(out)


def dns_name(name):
    return b"".join(bytes([len(p)]) + p.encode() for p in name.split(".")) + b"\0"


def dns_lookup(cap, txid, name, answer_ip):
    q = struct.pack("!HHHHHH", txid, 0x0100, 1, 0, 0, 0) + dns_name(name) + struct.pack("!HH", 1, 1)
    cap.udp(CLIENT_IP, 53000 + txid % 1000, DNS_IP, 53, q, CLIENT_MAC, GATEWAY_MAC)
    cap.tick(0.003)
    r = (struct.pack("!HHHHHH", txid, 0x8180, 1, 1, 0, 0) + dns_name(name) + struct.pack("!HH", 1, 1)
         + struct.pack("!HHHIH", 0xC00C, 1, 1, 300, 4) + ip2b(answer_ip))
    cap.udp(DNS_IP, 53, CLIENT_IP, 53000 + txid % 1000, r, GATEWAY_MAC, CLIENT_MAC)
    cap.tick(0.01)


SYN, ACK, PSH, FIN = 0x02, 0x10, 0x08, 0x01
MSS = 1448


def http_get(cap, sport, path, status, ctype, body, think=0.5):
    """One HTTP/1.1 request on its own TCP connection (Connection: close)."""
    c, s = CLIENT_IP, SERVER_IP
    cseq, sseq = (sport * 7919) & 0xFFFFFFFF, (sport * 104729) & 0xFFFFFFFF
    C = lambda seq, ack, fl, d=b"": cap.tcp(c, sport, s, 80, seq, ack, fl, d, CLIENT_MAC, SERVER_MAC)
    S = lambda seq, ack, fl, d=b"": cap.tcp(s, 80, c, sport, seq, ack, fl, d, SERVER_MAC, CLIENT_MAC)

    C(cseq, 0, SYN); cseq += 1
    S(sseq, cseq, SYN | ACK); sseq += 1
    C(cseq, sseq, ACK)

    req = (f"GET {path} HTTP/1.1\r\nHost: {HOST}\r\n"
           "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0\r\n"
           "Accept: */*\r\nConnection: close\r\n\r\n").encode()
    C(cseq, sseq, PSH | ACK, req); cseq += len(req)
    cap.tick(0.002)

    resp = (f"HTTP/1.1 {status}\r\nServer: nginx\r\nContent-Type: {ctype}\r\n"
            f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n").encode() + body
    acked = None
    for i in range(0, len(resp), MSS):
        chunk = resp[i:i + MSS]
        S(sseq, cseq, PSH | ACK if i + MSS >= len(resp) else ACK, chunk); sseq += len(chunk)
        if (i // MSS) % 2 == 1:
            C(cseq, sseq, ACK); acked = sseq
    if acked != sseq:
        C(cseq, sseq, ACK)

    S(sseq, cseq, FIN | ACK); sseq += 1
    C(cseq, sseq, FIN | ACK); cseq += 1
    S(sseq, cseq, ACK)
    cap.tick(think)


def main():
    logo, results = make_logo(), make_results()
    assert b"BarSides" not in results and b"pierogies}" not in results
    cap = Capture()
    dns_lookup(cap, 0x4e21, HOST, SERVER_IP)
    http_get(cap, 50112, "/", "200 OK", "text/html", INDEX, 0.05)
    http_get(cap, 50113, "/style.css", "200 OK", "text/css", STYLE, 0.02)
    http_get(cap, 50114, "/img/logo.png", "200 OK", "image/png", logo, 4.2)
    http_get(cap, 50120, "/schedule.html", "200 OK", "text/html", SCHEDULE, 0.03)
    http_get(cap, 50121, "/style.css", "200 OK", "text/css", STYLE, 6.8)
    http_get(cap, 50127, "/notes.txt", "200 OK", "text/plain", NOTES, 11.5)
    http_get(cap, 50131, "/private/", "403 Forbidden", "text/html",
             b"<html><body><h1>403 Forbidden</h1></body></html>\n", 2.1)
    http_get(cap, 50133, "/private/race_results.png", "200 OK", "image/png", results, 1.0)
    dns_lookup(cap, 0x4e22, "time.stadium.local", "10.20.0.3")
    OUT.parent.mkdir(exist_ok=True)
    cap.write(OUT)
    print(f"wrote {OUT} ({len(cap.packets)} packets, results.png {len(results)} bytes)")


if __name__ == "__main__":
    main()
