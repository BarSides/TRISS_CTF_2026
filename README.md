# TRISS_CTF_2026
Collection of challenges from the 2026 TRISS CTF presented by BarSides.

Event: Three Rivers Information Security Symposium, October 22, 2026. Jeopardy style on CTFd, aimed at new CTF players.

## Keep this repository private until after the event

Flags live in plaintext in each challenge's README and `challenge.yml`. Past years' repos are public, so any reused idea needs a new flag.

## Layout

Each category has a Beginner, Intermediate and Advanced slot:

```
<Category>/<Tier>/
  README.md            Name, Author, Overview, Setup, Flag (same format as 2024/2025)
  challenge.yml        ctfcli spec, used to import the challenge into CTFd
  files/               anything players download (optional)
  Dockerfile           hosted challenges only
  docker-compose.yml   hosted challenges only
  Walkthrough.md       solution notes (optional, never attached)
```

| Category | Beginner | Intermediate | Advanced |
|---|---|---|---|
| AI | Off the Rails | Phish Sandwich | Inky Pro Max |
| Cryptography | Steel City Shift | Bridge Keeper's Revenge | The Bridge Keeper's Last Note |
| Forensics | Rigged Race | Forgot to Clear History | TBD |
| ICS | Pump Station Gossip | Open the Flood Gate | Crack the Vault |
| Misc | TBD | TBD | TBD |
| Rev | TBD | TBD | TBD |
| Steganography | Ghost Sign | Nesting Dolls | Scatter Shot |
| Web | Staff Only | 446 Bridges | Link Preview |

Every slot starts as a placeholder with `state: hidden` and the flag `BarSides{CHANGE_ME}`. A challenge is ready when its README and `challenge.yml` are filled in, the flag is real, and `state` is `visible`.

Update the table above in the same PR that adds or renames a challenge.

Players need Python 3 (standard library only) for Cryptography Advanced, Steganography Advanced, and the ICS challenges (a small Modbus client is attached to each; mbpoll or pymodbus also work). Forensics Beginner needs Wireshark (or tshark), and Forensics Intermediate needs a SQLite reader (DB Browser for SQLite, `sqlite3`, or Python's built-in module); both ship with Kali, but tell players to install them before arriving. Everything else is solvable with the local CyberChef or common tools.

To add a category, copy `_template/` into `<Category>/<Tier>/` for each tier.

## No Internet at TRISS

The venue has no Internet. Every challenge must be either a downloadable file served by CTFd or a self-contained Docker instance on the local network. That means:

- No external APIs, hosted AI models, CDNs, web fonts, Discord or other online flags.
- Vendor CSS and JavaScript into the challenge's `static/` folder instead of linking to a CDN.
- Ship any wordlist a challenge expects as a download (for example a trimmed rockyou).
- Docker images are built and saved before going on site; nothing is pulled or installed at the venue.

`scripts/check-offline.sh` flags outbound URLs in challenge code and templates.

## Before the event (with Internet)

```sh
python3 scripts/validate.py          # check every challenge.yml and README
scripts/check-offline.sh             # look for CDN links and outbound URLs
scripts/build-images.sh              # build every hosted challenge and save images to offline/images/
scripts/fetch-tools.sh               # download CyberChef for the local tools server
```

Copy the whole repository, including `offline/`, onto the event server or a USB drive.

## At the event (no Internet)

```sh
scripts/load-images.sh               # docker load everything in offline/images/
scripts/up.sh                        # docker compose up -d for every hosted challenge
docker compose -f infra/cyberchef/docker-compose.yml up -d   # local CyberChef on port 8000
```

## Importing into CTFd

Challenges are described in ctfcli format, so they don't need to be entered by hand.

```sh
pip install ctfcli
ctf init                             # once, points ctfcli at the CTFd instance and token
scripts/install-ctfd.sh              # ctf challenge install for every challenge.yml
scripts/install-ctfd.sh sync         # push later edits to challenges already in CTFd
```

Hosted challenges set `connection_info` in `challenge.yml` to the address players use on the event network. Update it once the event server's IP or hostname is known.
