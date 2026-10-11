# Walkthrough: Ride All Day

The lesson: moving a check into native code makes it slower to read, not
secret. The logic still ships in the APK, and Ghidra reads ARM and x86 code.

1. Open `ride_all_day.apk` in jadx. `MainActivity` sends the typed code to
   `Gate.scan()`, and `Gate` is just:

   ```java
   static native boolean scan(String str);
   static { System.loadLibrary("wristband"); }
   ```

   Searching for `BarSides` finds nothing.

2. Unzip the APK (it is a normal zip) and open `lib/x86_64/libwristband.so`
   in Ghidra (Import, then accept the default analysis). The arm64 build has
   the same logic.

3. In the Symbol Tree, open the export `Java_org_barsides_rideallday_Gate_scan`.
   The decompiled code looks roughly like this:

   ```c
   len   = (**(code **)(*env + 0x540))(env, str);    // GetStringUTFLength
   chars = (**(code **)(*env + 0x548))(env, str, 0); // GetStringUTFChars
   if (len == 0x26) {
     bad = 0;
     for (i = 0; i != 0x26; i++) {
       x = chars[i] ^ KEY[i & 7];
       x = (x << 3) | (x >> 5);                       // rotate left 3
       bad |= (byte)(x + i * 0x11) ^ TABLE[i];
     }
     ok = bad == 0;
   }
   (**(code **)(*env + 0x550))(env, str, chars);     // ReleaseStringUTFChars
   ```

   The JNIEnv offsets are slots 168 to 170 of the standard JNI function table.
   Players don't need to name them, since they only fetch the input string.

4. Follow the two `.rodata` references. `KEY` is 8 bytes, `KENNYWD!`. `TABLE` is
   38 bytes:

   ```
   48 32 03 1b c5 ee 6f 09 09 f2 23 8c 4d e6 f7 f2 51 72 83
   9c 84 86 f7 c9 d1 f2 42 ac 5d 86 07 a1 c0 4a 23 ac 45 c6
   ```

5. Run the steps backwards for each byte: subtract `17*i`, rotate right by 3,
   then XOR with `KEY[i % 8]`:

   ```python
   KEY = b"KENNYWD!"
   T = bytes.fromhex("4832031bc5ee6f0909f2238c4de6f7f25172839c8486f7c9d1f242ac5d8607a1c04a23ac45c6")
   rotr = lambda x, n: ((x >> n) | (x << (8 - n))) & 0xFF
   print("".join(chr(rotr((t - 17 * i) & 0xFF, 3) ^ KEY[i % 8]) for i, t in enumerate(T)))
   ```

   which prints `BarSides{native_code_still_rides_free}`. On a phone, typing that
   code into the app shows "Wristband valid".

`build/solve.py` is the same script.
