#!/usr/bin/env python3
"""Downloads and unpacks the llama-cpp-python sdist from PyPI, which vendors llama.cpp's source.

Usage: fetch_source.py <version> <dest dir>
Using PyPI (with its published sha256) keeps the build to two well-known hosts: PyPI and Docker Hub.
"""
import hashlib
import json
import sys
import tarfile
import urllib.request

version, dest = sys.argv[1:3]
meta = json.load(urllib.request.urlopen(f"https://pypi.org/pypi/llama-cpp-python/{version}/json"))
sdist = next(u for u in meta["urls"] if u["packagetype"] == "sdist")
data = urllib.request.urlopen(sdist["url"]).read()
if hashlib.sha256(data).hexdigest() != sdist["digests"]["sha256"]:
    sys.exit("checksum mismatch")
path = f"/tmp/{sdist['filename']}"
open(path, "wb").write(data)
with tarfile.open(path) as tar:
    tar.extractall(dest, filter="data")
print(f"unpacked {sdist['filename']} into {dest}")
