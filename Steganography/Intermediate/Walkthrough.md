# Nesting Dolls: walkthrough

The file is three layers deep: a normal JPEG, EXIF metadata holding a password, and a password-protected ZIP appended after the JPEG's end-of-image marker (`FF D9`). Image viewers stop at that marker, so the postcard opens normally.

1. **Notice something's off.** The picture is simple flat art but the file is about 120 KB. `file postcard.jpg`, `strings postcard.jpg` (look for `PK` and `postcard_back.txt` near the end) or CyberChef's **Extract Files** (it lists a JPEG at 0x0 and ZIP data near the end) all show there is more than an image.
2. **Find the password.** CyberChef **Extract EXIF** (or `exiftool postcard.jpg`) shows:
   `ImageDescription: Back of the card is locked. Password: incline1877`
3. **Open the ZIP.** In CyberChef, load the whole file and add **Unzip** with password `incline1877`. It lists `postcard_back.txt`; open it to read the back of the postcard and the flag.
   - Command line: `unzip -P incline1877 postcard.jpg`, or `7z x postcard.jpg`.
   - Windows: rename to `postcard.zip` and open it with 7-Zip.
   - The ZIP's offsets were adjusted (`zip -A`) so the whole file works as a ZIP. Unzipping only the pieces CyberChef's Extract Files carves out will fail, because Extract Files splits the archive in two; use Unzip on the whole file instead.

Flag: `BarSides{postcards_have_two_sides}`
