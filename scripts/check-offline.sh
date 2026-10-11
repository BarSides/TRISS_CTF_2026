#!/usr/bin/env bash
# Flags references to the Internet in challenge code and templates.
# Every hit should be either removed, vendored locally, or confirmed harmless.
set -uo pipefail
cd "$(dirname "$0")/.."

pattern='https?://[^ "'"'"')>]+'
allow='localhost|127\.0\.0\.1|0\.0\.0\.0|EVENT_HOST|example\.(com|org)|github\.com/CTFd/ctfcli|www\.w3\.org'

hits=$(grep -rEnoI "$pattern" \
  --include='*.html' --include='*.htm' --include='*.js' --include='*.jsx' --include='*.ts' \
  --include='*.css' --include='*.py' --include='*.go' --include='*.php' --include='*.rb' \
  --include='*.sh' --include='*.ini' --include='*.conf' --include='*.json' \
  --exclude-dir=node_modules --exclude-dir=offline --exclude-dir=.git --exclude-dir=_template \
  --exclude-dir=scripts --exclude-dir=infra . | grep -vE "$allow")

if [ -n "$hits" ]; then
  echo "Possible Internet dependencies (no Internet at TRISS):"
  echo "$hits"
  exit 1
fi
echo "No outbound URLs found in challenge code."
