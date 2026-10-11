# Head Scratcher walkthrough

The capture has 109 DNS queries from 10.11.12.13 to 172.31.172.31, all for ordinary domains (example.com, wikipedia.org, ...). The names are a decoy. The data is in the DNS header: each query's 16-bit transaction ID carries one character.

- A transaction ID with high byte `0xF0` starts a new record (low byte is its length).
- Every other ID has a high byte counting up from `0x80`; the low byte with its top bit cleared (`& 0x7F`) is one ASCII character.

In Wireshark, add `dns.id` as a column with the filter `dns.flags.response == 0`, then decode the IDs. With tshark and Python:

```
tshark -r challenge.pcap -Y "dns.flags.response == 0" -T fields -e dns.id \
  | python3 -c "import sys; print(''.join('|' if int(l,16)>>8==0xf0 else chr(int(l,16)&0x7f) for l in sys.stdin))"
```

Output:

```
|sid:TSV4RRFFQ6KHMA01|prod:Windows NT Workstation|usr:JKos,pass:tunicLif3|flag:BarSides{h1d1ng_1n_th3_h34d3r}
```

Flag: `BarSides{h1d1ng_1n_th3_h34d3r}`
