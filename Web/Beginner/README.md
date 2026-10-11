# Name

Staff Only

## Author

@justinforbes

## Overview

The Great Pierogi Race fan site has a secret backstage page where the racers pick up their passes. It isn't linked anywhere, and the site's staff swear that only staff can get in. Find the backstage page and talk your way past the door.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

The site listens on port 8004 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `http://EVENT_HOST:8004`.

Two steps, browser only. `/robots.txt` disallows `/backstage/`. That page sets a cookie `staff=false` and shows "STAFF ONLY"; changing the cookie to `staff=true` (any case) in developer tools and reloading shows the flag. `app.py` is Python standard library on Alpine with local CSS, so it runs fully offline. The flag can be changed with the `FLAG` environment variable. Solution notes are in `Walkthrough.md`.

## Flag

BarSides{robots_txt_is_a_map_not_a_lock}
