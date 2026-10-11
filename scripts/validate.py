#!/usr/bin/env python3
"""Check every challenge folder before importing into CTFd.

A tier can hold up to three challenges: <Tier> is the first, "<Tier> 1" the second and
"<Tier> 2" the third (for example Beginner, Beginner 1, Beginner 2).

Errors fail the run. Placeholders (hidden challenges still using BarSides{CHANGE_ME})
are reported but allowed, so the repo stays green while slots are being filled.
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
TIERS = ["Beginner", "Intermediate", "Advanced"]
SLOT_RE = re.compile(rf"^({'|'.join(TIERS)})(?: ([12]))?$")
REQUIRED = ["name", "author", "category", "description", "value", "type", "flags", "state"]
SECTIONS = ["# Name", "## Author", "## Overview", "## Setup", "## Flag"]
FLAG_RE = re.compile(r"^BarSides\{[^{}\s]+\}$")
PLACEHOLDER = "BarSides{CHANGE_ME}"


def flag_values(flags):
    for f in flags or []:
        yield f["content"] if isinstance(f, dict) else str(f)


def check(chal_dir, errors, placeholders, seen_flags, seen_names):
    rel = chal_dir.relative_to(ROOT)
    category, tier = rel.parts[0], rel.parts[1]
    err = lambda msg: errors.append(f"{rel}: {msg}")

    slot = SLOT_RE.match(tier)
    if not slot:
        err(f"tier folder must be one of {TIERS}, optionally followed by ' 1' or ' 2'")
    elif slot.group(2):
        prev = slot.group(1) if slot.group(2) == "1" else f"{slot.group(1)} 1"
        if not (ROOT / category / prev / "challenge.yml").is_file():
            err(f"'{tier}' needs '{prev}' to exist first")

    spec = yaml.safe_load((chal_dir / "challenge.yml").read_text())
    if not isinstance(spec, dict):
        return err("challenge.yml is empty or not a mapping")
    for key in REQUIRED:
        if key not in spec:
            err(f"challenge.yml missing '{key}'")
    if spec.get("category") != category:
        err(f"category '{spec.get('category')}' does not match folder '{category}'")
    if spec.get("state") not in ("hidden", "visible"):
        err("state must be hidden or visible")

    name = spec.get("name")
    if name in seen_names:
        err(f"duplicate challenge name '{name}' (also {seen_names[name]})")
    seen_names[name] = rel

    flags = list(flag_values(spec.get("flags")))
    if not flags:
        err("no flags")
    is_placeholder = PLACEHOLDER in flags
    if is_placeholder:
        if spec.get("state") == "visible":
            err("visible challenge still has the placeholder flag")
        placeholders.append(str(rel))
    for flag in flags:
        if flag == PLACEHOLDER:
            continue
        if not FLAG_RE.match(flag):
            err(f"flag '{flag}' is not in BarSides{{...}} format")
        if flag in seen_flags:
            err(f"flag reused from {seen_flags[flag]}")
        seen_flags[flag] = rel

    for f in spec.get("files") or []:
        if not (chal_dir / f).is_file():
            err(f"listed file '{f}' does not exist")

    readme = chal_dir / "README.md"
    if not readme.is_file():
        err("missing README.md")
    else:
        text = readme.read_text()
        for s in SECTIONS:
            if not re.search(rf"^{re.escape(s)}\s*$", text, re.M):
                err(f"README.md missing '{s}' section")
        if not is_placeholder:
            for flag in flags:
                if flag not in text:
                    err(f"README.md Flag section does not match challenge.yml flag '{flag}'")

    compose = chal_dir / "docker-compose.yml"
    if compose.is_file():
        if "connection_info" not in spec and not is_placeholder:
            err("hosted challenge has docker-compose.yml but no connection_info")
        prefix = f"triss2026/{slug(rel)}"
        for image in compose_images(compose):
            if image != prefix and not image.startswith(prefix + "-"):
                err(f"image '{image}' should be tagged {prefix} (or {prefix}-<part>)")


def slug(rel):
    """AI/Beginner 1 -> ai-beginner-1, the name used for image tags and compose projects."""
    return re.sub(r"[^a-z0-9]+", "-", str(rel).lower()).strip("-")


def compose_services(path):
    spec = yaml.safe_load(path.read_text()) or {}
    return (spec.get("services") or {}).values()


def compose_images(path):
    return [s["image"] for s in compose_services(path) if s.get("image")]


def host_ports(path):
    for s in compose_services(path):
        for p in s.get("ports") or []:
            if isinstance(p, dict):
                yield str(p.get("published"))
            else:
                parts = str(p).split(":")
                if len(parts) > 1:
                    yield parts[-2]


def check_compose_conflicts(errors):
    """Every hosted challenge runs at once on the event laptop, so images and ports must be unique."""
    seen_images, seen_ports = {}, {}
    files = sorted(ROOT.glob("*/*/docker-compose.yml"))
    for f in files:
        if f.parts[-3].startswith(("_", ".")):
            continue
        rel = f.parent.relative_to(ROOT)
        for image in compose_images(f):
            if image in seen_images and seen_images[image] != rel:
                errors.append(f"{rel}: image '{image}' already used by {seen_images[image]}")
            seen_images.setdefault(image, rel)
        for port in host_ports(f):
            if port in seen_ports and seen_ports[port] != rel:
                errors.append(f"{rel}: host port {port} already used by {seen_ports[port]}")
            seen_ports.setdefault(port, rel)


def main():
    errors, placeholders = [], []
    seen_flags, seen_names = {}, {}
    dirs = sorted(
        p.parent for p in ROOT.glob("*/*/challenge.yml")
        if not p.parts[-3].startswith(("_", "."))
    )
    for d in dirs:
        check(d, errors, placeholders, seen_flags, seen_names)
    check_compose_conflicts(errors)

    ready = len(dirs) - len(placeholders)
    print(f"{len(dirs)} challenge slots, {ready} ready, {len(placeholders)} placeholders")
    for p in placeholders:
        print(f"  placeholder: {p}")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
