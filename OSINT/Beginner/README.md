# Name

Where Was This?

## Author

@justinforbes

## Overview

The night before TRISS, one of the BarSides crew posted this photo with the caption "Pre-game's here, come find us." No bar name, no address, no reply to anyone asking where "here" is.

Phones remember more than people say. Work out the street address where the photo was taken. There's no Internet at the venue, so a map of the neighborhood is attached.

Flag format: BarSides{housenumber_streetname} in lowercase, for example BarSides{1234_example_street}

## Setup

File challenge. Attach `files/pregame.jpg` and `files/lawrenceville_map.png` in CTFd. Nothing is hosted.

The photo's EXIF holds GPS coordinates for Stinky's Bar & Grill, 4901 Hatfield St in Lawrenceville (40.477683 N, 79.957717 W), plus a Pixel 8 camera model and a timestamp of 2026-10-15 19:12. CyberChef's Extract EXIF shows the coordinates as decimal degrees (tested with the event's CyberChef v10.19.4); exiftool or an image viewer's properties panel work too. Players then find that point on the attached map, which has a latitude/longitude grid (labelled every 0.0005 degrees, faint lines every 0.0001) and a house number on every lot. The point lands in the middle of lot 4901 on Hatfield St, about 11 m from its neighbors.

Since players can't look anything up at the venue, knowing the bar is Stinky's doesn't give away the house number. Both `BarSides{4901_hatfield_street}` and `BarSides{4901_hatfield_st}` are accepted, case-insensitive.

The map is drawn by `build/make_files.py` (needs Pillow and DejaVu fonts), not taken from a map service, so it has no licensing strings attached. Only Stinky's position is real; the streets and lots around it are a simplified sketch of the Lawrenceville grid (Butler and Hatfield running northeast, numbered streets crossing them) and the map says so. Rerun the script to regenerate both files. Solution notes are in `Walkthrough.md`.

## Flag

BarSides{4901_hatfield_street}
