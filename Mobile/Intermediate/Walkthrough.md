# Walkthrough: Pothole Patrol

The lesson: hiding a string by encoding it in the app doesn't help when the
key ships in the same app. Text search fails, so players have to read code.

1. Open `pothole_patrol.apk` in jadx-gui. Searching for `BarSides` finds
   nothing, which is the hint that the flag is built at runtime.
2. `MainActivity` is just the report form and repair queue. The other class,
   `SupervisorConsole`, is never called:

   ```java
   private static final byte[] SEALED = {1, 51, 51, 7, 44, 54, 72, 48, ...};

   static String repairAuthorization(Context context) {
       return unseal(SEALED, context.getString(R.string.dispatch_key));
   }
   // unseal: out[i] = SEALED[i] ^ key.charAt(i % key.length())
   ```

   That is a repeating-key XOR.
3. Double-click `R.string.dispatch_key` (or open Resources > resources.arsc >
   res/values/strings.xml) to find the key:

   ```xml
   <string name="dispatch_key">CRATER-CREW-412</string>
   ```

4. Undo the XOR. In CyberChef, paste the numbers from `SEALED`, then
   **From Decimal** (delimiter Comma) and **XOR** with key `CRATER-CREW-412`
   (UTF8). Or in Python:

   ```python
   d = [1, 51, 51, 7, 44, 54, 72, 48, 41, 53, 56, 89, 92, 94, 94, 38, 33, 30, 36,
        36, 38, 78, 43, 55, 33, 8, 76, 64, 110, 64, 54, 60, 53, 61, 40, 55, 80]
   k = "CRATER-CREW-412"
   print("".join(chr(b ^ ord(k[i % len(k)])) for i, b in enumerate(d)))
   ```

   which prints `BarSides{potholes_patched_at_runtime}`.

All the bytes are below 128, so jadx shows them as plain positive numbers and
From Decimal works without any sign fix-up.
