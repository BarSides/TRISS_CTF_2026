#!/usr/bin/env bash
# Run BEFORE the event, with Internet. Builds every hosted challenge, pulls the images
# it depends on (databases etc.) and saves them all to offline/images/ for docker load on site.
set -euo pipefail
cd "$(dirname "$0")/.."
. scripts/lib.sh
mkdir -p offline/images

find . -name docker-compose.yml -not -path './_template/*' -not -path './offline/*' | sort | while read -r f; do
  dir=$(dirname "$f")
  project=$(project_name "$dir")
  echo "==> $dir"
  docker compose -p "$project" -f "$f" pull --ignore-buildable
  docker compose -p "$project" -f "$f" build --pull
  for img in $(docker compose -p "$project" -f "$f" config --images); do
    out="offline/images/$(echo "$img" | tr '/:' '__').tar"
    echo "    saving $img -> $out"
    docker save -o "$out" "$img"
  done
done

echo "Saved images:"
ls -lh offline/images
