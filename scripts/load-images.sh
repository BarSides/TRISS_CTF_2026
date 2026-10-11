#!/usr/bin/env bash
# Run AT the event. Loads every image saved by build-images.sh; no Internet needed.
set -euo pipefail
cd "$(dirname "$0")/.."
shopt -s nullglob
for t in offline/images/*.tar; do
  echo "==> loading $t"
  docker load -i "$t"
done
