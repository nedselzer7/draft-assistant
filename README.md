# NFL Depth Charts

A local depth chart viewer for fantasy football draft day. Shows who's first, second, and third string at every offensive position for all 32 NFL teams. Click team logos to pull up their depth chart, and select multiple teams to compare them side by side.

**Works offline** — all data is stored locally after setup. An internet connection is only needed to refresh roster data.

---

## What you'll need

- **Python 3** — used to download the data. Most Macs already have it. [How to check ↓](#do-i-have-python-3)
- **A modern browser** — Chrome, Firefox, Safari, or Edge all work.
- **~2 minutes** for the first-time setup.

That's it. No accounts, no API keys, nothing to install beyond Python.

---

## Getting started

### Step 1 — Download the files

**Option A — If you have git:**
```
git clone https://github.com/nedselzer7/draft-assistant.git
```

**Option B — If you don't have git:**
1. Click the green **Code** button at the top of this page on GitHub
2. Click **Download ZIP**
3. Unzip the downloaded file (double-click it on Mac)

### Step 2 — Open Terminal

On a Mac, press **⌘ + Space**, type **Terminal**, and press Enter.

> **Tip:** If you're not sure how to navigate to the right folder in Terminal, open Finder, find the `draft-assistant` folder, and drag it directly into the Terminal window after typing `cd ` (with a space). Then press Enter.

Or type it manually (adjust the path to wherever you unzipped/cloned it):
```
cd ~/Downloads/draft-assistant
```

### Step 3 — Run the setup script

```
python3 setup.py
```

This will:
- Download depth charts for all 32 teams from ESPN (~40 seconds)
- Download all 32 team logos (first time only)
- Open the viewer in your browser automatically

You'll see team names scrolling by as it works. When it's done, the browser opens on its own.

---

## Opening the app day-to-day

After the first-time setup, use this command to open the app:

```
python3 launch.py
```

This automatically checks whether your roster data is from a previous day. If it is, it refreshes before opening the browser — so you always have current depth charts without having to think about it.

---

## Using the viewer

**Select a team** — Click any team logo to load their depth chart in the table below.

**Compare teams** — Click multiple logos to see them side by side. The table adds a column for each team.

**Remove a team** — Click the **×** in that team's column header.

**Clear everything** — Click **Clear all** in the top right.

**Search** — Type a player or team name in the search box. Logos for teams that don't match will fade out, making it easy to spot which team a player is on.

**Keyboard shortcuts:**
- `/` — jump to the search box
- `Esc` — clear the search (if the search box is focused), or clear all selected teams

**Injury labels** appear next to any player with a current designation:
- `OUT` — out this week
- `Q` — questionable
- `D` — doubtful
- `DTD` — day-to-day
- `IR` — injured reserve

---

## Do I have Python 3?

Open Terminal and run:

```
python3 --version
```

If you see something like `Python 3.11.4`, you're all set.

If you get `command not found` or a version starting with `2.`, download Python 3:

1. Go to **[python.org/downloads](https://www.python.org/downloads/)**
2. Click the big yellow download button
3. Open the downloaded file and follow the installer
4. Restart Terminal, then try `python3 --version` again

---

## Troubleshooting

**"No depth chart data" on the page**
Run `python3 setup.py` (first time) or `python3 launch.py`, then reload the page.

**The page opens but logos are broken**
Delete the `logos/` folder and run `python3 fetch.py` to re-download them.

**`python3: command not found`**
Python 3 isn't installed. See [Do I have Python 3?](#do-i-have-python-3) above.

**Data looks outdated**
Run `python3 fetch.py` to pull the latest from ESPN, then reload the page.

**Windows users**
Everything works the same — use `python` instead of `python3` if needed. Run `python setup.py` or `python launch.py` in Command Prompt or PowerShell from the project folder.
