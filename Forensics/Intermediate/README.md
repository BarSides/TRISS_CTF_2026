# Name

Forgot to Clear History

## Author

@justinforbes

## Overview

Dana, an engineer at Steel City Signal Co., resigned on Tuesday and started at a competitor the following week. The next day, our confidential bid numbers turned up in the competitor's proposal.

Dana's work laptop was wiped before IT could image it, but a backup of the Firefox profile survived. Work out how the secret left the building and recover what was sent.

## Setup

Attach `files/dkowalski_firefox_profile.zip` as a CTFd download. No hosted service is needed. Players need a way to read SQLite files: DB Browser for SQLite, the `sqlite3` command line tool, or Python's built-in `sqlite3` module. The local CyberChef reverses the encoding.

Solve path: `formhistory.sqlite` holds the text typed into a paste site's `paste_body` field (Base64). `places.sqlite` history shows Dana built a CyberChef recipe of XOR with the key `yinz` followed by To Base64, just before making the paste. Reversing it (From Base64, then XOR `yinz`) gives the flag. The flag never appears in plaintext in the profile.

`build/make_profile.py` regenerates the zip byte for byte from `build/browsing.tsv` (standard library only). It is for organizers only; do not attach it. The URLs in `browsing.tsv` are fake history entries and are never fetched.

## Flag

BarSides{the_recipe_was_in_the_url}
