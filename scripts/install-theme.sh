#!/usr/bin/env bash
# Install the BarSides CTFd theme (infra/ctfd-theme/barsides) next to a docker compose CTFd.
# Usage: scripts/install-theme.sh [--activate] [--index] [CTFD_DIR]
#   CTFD_DIR    folder holding CTFd's docker-compose.yml (default: $CTFD_DIR or ~/Claude/ctfd)
#   --activate  switch CTFd to the theme through the API (uses ctfcli's .ctf/config)
#   --index     replace the CTFd home page with infra/ctfd-theme/index.html; the old one is saved first
# EVENT_HOST (default 10.42.0.1) is filled into the home page's links.
set -euo pipefail
cd "$(dirname "$0")/.."

activate=0
index=0
ctfd_dir=${CTFD_DIR:-$HOME/Claude/ctfd}
for arg in "$@"; do
  case $arg in
    --activate) activate=1 ;;
    --index) index=1 ;;
    -*) echo "unknown option: $arg" >&2; exit 2 ;;
    *) ctfd_dir=$arg ;;
  esac
done
event_host=${EVENT_HOST:-10.42.0.1}

[ -f "$ctfd_dir/docker-compose.yml" ] || { echo "No docker-compose.yml in $ctfd_dir" >&2; exit 1; }

echo "==> copy theme to $ctfd_dir/themes/barsides"
mkdir -p "$ctfd_dir/themes"
rm -rf "$ctfd_dir/themes/barsides.new"
cp -r infra/ctfd-theme/barsides "$ctfd_dir/themes/barsides.new"
rm -rf "$ctfd_dir/themes/barsides"
mv "$ctfd_dir/themes/barsides.new" "$ctfd_dir/themes/barsides"

mount='./themes/barsides:/opt/CTFd/CTFd/themes/barsides:ro'
if ! grep -qF "$mount" "$ctfd_dir/docker-compose.yml"; then
  cat <<EOF

CTFd can't see the theme yet. Add this line under the ctfd service's volumes in
$ctfd_dir/docker-compose.yml:

      - $mount

then recreate the container (the database and uploads are untouched):

  docker compose -f $ctfd_dir/docker-compose.yml up -d ctfd

and run this script again with --activate.
EOF
  [ $activate = 1 ] || [ $index = 1 ] && exit 1
  exit 0
fi
echo "    already mounted in docker-compose.yml (after changing templates: docker compose -f $ctfd_dir/docker-compose.yml restart ctfd)"

[ $activate = 1 ] || [ $index = 1 ] || exit 0

[ -f .ctf/config ] || { echo "No .ctf/config: run 'ctf init' first" >&2; exit 1; }
python3 - "$activate" "$index" "$event_host" "$ctfd_dir" <<'EOF'
import configparser, json, sys, time, urllib.request

activate, index, event_host, ctfd_dir = sys.argv[1] == "1", sys.argv[2] == "1", sys.argv[3], sys.argv[4]
cfg = configparser.ConfigParser()
cfg.read(".ctf/config")
url = cfg["config"]["url"].rstrip("/")
token = cfg["config"]["access_token"]

def api(method, path, body=None):
    req = urllib.request.Request(
        url + "/api/v1" + path, method=method,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Authorization": "Token " + token, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        out = json.load(r)
    if not out.get("success"):
        sys.exit(f"{method} {path} failed: {out}")
    return out.get("data")

if activate:
    api("PATCH", "/configs", {"ctf_theme": "barsides"})
    print("==> CTFd theme set to barsides")

if index:
    pages = [p for p in api("GET", "/pages") if p["route"] == "index"]
    content = open("infra/ctfd-theme/index.html").read().replace("EVENT_HOST", event_host)
    if pages:
        page = api("GET", f"/pages/{pages[0]['id']}")
        backup = f"{ctfd_dir}/themes/index-backup-{time.strftime('%Y%m%d-%H%M%S')}.html"
        with open(backup, "w") as f:
            f.write(page["content"] or "")
        print(f"==> old home page saved to {backup}")
        api("PATCH", f"/pages/{page['id']}", {"content": content, "format": "html"})
    else:
        api("POST", "/pages", {"title": "Home", "route": "index", "content": content, "format": "html", "draft": False, "hidden": False, "auth_required": False})
    print("==> home page replaced with infra/ctfd-theme/index.html")
EOF
