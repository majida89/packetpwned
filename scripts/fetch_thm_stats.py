#!/usr/bin/env python3
"""
fetch_thm_stats.py
Fetches TryHackMe public profile stats and writes them to data/thm.json
for Hugo to consume at build time.

Usage:
    python3 scripts/fetch_thm_stats.py

Runs automatically via GitHub Actions every Monday at 06:00 UTC.
"""

import requests
import json
import sys
import os
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
THM_USERNAME  = "majida89"
OUTPUT_PATH   = "data/thm.json"          # relative to repo root
TIMEOUT       = 15                        # seconds

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

# ── Fetch ─────────────────────────────────────────────────────────────────────
def fetch_stats(username: str) -> dict:
    """Pull stats from the THM public API endpoints."""

    stats = {}

    # Primary endpoint — rank, badges, rooms, points
    url_rank = f"https://tryhackme.com/api/user/rank/{username}"
    r = requests.get(url_rank, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    rank_data = r.json()

    stats["rank"]           = rank_data.get("userRank", 0)
    stats["points"]         = rank_data.get("userPoints", 0)
    stats["badges"]         = rank_data.get("totalBadges", 0)
    stats["rooms_complete"] = rank_data.get("completedRooms", 0)

    # Secondary endpoint — streak & top % label
    url_profile = f"https://tryhackme.com/api/v2/public-profile/?username={username}"
    rp = requests.get(url_profile, headers=HEADERS, timeout=TIMEOUT)
    rp.raise_for_status()
    profile_data = rp.json()

    data = profile_data.get("data", profile_data)   # handle nested or flat
    stats["streak"]    = data.get("streak", {}).get("currentStreak", 0)
    stats["top_pct"]   = data.get("userRankBadge", "top 5%")   # e.g. "top 5%"
    stats["level"]     = data.get("level", "")

    return stats


# ── Write ─────────────────────────────────────────────────────────────────────
def write_json(stats: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    payload = {
        **stats,
        "username":   THM_USERNAME,
        "profile_url": f"https://tryhackme.com/p/{THM_USERNAME}",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"[ok] Written to {path}")
    print(json.dumps(payload, indent=2))


# ── Fallback ──────────────────────────────────────────────────────────────────
def load_existing(path: str) -> dict:
    """Return existing data if the file exists, otherwise empty dict."""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"[*] Fetching TryHackMe stats for: {THM_USERNAME}")

    try:
        stats = fetch_stats(THM_USERNAME)
        write_json(stats, OUTPUT_PATH)

    except requests.HTTPError as e:
        print(f"[!] HTTP error: {e}", file=sys.stderr)
        # If we already have data, keep it rather than failing the build
        existing = load_existing(OUTPUT_PATH)
        if existing:
            print("[!] Keeping existing data — THM API may be rate-limiting.")
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"[!] Unexpected error: {e}", file=sys.stderr)
        existing = load_existing(OUTPUT_PATH)
        if existing:
            print("[!] Keeping existing data.")
            sys.exit(0)
        else:
            sys.exit(1)
