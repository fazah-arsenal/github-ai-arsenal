#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub AI Arsenal — 10,000+ Real GitHub Tools Mega Index Builder
================================================================
Harvests real, human-curated GitHub repositories (`owner/repo` + description + domain)
from 30+ legendary open-source Awesome Lists via raw.githubusercontent.com
(zero API rate limits, zero fake entries) and compiles them into a fast, compact
`references/mega_index.json.gz` searchable offline in milliseconds.
"""

from __future__ import annotations

import concurrent.futures
import datetime
import gzip
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
REFS_DIR = ROOT / "references"
CORE_CATALOG = REFS_DIR / "catalog.json"
MEGA_INDEX_GZ = REFS_DIR / "mega_index.json.gz"
USER_AGENT = "GitHub-AI-Arsenal-Harvester/2.0"

# 35+ Real, Legendary GitHub Awesome Lists covering AI, MCP, Security, Python, JS, Go, Rust, DevOps, Self-Hosted, Bots, Media, UI, Data
AWESOME_SOURCES: List[Tuple[str, str, str]] = [
    # (category, owner/repo, branch/path)
    ("mcp-servers", "punkpeye/awesome-mcp-servers", "main/README.md"),
    ("mcp-servers", "appcypher/awesome-mcp-servers", "main/README.md"),
    ("ai-agents", "e2b-dev/awesome-ai-agents", "main/README.md"),
    ("ai-agents", "kyrolabs/awesome-agents", "main/README.md"),
    ("ai-agents", "Shubhamsaboo/awesome-llm-apps", "main/README.md"),
    ("ai-llm", "hannibal046/Awesome-LLM", "main/README.md"),
    ("ai-llm", "steven2358/awesome-generative-ai", "master/README.md"),
    ("ai-llm", "mahseema/awesome-ai-tools", "main/README.md"),
    ("ai-llm", "underlines/awesome-marketing", "master/README.md"),
    ("machine-learning", "josephmisiti/awesome-machine-learning", "master/README.md"),
    ("python", "vinta/awesome-python", "master/README.md"),
    ("python", "trananhkma/generally-useful-python", "master/README.md"),
    ("javascript-web", "sorrycc/awesome-javascript", "master/README.md"),
    ("javascript-web", "sindresorhus/awesome-nodejs", "main/README.md"),
    ("ui-frontend", "enaqx/awesome-react", "master/README.md"),
    ("ui-frontend", "vuejs/awesome-vue", "master/README.md"),
    ("ui-frontend", "aniftyco/awesome-tailwindcss", "master/README.md"),
    ("go-systems", "avelino/awesome-go", "main/README.md"),
    ("rust-systems", "rust-unofficial/awesome-rust", "main/README.md"),
    ("cpp-systems", "fffaraz/awesome-cpp", "master/README.md"),
    ("security-pentest", "sbilly/awesome-security", "master/README.md"),
    ("security-pentest", "Hack-with-Github/Awesome-Hacking", "master/README.md"),
    ("security-pentest", "enaqx/awesome-pentest", "master/README.md"),
    ("security-pentest", "qazbnm456/awesome-web-security", "master/README.md"),
    ("osint-recon", "jivoi/awesome-osint", "master/README.md"),
    ("reverse-engineering", "alphaSeclab/awesome-reverse-engineering", "master/README.md"),
    ("reverse-engineering", "fdivrp/awesome-reversing", "master/README.md"),
    ("scraping-data", "lorien/awesome-web-scraping", "master/README.md"),
    ("devops-cloud", "awesome-selfhosted/awesome-selfhosted", "master/README.md"),
    ("devops-cloud", "veggiemonk/awesome-docker", "master/README.md"),
    ("devops-cloud", "ramitsurana/awesome-kubernetes", "master/README.md"),
    ("devops-cloud", "dastergon/awesome-sre", "main/README.md"),
    ("cli-productivity", "agarrharr/awesome-cli-apps", "main/README.md"),
    ("cli-productivity", "alebcay/awesome-shell", "master/README.md"),
    ("databases-rag", "numetriclabz/awesome-db", "master/README.md"),
    ("mobile-desktop", "Solido/awesome-flutter", "master/README.md"),
    ("mobile-desktop", "JStumpp/awesome-android", "master/README.md"),
    ("mobile-desktop", "tauri-apps/awesome-tauri", "dev/README.md"),
    ("media-audio-video", "krzemienski/awesome-video", "master/README.md"),
    ("bots-automation", "botpress/awesome-bots", "master/README.md"),
    ("apis-backend", "public-apis/public-apis", "master/README.md"),
    ("devops-cloud", "trimstray/the-book-of-secret-knowledge", "master/README.md"),
    ("developer-tools", "ripienaar/free-for-dev", "master/README.md"),
    ("blockchain-web3", "bkrem/awesome-solidity", "master/README.md"),
    ("blockchain-web3", "OffcierCia/DeFi-Developer-Road-Map", "main/README.md"),
    ("java-jvm", "akullpp/awesome-java", "master/README.md"),
    ("dotnet-csharp", "quozd/awesome-dotnet", "master/README.md"),
    ("php-web", "ziadoz/awesome-php", "master/README.md"),
    ("game-dev", "ellisonleao/magictools", "main/README.md"),
    ("mobile-desktop", "ashishb/android-security-awesome", "master/README.md"),
    ("machine-learning", "ChristosChristofidis/awesome-deep-learning", "master/README.md"),
    ("security-pentest", "yeyintminthuhtut/Awesome-Red-Teaming", "master/README.md"),
    ("databases-rag", "dhamaniasad/awesome-postgres", "master/README.md"),
]

# Match markdown links to GitHub repos: [Name](https://github.com/owner/repo) followed by optional description
REPO_LINE_RE = re.compile(
    r"\[([^\]]{1,90})\]\(https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?:/[^\)\s]*)?\)\s*(?:[-–—:|]+\s*(.*))?",
    re.IGNORECASE,
)

SKIP_OWNERS = {"sponsors", "features", "topics", "collections", "marketplace", "orgs", "users", "about", "pricing", "login"}


def _clean_desc(text: str) -> str:
    if not text:
        return ""
    # Strip markdown images/badges/links
    text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", text)
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"\s+", " ", text).strip(" -–—:|•.")
    return text[:220]


def fetch_source(item: Tuple[str, str, str]) -> List[Dict[str, str]]:
    category, source_repo, branch_path = item
    url = f"https://raw.githubusercontent.com/{source_repo}/{branch_path}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=18) as resp:
            if resp.status != 200:
                return []
            body = resp.read().decode("utf-8", errors="ignore")
    except Exception:
        # Try alternate branch main <-> master
        alt = branch_path.replace("master/", "main/") if branch_path.startswith("master/") else branch_path.replace("main/", "master/")
        try:
            req2 = urllib.request.Request(f"https://raw.githubusercontent.com/{source_repo}/{alt}", headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req2, timeout=15) as resp2:
                body = resp2.read().decode("utf-8", errors="ignore")
        except Exception:
            return []

    found: List[Dict[str, str]] = []
    subcat = ""
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line.startswith("#"):
            h = re.sub(r"^#+\s*", "", line)
            h = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", h)
            h = re.sub(r"[^A-Za-z0-9 &/+_-]", "", h).strip()
            if 2 <= len(h) <= 45:
                subcat = h
            continue

        m = REPO_LINE_RE.search(line)
        if not m:
            continue
        name = _clean_desc(m.group(1))
        slug = m.group(2).rstrip("/")
        if slug.endswith(".git"):
            slug = slug[:-4]
        owner, repo = slug.split("/", 1)
        if owner.lower() in SKIP_OWNERS or len(repo) < 2 or repo.lower() in ("issues", "pulls", "wiki", "releases"):
            continue
        desc = _clean_desc(m.group(3) or "")
        if not desc:
            desc = f"{name} ({subcat or category})"
        found.append({
            "n": name or repo,
            "r": slug,
            "c": category,
            "s": subcat[:32] if subcat else "",
            "d": desc,
        })
    return found


def build_index() -> Dict[str, object]:
    REFS_DIR.mkdir(parents=True, exist_ok=True)
    dedup: Dict[str, Dict[str, str]] = {}

    # 1. Seed with hand-curated core catalog first (highest priority)
    if CORE_CATALOG.exists():
        core = json.loads(CORE_CATALOG.read_text(encoding="utf-8"))
        for t in core.get("tools", []):
            slug = t["repo"].strip()
            dedup[slug.lower()] = {
                "n": t["name"],
                "r": slug,
                "c": t["category"],
                "s": "core-elite",
                "d": t["use_when"][:220],
            }

    # 2. Parallel harvest from 40+ curated Awesome Lists
    print(f"Harvesting from {len(AWESOME_SOURCES)} curated GitHub Awesome Lists...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        futures = {pool.submit(fetch_source, src): src for src in AWESOME_SOURCES}
        for fut in concurrent.futures.as_completed(futures):
            src = futures[fut]
            try:
                rows = fut.result()
                added = 0
                for row in rows:
                    key = row["r"].lower()
                    if key not in dedup:
                        dedup[key] = row
                        added += 1
                print(f"  + {src[1]:44s} -> +{added:4d} unique (total: {len(dedup)})")
            except Exception as exc:
                print(f"  ! {src[1]} failed: {exc}")

    items = list(dedup.values())
    cat_counts: Dict[str, int] = {}
    for it in items:
        cat_counts[it["c"]] = cat_counts.get(it["c"], 0) + 1

    payload = {
        "version": "2.0.0",
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_tools": len(items),
        "categories": dict(sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)),
        "tools": items,
    }

    raw_bytes = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    with gzip.open(MEGA_INDEX_GZ, "wb", compresslevel=9) as gz:
        gz.write(raw_bytes)

    size_kb = MEGA_INDEX_GZ.stat().st_size / 1024
    print(f"\nDONE! Saved {len(items):,} unique real GitHub tools to {MEGA_INDEX_GZ} ({size_kb:.1f} KB compressed).")
    return payload


if __name__ == "__main__":
    build_index()
