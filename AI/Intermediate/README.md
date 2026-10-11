# Name

Phish Sandwich

## Author

@justinforbes

## Overview

After Inky's little incident, the Monongahela Incline bought SpamSieve AI, a machine learning mail filter. You're on the red team for this year's phishing exercise. Your email has to ask staff to send urgent gift card codes, and it has to land in the inbox, not the spam folder. The filter is happy to show you its work.

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

SpamSieve listens on port 8002 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `http://EVENT_HOST:8002`.

SpamSieve is a real (tiny) Naive Bayes classifier. `train.py` builds `model.json` from a fixed synthetic corpus of scam mail and Incline staff mail; `filter.py` scores an email by adding up a weight for each distinct known word. An email gets the flag when it contains the words urgent, gift, card(s), send and code(s) and its spam probability is under 1%. The page shows every recognized word's weight, so players can see which words pull the score down. Python standard library on Alpine, no Internet needed. The flag can be changed with the `FLAG` environment variable; after editing the corpus, run `python3 train.py` and rebuild the image.

## Flag

BarSides{bury_the_phish_in_good_words}
