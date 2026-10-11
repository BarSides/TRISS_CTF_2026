# Name

446 Bridges

## Author

@justinforbes

## Overview

Pittsburgh has 446 bridges, and somebody built a website to search them. The bridge crew keeps its private notes in the same database, including the gate code for a maintenance catwalk. The search box only shows bridges... or does it?

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

The site listens on port 8005 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `http://EVENT_HOST:8005`.

The bridge search builds `SELECT name, river, year_opened FROM bridges WHERE name LIKE '%<q>%'` by string formatting and shows SQLite error messages, so players can UNION SELECT from `sqlite_master` to find the hidden `maintenance_crew_notes` table and read the flag from it. Players can't break it for each other: the SQLite database is rebuilt in memory at start, every search runs read only (`PRAGMA query_only`), only one statement is allowed per search, results are capped at 100 rows, and queries over one second are cut off. `app.py` is Python standard library on Alpine with local CSS, so it runs fully offline. The flag can be changed with the `FLAG` environment variable. Solution notes are in `Walkthrough.md`.

## Flag

BarSides{union_select_the_city_of_bridges}
