# Name

Link Preview

## Author

@justinforbes

## Overview

PghChat shows a little preview whenever you paste a link, fetching the page for you on its server. Somewhere behind that server is an admin console that is supposed to be reachable only from inside. PghChat refuses to preview the obvious internal addresses... but it isn't very thorough about it.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

The site listens on port 8006 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `http://EVENT_HOST:8006`.

This is a server side request forgery (SSRF) challenge. `/preview` fetches the URL the player submits and shows the result, so the player can target an internal-only admin page that holds the flag. A blocklist rejects the exact hostnames `localhost` and `127.0.0.1`, but the same address written another way (`127.1`, the decimal `2130706433`, `[::1]`, a trailing-dot `127.0.0.1.`, or the internal name `admin.pghchat.internal`) gets through.

Safety: there is **no real network**. The "internet" PghChat can see is a fixed dictionary inside `app.py` (`MOCK_NET`); the fetcher only reads from it and never opens a socket, so players cannot use it to reach anything else on the venue network. `app.py` is Python standard library on Alpine with local CSS, so it runs fully offline. The flag can be changed with the `FLAG` environment variable. Solution notes are in `Walkthrough.md`.

## Flag

BarSides{server_side_requests_cross_the_bridge}
