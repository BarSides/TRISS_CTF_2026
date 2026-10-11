# Rigged Race walkthrough

1. Open `stadium_office.pcap` in Wireshark and apply the display filter `http`.
2. The office PC (10.20.4.37) browses `racedesk.stadium.local`: the home page, a schedule, and `/notes.txt`.
3. Follow the TCP stream for `/notes.txt` (right click > Follow > TCP Stream). The crew note says the final order was uploaded as `/private/race_results.png` and that nobody will find it because it isn't linked.
4. The PC tries `/private/` (403 Forbidden) and then fetches `/private/race_results.png` directly (200 OK).
5. File > Export Objects > HTTP, select `race_results.png`, Save, and open it. The flag is printed at the bottom of the results.

Command line alternative:

```sh
tshark -r stadium_office.pcap -q --export-objects http,out
```

Flag: `BarSides{plain_http_spills_the_pierogies}`
