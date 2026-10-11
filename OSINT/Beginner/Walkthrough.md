# Where Was This? walkthrough

1. Load `pregame.jpg` into CyberChef and run **Extract EXIF** (or `exiftool -n pregame.jpg`).
2. The output includes:
   ```
   Model: Pixel 8
   GPSLatitudeRef: N
   GPSLatitude: 40.47768333333334
   GPSLongitudeRef: W
   GPSLongitude: -79.95771666666667
   ```
   (Tools that print degrees, minutes and seconds show 40° 28' 39.66" N, 79° 57' 27.78" W. Decimal = degrees + minutes/60 + seconds/3600, and west is negative.)
3. Open `lawrenceville_map.png`. Latitude 40.4777 sits just above the 40.4775 line, almost two faint lines up. Longitude -79.9577 is between the -79.9580 and -79.9575 lines, almost three faint lines east of -79.9580.
4. That point is inside the lot numbered **4901**, on the river side of **Hatfield St** at the corner of 49th St.
5. Flag: `BarSides{4901_hatfield_street}` (`BarSides{4901_hatfield_st}` also works).

It's Stinky's Bar & Grill, where BarSides meets. Lesson: unless the app strips it, a phone photo's EXIF can give away exactly where you were standing.
