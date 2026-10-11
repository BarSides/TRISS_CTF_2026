#!/usr/bin/env bash
# Run BEFORE the event, with Internet. Downloads CyberChef so players have a local copy,
# served by infra/cyberchef/docker-compose.yml.
set -euo pipefail
cd "$(dirname "$0")/.."
CYBERCHEF_VERSION=${CYBERCHEF_VERSION:-v10.19.4}
dest=offline/tools/cyberchef
mkdir -p "$dest"
curl -fsSL -o /tmp/cyberchef.zip \
  "https://github.com/gchq/CyberChef/releases/download/${CYBERCHEF_VERSION}/CyberChef_${CYBERCHEF_VERSION}.zip"
unzip -oq /tmp/cyberchef.zip -d "$dest"
mv -f "$dest/CyberChef_${CYBERCHEF_VERSION}.html" "$dest/index.html"
rm /tmp/cyberchef.zip
docker pull nginx:1.27-alpine
mkdir -p offline/images
docker save -o offline/images/nginx_1.27-alpine.tar nginx:1.27-alpine
echo "CyberChef ${CYBERCHEF_VERSION} saved to $dest"
