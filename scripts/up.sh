#!/usr/bin/env bash
# Start every hosted challenge from local images only. Pass "down" to stop them.
set -euo pipefail
cd "$(dirname "$0")/.."
action=${1:-up}
find . -name docker-compose.yml -not -path './_template/*' -not -path './offline/*' | sort | while read -r f; do
  echo "==> $(dirname "$f")"
  if [ "$action" = down ]; then
    docker compose -f "$f" down
  else
    docker compose -f "$f" up -d --no-build --pull never
  fi
done
