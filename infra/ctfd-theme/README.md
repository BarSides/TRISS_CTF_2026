# BarSides CTFd theme

A CTFd 3.8 theme in the BarSides look from barsides.com: dark first, C64 Pro pixel type on an 8px grid, gold for the main action, quiet grey surfaces, and the logo's rainbow used once. Players can still switch to light mode with the sun/moon button.

It is a thin layer over CTFd's built-in `core` theme. `barsides/` only holds what changes (the page frame, the top bar, one stylesheet, fonts and logos), and CTFd falls back to `core` for every other template and script. That is CTFd's default (`THEME_FALLBACK` is on), so nothing needs configuring. Everything is served from the theme folder, so it works with no Internet.

```
barsides/
  templates/base.html               core's frame + the BarSides stylesheet, dark default, READY. footer, chart colours
  templates/components/navbar.html  core's top bar with the BarSides CTF badge
  static/barsides/barsides.css      the design tokens and every style change
  static/barsides/fonts/            C64 Pro, C64 Pro Mono (see below), IBM Plex Sans (SIL OFL)
  static/barsides/img/              BarSides CTF badge and favicon
index.html                          the home page content, for CTFd's "index" page
screenshots/                        how it looks with this year's challenges loaded
```

Challenge cards get a coloured stripe from their `beginner`, `intermediate` or `advanced` tag (green, gold, red), and turn green with a SOLVED mark once solved.

## Install

```sh
scripts/install-theme.sh                        # copies the theme next to CTFd and checks it's mounted
scripts/install-theme.sh --activate             # also switches CTFd to it
scripts/install-theme.sh --activate --index     # and replaces the home page with index.html
```

The script defaults to `~/Claude/ctfd` (pass another folder as an argument). CTFd runs in Docker, so the first time it asks you to add one line to the ctfd service's `volumes:` in that folder's `docker-compose.yml` and recreate the container:

```yaml
      - ./themes/barsides:/opt/CTFd/CTFd/themes/barsides:ro
```

```sh
docker compose -f ~/Claude/ctfd/docker-compose.yml up -d ctfd
```

`--activate` and `--index` talk to the CTFd API with ctfcli's `.ctf/config`, so run `ctf init` first. `--index` saves the current home page to `themes/index-backup-<time>.html` before replacing it, and fills `EVENT_HOST` in the links with `$EVENT_HOST` (default `10.42.0.1`). You can also switch themes by hand under Admin Panel → Config → Theme.

To undo, pick `core` under Admin Panel → Config → Theme.

## Font license

C64 Pro and C64 Pro Mono are © Style (https://style64.org/c64-truetype/license). They are copied unchanged from the private BarSides/website repo. The license allows embedding them with `@font-face`, which is all this theme does, but not offering the files for download. **Before this repository is made public, delete `barsides/static/barsides/fonts/C64_*.woff2`** (the theme then falls back to a monospace font) or keep them out of the public copy.

IBM Plex Sans is under the SIL Open Font License; its license is in `fonts/IBM-Plex-OFL.txt`.
