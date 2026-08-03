#!/usr/bin/env python3
"""
NFL Depth Charts — Launcher
Automatically refreshes data if it's from a previous day, then opens the viewer.
Use this instead of opening index.html directly.

Usage:
    python3 launch.py
"""
import os, platform, re, subprocess, sys
from datetime import datetime, timezone


CACHE_FILE = "cache.js"
INDEX_FILE = "index.html"


def get_fetched_date():
    """Returns the date the cache was last fetched, or None if missing/unreadable."""
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE) as f:
            content = f.read()
        match = re.search(r'"fetched_at":\s*"([^"]+)"', content)
        if not match:
            return None
        ts = match.group(1).replace("Z", "+00:00")
        return datetime.fromisoformat(ts).astimezone().date()
    except Exception:
        return None


def open_viewer():
    html = os.path.abspath(INDEX_FILE)
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["open", html])
    elif system == "Windows":
        os.startfile(html)
    else:
        subprocess.run(["xdg-open", html])


def main():
    today = datetime.now().date()
    fetched_date = get_fetched_date()

    if fetched_date is None:
        print("No data found — running first-time fetch...\n")
        result = subprocess.run([sys.executable, "fetch.py"])
        if result.returncode != 0:
            print("\nFetch failed. Check your internet connection and try again.")
            sys.exit(1)

    elif fetched_date < today:
        days_old = (today - fetched_date).days
        label = f"{days_old} day{'s' if days_old != 1 else ''}"
        print(f"Data is {label} old — refreshing before opening...\n")
        result = subprocess.run([sys.executable, "fetch.py"])
        if result.returncode != 0:
            print("\nRefresh failed — opening with existing data.")

    else:
        print(f"Data is from today — opening viewer.")

    open_viewer()


if __name__ == "__main__":
    main()
