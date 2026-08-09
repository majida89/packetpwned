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
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://tryhackme.com/",
}

# ── Fetch ─────────────────────────────────────────────────────────────────────
def fetch_stats(username: str) -> dict:
    """Pull stats from the THM v2 public profile endpoint."""

    url = f"https://tryhackme.com/api/v2/public-profile/?username={username}"
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json().get("data", {})

    top_pct = data.get("topPercentage", 5)

    return {
        "rank":           data.get("rank", 0),
        "points":         data.get("totalPoints", 0),
        "badges":         data.get("badgesNumber", 0),
        "rooms_complete": data.get("completedRoomsNumber", 0),
        "streak":         data.get("streak", 0),
        "top_pct":        f"top {top_pct}%",
        "level":          data.get("level", ""),
    }


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

    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        print("[!] Keeping existing data — build will continue.")
        sys.exit(0)
