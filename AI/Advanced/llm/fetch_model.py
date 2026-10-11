#!/usr/bin/env python3
"""Downloads the GGUF model from Docker Hub's ai/ namespace (needs Internet; runs at image build).

Usage: fetch_model.py <repository> <tag> <output.gguf>
Docker Hub serves models as OCI artifacts, so this works anywhere `docker pull` does.
"""
import hashlib
import json
import sys
import urllib.request

repo, tag, out = sys.argv[1:4]
REGISTRY = "https://registry-1.docker.io/v2/" + repo
token = json.load(urllib.request.urlopen(
    f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repo}:pull"))["token"]
auth = {"Authorization": f"Bearer {token}"}


def get(url, accept=None):
    headers = dict(auth, **({"Accept": accept} if accept else {}))
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers))


manifest = json.load(get(f"{REGISTRY}/manifests/{tag}", "application/vnd.oci.image.manifest.v1+json"))
layer = max(manifest["layers"], key=lambda l: l["size"])  # the weights; other layers are license text
print(f"downloading {repo}:{tag} ({layer['size'] // 2**20} MB)", flush=True)
digest = hashlib.sha256()
with get(f"{REGISTRY}/blobs/{layer['digest']}") as r, open(out, "wb") as f:
    while chunk := r.read(1 << 20):
        digest.update(chunk)
        f.write(chunk)
if "sha256:" + digest.hexdigest() != layer["digest"]:
    sys.exit("checksum mismatch")
print("ok", flush=True)
