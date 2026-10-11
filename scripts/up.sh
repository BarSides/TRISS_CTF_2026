#!/usr/bin/env bash
# Start every hosted challenge from local images only. Pass "down" to stop them.
set -euo pipefail
cd "$(dirname "$0")/.."
. scripts/lib.sh
action=${1:-up}
find . -name docker-compose.yml -not -path './_template/*' -not -path './offline/*' | sort | while read -r f; do
  dir=$(dirname "$f")
  project=$(project_name "$dir")
  echo "==> $dir"
  if [ "$action" = down ]; then
    docker compose -p "$project" -f "$f" down
  else
    docker compose -p "$project" -f "$f" up -d --no-build --pull never
  fi
done
