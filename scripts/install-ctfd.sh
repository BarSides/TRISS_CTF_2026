#!/usr/bin/env bash
# Import every challenge into CTFd with ctfcli. Run `ctf init` once first.
# Usage: scripts/install-ctfd.sh [install|sync]
set -euo pipefail
cd "$(dirname "$0")/.."
action=${1:-install}
find . -name challenge.yml -not -path './_template/*' | sort | while read -r f; do
  echo "==> $action $(dirname "$f")"
  ctf challenge "$action" "$(dirname "$f")"
done
