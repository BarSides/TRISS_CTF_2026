# Name

Lost Badge

## Author

@justinforbes

## Overview

After last week's BarSides meetup at Stinky's Bar & Grill in Lawrenceville, somebody left their TRISS 2026 speaker badge on the bar. BarSides posted a photo of it on Yinzr, the local social network, and the bartender will only hand it back for the claim code printed on the back.

Speakers are terrible at keeping secrets. Track down the badge's owner on Yinzr and find the claim code.

There's no Internet here, so Yinzr is the whole world for this one.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

Yinzr listens on port 8012 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `http://EVENT_HOST:8012`. Nothing is attached.

Yinzr is a fake social network in `app.py` (Python standard library on Alpine, no CDN or web fonts, so it runs fully offline). The home feed shows BarSides' photo of the badge: "Rosie K.", a TRISS 2026 speaker, with the Yinzr handle `@pierogi_` and a thumb over the rest. People search for `pierogi` (or `rosie`) turns up five lookalikes. Two are TRISS speakers named Rosie: `@pierogi_payloads` posted that they were stuck in Columbus the night of the meetup, while `@pierogi_packets` posted from Stinky's that night and pinned the badge claim code (the flag) to their profile. Search only covers names and handles, not post text, so players can't search for the flag directly.

Every person on Yinzr is fictional; only BarSides, TRISS, Stinky's and Lawrenceville are real. The badge photo is drawn by `build/make_badge.py` (needs Pillow) and committed as `static/badge.jpg`, so the image build needs nothing extra. The flag can be changed with the `FLAG` environment variable. Solution notes are in `Walkthrough.md`.

## Flag

BarSides{pivot_on_the_handle}
