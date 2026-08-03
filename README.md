# NFL Depth Charts

A local depth chart viewer for fantasy football draft day. Shows who's first, second, and third string at every offensive position for all 32 NFL teams. Click team logos to pull up their depth chart, and select multiple teams to compare them side by side.

**Works offline** — all data is stored locally. Run the fetch script once to download everything, then open the page any time without internet.

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

Or type these commands manually (adjust the path to wherever you unzipped/cloned it):
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

## Keeping data fresh

Rosters change throughout the preseason. Run this any time you want up-to-date depth charts:

```
python3 fetch.py
```

Then reload `index.html` in your browser (Ctrl+R or ⌘+R).

The **Updated** timestamp at the top of the page shows when the data was last pulled. It turns orange if it's more than a week old.

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
The data file hasn't been generated yet. Run `python3 setup.py` (first time) or `python3 fetch.py` (to refresh), then reload the page.

**The page opens but logos are broken**
The `logos/` folder is missing or incomplete. Delete it and run `python3 fetch.py` to re-download.

**`python3: command not found`**
Python 3 isn't installed. See [Do I have Python 3?](#do-i-have-python-3) above.

**Data looks outdated**
Rosters move fast during preseason. Run `python3 fetch.py` to pull the latest from ESPN.

**Windows users**
Everything works the same — use `python` instead of `python3` if needed. Run `python setup.py` in Command Prompt or PowerShell from the project folder.
