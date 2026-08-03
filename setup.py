#!/usr/bin/env python3
"""
NFL Depth Charts — First-time setup script.
Downloads all 32 teams' depth charts and logos, then opens the viewer.
Run this once to get started. Run fetch.py any time you want fresh data.
"""
import os, platform, subprocess, sys


def check_python():
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 6):
        print(f"\n  ERROR: Python 3.6 or newer is required.")
        print(f"         You have Python {v.major}.{v.minor}.{v.micro}.")
        print(f"         Download the latest Python 3 from: https://www.python.org/downloads/\n")
        sys.exit(1)
    print(f"  Python {v.major}.{v.minor}.{v.micro} — OK")


def check_fetch_script():
    if not os.path.exists("fetch.py"):
        print("\n  ERROR: fetch.py not found.")
        print("         Make sure you're running this from inside the draft-assistant folder.\n")
        sys.exit(1)
    print("  fetch.py found — OK")


def run_fetch():
    print("\n" + "─" * 60)
    print("  Downloading NFL depth charts and logos from ESPN...")
    print("  This takes about 45 seconds. You'll see teams scroll by.")
    print("─" * 60 + "\n")
    result = subprocess.run([sys.executable, "fetch.py"])
    if result.returncode != 0:
        print("\n  ERROR: Data download failed.")
        print("         Check that you're connected to the internet and try again.")
        sys.exit(1)


def open_viewer():
    html = os.path.abspath("index.html")
    system = platform.system()
    print("\n" + "─" * 60)
    print("  Opening the depth chart viewer in your browser...")
    print("─" * 60)
    try:
        if system == "Darwin":
            subprocess.run(["open", html])
        elif system == "Windows":
            os.startfile(html)
        else:
            subprocess.run(["xdg-open", html])
    except Exception:
        print(f"\n  Could not open automatically. Open this file in your browser:")
        print(f"  {html}")


def main():
    print()
    print("  NFL DEPTH CHARTS — Setup")
    print("=" * 60)
    print()
    print("  Checking requirements...")
    check_python()
    check_fetch_script()

    run_fetch()
    open_viewer()

    print()
    print("=" * 60)
    print("  Setup complete!")
    print()
    print("  Next time: run  python3 launch.py")
    print("  It auto-refreshes data if it's from a previous day.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
