#!/usr/bin/env python3
"""
NFL Depth Chart Fetcher
Pulls all 32 teams from ESPN's public API, downloads team logos to logos/,
and writes cache.js for index.html.

Usage:
    python3 fetch.py

Requires: Python 3.6+ standard library only.
Logos are skipped on subsequent runs if already present — delete logos/ to force a refresh.
"""
import json, os, re, sys, time, urllib.request
from datetime import datetime, timezone

BASE_SITE = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
BASE_CORE = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"
SEASON = 2026
DELAY = 0.3

HEADERS = {"User-Agent": "nfl-depth-chart-viewer/1.0 (local reference tool)"}


def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def fetch_bytes(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def extract_athlete_id(ref_url):
    m = re.search(r"/athletes/(\d+)", ref_url)
    return m.group(1) if m else None


def build_roster_map(team_id):
    """Returns {athlete_id: {name, short, injury, status}} for all players on roster."""
    data = fetch_json(f"{BASE_SITE}/teams/{team_id}/roster")
    athlete_map = {}
    for grp in data.get("athletes", []):
        for player in grp.get("items", []):
            pid = str(player["id"])
            injuries = player.get("injuries", [])
            inj = injuries[0]["status"] if injuries else None
            status_name = player.get("status", {}).get("abbreviation", "")
            athlete_map[pid] = {
                "name": player["displayName"],
                "short": player.get("shortName", player["displayName"]),
                "injury": inj,
                "status": status_name,
            }
    return athlete_map


def resolve_athletes(positions_dict, pos_key, roster_map):
    """Extract and resolve athlete $ref URLs to names for a position slot."""
    pos = positions_dict.get(pos_key, {})
    result = []
    for entry in pos.get("athletes", []):
        ref = entry.get("athlete", {}).get("$ref", "")
        pid = extract_athlete_id(ref)
        if not pid:
            continue
        info = roster_map.get(
            pid,
            {"name": f"#{pid}", "short": f"#{pid}", "injury": None, "status": ""},
        )
        result.append({"id": pid, "slot": entry.get("slot"), "rank": entry.get("rank"), **info})
    return result


def parse_offense(dc_data, roster_map):
    """
    Parse '3WR 1TE' offense group and 'Special Teams' for kicker.

    WR slots: 1=X, 2=Z, 8=Slot — ranks interleave across slots (1,4,7... for X;
    2,5,8... for Z; 3,6,9... for Slot). Group by slot, sort by rank within each slot.
    """
    items = dc_data.get("items", [])
    offense = next((i for i in items if i.get("name") == "3WR 1TE"), None)
    special = next((i for i in items if i.get("name") == "Special Teams"), None)

    off_pos = offense.get("positions", {}) if offense else {}
    st_pos = special.get("positions", {}) if special else {}

    def sorted_pos(positions, key):
        athletes = resolve_athletes(positions, key, roster_map)
        athletes.sort(key=lambda x: x["rank"] or 999)
        return athletes

    wr_all = resolve_athletes(off_pos, "wr", roster_map)
    wr_slots = {}
    for a in wr_all:
        s = a["slot"]
        wr_slots.setdefault(s, []).append(a)
    for s in wr_slots:
        wr_slots[s].sort(key=lambda x: x["rank"] or 999)

    return {
        "qb":      sorted_pos(off_pos, "qb"),
        "rb":      sorted_pos(off_pos, "rb"),
        "wr_x":    wr_slots.get(1, []),   # slot 1 = X receiver
        "wr_z":    wr_slots.get(2, []),   # slot 2 = Z receiver
        "wr_slot": wr_slots.get(8, []),   # slot 8 = Slot receiver
        "te":      sorted_pos(off_pos, "te"),
        "k":       sorted_pos(st_pos, "pk"),  # kicker is 'pk' in Special Teams
    }


def download_logos(teams):
    """Download team logos to logos/ directory. Skips existing files."""
    os.makedirs("logos", exist_ok=True)
    print("Downloading logos…", end=" ", flush=True)
    downloaded = skipped = failed = 0
    for team in teams:
        abbrev = team["abbreviation"]
        dest = f"logos/{abbrev.lower()}.png"
        if os.path.exists(dest):
            skipped += 1
            continue
        # Find the 'full/default' logo (standard transparent-bg PNG)
        logo_url = next(
            (l["href"] for l in team.get("logos", []) if "default" in l.get("rel", [])),
            None,
        )
        if not logo_url:
            failed += 1
            continue
        try:
            data = fetch_bytes(logo_url)
            with open(dest, "wb") as f:
                f.write(data)
            downloaded += 1
        except Exception as e:
            print(f"\n  {abbrev} logo failed: {e}")
            failed += 1
        time.sleep(0.05)
    print(f"{downloaded} downloaded, {skipped} already present, {failed} failed")


def main():
    print("Fetching NFL team list…", flush=True)
    teams_data = fetch_json(f"{BASE_SITE}/teams")
    raw_teams = teams_data["sports"][0]["leagues"][0]["teams"]
    teams = [t["team"] for t in raw_teams]
    print(f"Found {len(teams)} teams\n", flush=True)

    download_logos(teams)
    print()

    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "season": SEASON,
        "teams": {},
    }

    errors = []
    for team in teams:
        tid = team["id"]
        abbrev = team["abbreviation"]
        sys.stdout.write(f"  {abbrev:<4} ")
        sys.stdout.flush()

        try:
            roster_map = build_roster_map(tid)
            time.sleep(DELAY)

            dc_url = f"{BASE_CORE}/seasons/{SEASON}/teams/{tid}/depthcharts"
            dc_data = fetch_json(dc_url)
            time.sleep(DELAY)

            offense = parse_offense(dc_data, roster_map)
            qb1 = offense["qb"][0]["name"] if offense["qb"] else "—"
            rb1 = offense["rb"][0]["name"] if offense["rb"] else "—"
            print(f"QB: {qb1:<24} RB: {rb1}", flush=True)

            result["teams"][tid] = {
                "id": tid,
                "abbreviation": abbrev,
                "displayName": team["displayName"],
                "shortDisplayName": team.get("shortDisplayName", abbrev),
                "nickname": team.get("nickname", ""),
                "color": team.get("color", "333333"),
                "alternateColor": team.get("alternateColor", "ffffff"),
                "logo": f"logos/{abbrev.lower()}.png",
                "offense": offense,
            }
        except Exception as e:
            print(f"ERROR: {e}", flush=True)
            errors.append((abbrev, str(e)))

    with open("cache.js", "w") as f:
        f.write(f"/* NFL Depth Charts {SEASON} — fetched {result['fetched_at']} */\n")
        f.write(f"const CACHE = {json.dumps(result, indent=2)};\n")

    total = len(result["teams"])
    print(f"\nWrote cache.js — {total}/32 teams")
    if errors:
        print(f"Errors ({len(errors)}): {', '.join(a for a, _ in errors)}")
    if total == 0:
        print("WARNING: No teams fetched. Check internet connection.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
