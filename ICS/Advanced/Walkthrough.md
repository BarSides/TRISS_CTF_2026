# Walkthrough: Crack the Vault

1. Read `vault_lock.scl`. The lock advances one step each time the correct
   value is written to the ENTRY register (40031), and resets on any wrong
   value or when RUN is off. The expected value per step is:

       EXPECTED(i) = (K[i] XOR SEED) + i * STEP_GAIN

   with `SEED = 0x5A`, `STEP_GAIN = 100`, `K = [0x12, 0x34, 0x56, 0x78]`.

2. Compute the four values:

       i=0: (0x12 ^ 0x5A) + 0   = 0x48      = 72
       i=1: (0x34 ^ 0x5A) + 100 = 0x6E+100  = 210
       i=2: (0x56 ^ 0x5A) + 200 = 0x0C+200  = 212
       i=3: (0x78 ^ 0x5A) + 300 = 0x22+300  = 334

   Code: 72, 210, 212, 334.

3. Put the PLC in RUN (coil 00001) and enter the code in order into 40031
   (zero-based address 30):

       python3 modbus_client.py EVENT_HOST 8009 wcoil 0 1
       python3 modbus_client.py EVENT_HOST 8009 wreg 30 72
       python3 modbus_client.py EVENT_HOST 8009 wreg 30 210
       python3 modbus_client.py EVENT_HOST 8009 wreg 30 212
       python3 modbus_client.py EVENT_HOST 8009 wreg 30 334

4. Confirm the step counter (40041 -> address 40) reads 4, then read the note
   from 40201+ and decode the hex (CyberChef From Hex, two bytes per register):

       python3 modbus_client.py EVENT_HOST 8009 read holding 40 1    -> 4
       python3 modbus_client.py EVENT_HOST 8009 read holding 200 24

   `BarSides{i_read_the_ladder_and_walked_right_in}`

A wrong value at any step resets the counter to 0, so enter the four in order.
Coil 00002 is a reset button if you want to start over.

Lesson: safety and access logic living only inside the PLC program is not a
secret. Anyone who can read a controller backup can reconstruct it.
