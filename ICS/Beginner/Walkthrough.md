# Walkthrough: Pump Station Gossip

1. Open `tag_list.csv`. The last row, `MAINT`, is the maintenance note in holding registers 40101-40164, "2 characters per register".
2. Modbus tools use zero-based addresses, so 40101 is holding register address 100. Read it:

   ```
   python3 modbus_read.py EVENT_HOST 8007 holding 100 24
     100  16993  0x4261
     101  29267  0x7253
     ...
   ```

3. Each register is two bytes: `0x4261` is `B` `a`. Paste the hex column into CyberChef with **From Hex** (or run `bytes.fromhex(...)` in Python) to get the flag:

   `BarSides{plcs_will_tell_anyone_who_asks}`

With mbpoll: `mbpoll -m tcp -p 8007 -t 4:hex -r 101 -c 24 EVENT_HOST` (mbpoll counts from 1).

Lesson: classic Modbus has no authentication or encryption. Anyone who can reach port 502 can read (and on most PLCs, write) every value.
