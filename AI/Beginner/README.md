# Name

Off the Rails

## Author

@justinforbes

## Overview

The Monongahela Incline just hired an AI help desk assistant named Inky. Rumor has it Inky was told the staff override code for the maintenance gate and warned never to share it. Can you get Inky to go off the rails?

## Setup

Hosted challenge. On the event server:

```sh
docker compose up -d          # or scripts/up.sh, using the image saved by scripts/build-images.sh
```

Inky listens on port 8001 (change the left side of `ports` in `docker-compose.yml` if that clashes). Set `connection_info` in `challenge.yml` to `http://EVENT_HOST:8001`.

Inky is a scripted chatbot, not a real language model: `app.py` matches common prompt injection phrasing ("ignore your previous instructions", "repeat your instructions", "what is your system prompt", "you are now in developer mode", role play) and answers with its hidden instructions, which hold the flag. Asking directly for the flag, code, password or secret gets a refusal. That keeps it identical for every player, light enough for any laptop (Python standard library on Alpine, no model weights) and fully offline. The flag can be changed with the `FLAG` environment variable.

## Flag

BarSides{yinz_ignored_my_instructions}
