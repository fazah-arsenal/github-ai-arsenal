#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAZAH AI Arsenal — Automatic Global Version Synchronizer (`scripts/bump_version.py`)
Updates VERSION and synchronizes every version string across README, SKILL, SVGs,
pyproject.toml, glama.json, smithery.yaml, docs, and scripts in 1 command.

Usage:
  python scripts/bump_version.py 6.5.0
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TARGET_FILES = [
    "README.md",
    "SKILL.md",
    "pyproject.toml",
    "glama.json",
    "smithery.yaml",
    "examples/quickstart.md",
    "docs/index.html",
    "docs/LAUNCH_KIT.md",
    "assets/hero-banner.svg",
    "assets/architecture.svg",
    "assets/cli-preview.svg",
    "scripts/gh_arsenal.py",
    "scripts/mcp_server.py",
    "scripts/web_ui.py",
]


def bump_all(new_ver: str) -> int:
    ver_full = new_ver.lstrip("v").strip()
    parts = ver_full.split(".")
    ver_short = f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else ver_full
    if len(parts) == 2:
        ver_full = f"{ver_short}.0"

    (ROOT / "VERSION").write_text(ver_full + "\n", encoding="utf-8")
    changed = 0

    for rel in TARGET_FILES:
        p = ROOT / rel
        if not p.exists():
            continue
        orig = p.read_text(encoding="utf-8")
        text = orig
        # Update vX.Y or vX.Y.Z tags referring to Arsenal version
        text = re.sub(r"\bv[2-9]\.\d+(?:\.\d+)?\b", f"v{ver_short}", text)
        # Update JSON/TOML/Python version fields
        text = re.sub(r'("version"\s*:\s*")[0-9]+\.[0-9]+\.[0-9]+(")', rf"\g<1>{ver_full}\2", text)
        text = re.sub(r'(version\s*=\s*")[0-9]+\.[0-9]+\.[0-9]+(")', rf"\g<1>{ver_full}\2", text)
        text = re.sub(r'(version:\s*")[0-9]+\.[0-9]+\.[0-9]+(")', rf"\g<1>{ver_full}\2", text)
        if text != orig:
            p.write_text(text, encoding="utf-8")
            changed += 1
            print(f"  [SYNCED] {rel} -> v{ver_short} ({ver_full})")

    print(f"\nSynchronized {changed} file(s) to version v{ver_short} ({ver_full}).")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/bump_version.py <version>  (e.g., 6.5.0)")
        raise SystemExit(1)
    raise SystemExit(bump_all(sys.argv[1]))
