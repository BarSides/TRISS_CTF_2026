# Walkthrough: Parking Chair

The lesson: anything shipped inside an app is readable by whoever has the
app. An APK is a zip holding `classes.dex` (the compiled Java), and jadx turns
that back into readable Java.

1. Open `parking_chair.apk` in jadx-gui (or run `jadx -d out parking_chair.apk`).
2. The manifest (Resources > AndroidManifest.xml) names the launcher screen,
   `org.barsides.parkingchair.MainActivity`.
3. In `MainActivity.onCreate`, the "Move the chair" button passes the typed
   code to `ChairLock.isOwner(...)` and, on success, shows
   `ChairLock.ownerReceipt()`.
4. Open `ChairLock`:

   ```java
   private static final String OWNER_CODE = "SNOWMAGEDDON-2010";
   private static final String RECEIPT = "BarSides{the_chair_was_hardcoded}";
   ```

   The flag is right there. Text search (Navigation > Text search for
   `BarSides`) finds it in one step too.

Players with an Android phone can sideload the APK, type `SNOWMAGEDDON-2010`
and see "Chair moved. Receipt: BarSides{the_chair_was_hardcoded}", but nobody
needs to.

This is the warm-up for Mobile Intermediate (flag assembled at runtime, so a
text search finds nothing) and Advanced (check hidden in a native library).
