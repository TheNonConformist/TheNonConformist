#!/usr/bin/env python3
"""Generate the pixel stats, contribution calendar and quest log cards.

Data comes from the GitHub REST + GraphQL APIs at build time; the workflow
commits the three SVGs back to the profile repo. No third-party card services.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from gen_hero import FONT, glyph_path, pixel_map, rect, text

USER = os.environ.get("PROFILE_USER", "TheNonConformist")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    sys.exit("GH_TOKEN is required")

API = "https://api.github.com"
BG = "#06080c"
PANEL = "#0b0e14"
CREAM = "#d8d3c6"
MUTED = "#6d7280"
DIM = "#242a35"
ORANGE = "#e2603f"
ORANGE_HI = "#ff9a6b"
GREEN = "#3ddc84"
CYAN = "#58c8d8"

LANG_COLORS = {
    "Python": "#3ddc84",
    "C": "#e2603f",
    "C++": "#ff9a6b",
    "CUDA": "#76b900",
    "HTML": "#d8d3c6",
    "Shell": "#6d7280",
    "Makefile": "#7d8290",
    "CMake": "#58c8d8",
    "JavaScript": "#f1e05a",
    "Dart": "#00b4ab",
    "Jupyter Notebook": "#da5b0b",
}

FEATURED = [
    ("Multi-Container-Runtime", "MULTI-CONTAINER RUNTIME",
     "container runtime built from scratch in C", "server"),
    ("Edge-Powered-Sequential-Anomaly-Detection-EP-SAD-", "EDGE ANOMALY DETECTION",
     "on-device anomaly detection for telemetry", "wave"),
    ("Console-Based-SocialNetwork", "CONSOLE SOCIAL NETWORK",
     "sockets, protocols and a social graph", "network"),
    ("Traffic-Monitoring-and-Statistics-Collector", "TRAFFIC COLLECTOR",
     "packet-level traffic analytics", "terminal"),
]


def api(path):
    req = urllib.request.Request(API + path)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "pixel-profile")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def graphql(query, variables):
    req = urllib.request.Request(
        API + "/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        method="POST",
    )
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "pixel-profile")
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.loads(r.read().decode())
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]


def defs():
    out = ['<defs>']
    for ch, rows in FONT.items():
        out.append(f'<g id="g{ord(ch)}"><path d="{glyph_path(rows)}"/></g>')
    out.append(
        '<pattern id="dither" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="2" height="2" fill="{CREAM}" opacity="0.022"/></pattern>'
    )
    out.append("</defs>")
    return "".join(out)


def frame(w, h):
    path = f"M20 6H{w-20}V20H{w-6}V{h-20}H{w-20}V{h-6}H20V{h-20}H6V20H20Z"
    return (
        f'<path d="{path}" fill="none" stroke="{CREAM}" stroke-width="3" '
        'shape-rendering="crispEdges"/>'
        + rect(16, 16, w - 32, h - 32, "none",
               f'stroke="{DIM}" stroke-width="1" shape-rendering="crispEdges"')
    )


def dashed(w, y):
    return "".join(rect(x, y, 5, 2, DIM) for x in range(32, w - 32, 9))


def svg_doc(w, h, body, label):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="{label}">'
        + defs() + rect(0, 0, w, h, BG) + rect(0, 0, w, h, "url(#dither)")
        + frame(w, h) + body + "</svg>"
    )


def pct(n, total):
    return 0 if not total else round(n * 100 / total)


def stat_card(user, repos, contributions, languages):
    w, h = 1180, 300
    b = []
    b.append(text(40, 24, "SYSTEM STATS", 2, CREAM))
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y").upper()
    b.append(text(1140, 24, "UPDATED " + stamp, 2, MUTED, anchor="end"))
    b.append(dashed(w, 48))

    cal = contributions["contributionCalendar"]
    values = [
        ("REPOS", user["public_repos"], CREAM),
        ("STARS", sum(r["stargazers_count"] for r in repos), ORANGE),
        ("COMMITS 1Y", contributions["totalCommitContributions"], GREEN),
        ("PRS 1Y", contributions["totalPullRequestContributions"], CREAM),
        ("FOLLOWERS", user["followers"], CREAM),
        ("CONTRIB 1Y", cal["totalContributions"], ORANGE_HI),
    ]
    for i, (label, value, color) in enumerate(values):
        x = 50 + i * 183
        b.append(text(x, 70, str(value), 4, color))
        b.append(text(x, 110, label, 2, MUTED))

    b.append(rect(40, 136, 1100, 1, DIM))
    b.append(text(40, 156, "LANGUAGES", 2, CREAM))
    b.append(text(1140, 156, "BY BYTES", 2, MUTED, anchor="end"))

    total = sum(languages.values()) or 1
    top = sorted(languages.items(), key=lambda kv: kv[1], reverse=True)[:5]
    for i, (name, n) in enumerate(top):
        x = 50 + i * 220
        percentage = pct(n, total)
        if percentage >= 10:
            filled = round(percentage / 10)
        else:
            filled = 1 if percentage else 0
        filled = max(0, min(10, filled))
        b.append(text(x, 184, name.upper(), 2, CREAM))
        b.append(text(x + 190, 184, f"{percentage}%", 2, MUTED, anchor="end"))
        for seg in range(10):
            color = LANG_COLORS.get(name, ORANGE) if seg < filled else "#171c24"
            b.append(rect(x + seg * 19, 202, 16, 12, color))

    b.append(text(40, 250, "FOCUS  C / C++ / CUDA / HPC / ML", 2, MUTED))
    b.append(text(1140, 250, "SINCE 2025", 2, DIM, anchor="end"))
    return svg_doc(w, h, "".join(b), "GitHub system stats")


def color_for(count):
    if count == 0:
        return "#12161e"
    if count == 1:
        return "#3a1f18"
    if count <= 3:
        return "#7a3424"
    if count <= 6:
        return "#b84a2e"
    return ORANGE


def contrib_card(contributions):
    w, h = 1180, 290
    cal = contributions["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for week in weeks for d in week["contributionDays"]]
    days.sort(key=lambda d: d["date"])

    current = 0
    for d in reversed(days):
        if d["contributionCount"] > 0:
            current += 1
        else:
            break
    best = run = 0
    for d in days:
        if d["contributionCount"] > 0:
            run += 1
            best = max(best, run)
        else:
            run = 0

    b = []
    b.append(text(40, 24, "CONTRIBUTIONS", 2, CREAM))
    b.append(text(1140, 24, "LAST 12 MONTHS", 2, MUTED, anchor="end"))
    b.append(dashed(w, 48))

    x0, y0, step, cell = 90, 82, 15, 12
    # month labels
    last_month = None
    for wi, week in enumerate(weeks):
        d = week["contributionDays"][0]["date"]
        month = d[:7]
        if month != last_month:
            label = datetime.strptime(d, "%Y-%m-%d").strftime("%b").upper()
            b.append(text(x0 + wi * step, 64, label, 1, MUTED))
            last_month = month

    day_labels = {1: "MON", 3: "WED", 5: "FRI", 6: "SUN"}
    for row, label in day_labels.items():
        b.append(text(52, y0 + row * step + 3, label, 1, MUTED))

    for wi, week in enumerate(weeks):
        for d in week["contributionDays"]:
            row = d["weekday"]
            b.append(rect(x0 + wi * step, y0 + row * step, cell, cell,
                          color_for(d["contributionCount"])))

    # legend
    b.append(text(90, 200, "LESS", 1, MUTED))
    for i, c in enumerate(["#12161e", "#3a1f18", "#7a3424", "#b84a2e", ORANGE]):
        b.append(rect(132 + i * step, 196, cell, cell, c))
    b.append(text(132 + 5 * step + 6, 200, "MORE", 1, MUTED))

    # right summary
    b.append(text(930, 82, "TOTAL", 2, MUTED))
    b.append(text(930, 102, str(cal["totalContributions"]), 4, CREAM))
    b.append(text(930, 148, "CURRENT STREAK", 2, MUTED))
    b.append(text(930, 168, f"{current} DAYS", 3, GREEN))
    b.append(text(930, 206, "BEST STREAK", 2, MUTED))
    b.append(text(930, 226, f"{best} DAYS", 3, ORANGE))

    first = days[0]["date"][:7] if days else ""
    last = days[-1]["date"][:7] if days else ""
    fmt = lambda s: datetime.strptime(s, "%Y-%m").strftime("%b %Y").upper()
    b.append(text(40, 258, "DATA VIA GITHUB GRAPHQL", 2, DIM))
    b.append(text(1140, 258, f"{fmt(first)} - {fmt(last)}", 2, DIM, anchor="end"))
    return svg_doc(w, h, "".join(b), "Pixel contribution calendar")


ICONS = {
    "server": [
        ".XXXXXX.",
        ".X.XX.X.",
        ".XXXXXX.",
        ".X.XX.X.",
        ".XXXXXX.",
        ".X.XX.X.",
        ".XXXXXX.",
        "........",
    ],
    "wave": [
        "........",
        "..X.....",
        "..X..X..",
        "X.X..X..",
        "X.X..X.X",
        "X.XX.X.X",
        "X.XX.X.X",
        "........",
    ],
    "network": [
        "X.....X.",
        ".X...X..",
        "..X.X...",
        "...X....",
        "..X.X...",
        ".X...X..",
        "X.....X.",
        "........",
    ],
    "terminal": [
        "XXXXXXXX",
        "X......X",
        "X.X....X",
        "X..X...X",
        "X.X....X",
        "X......X",
        "XXXXXXXX",
        "........",
    ],
}


def wrap(s, n):
    words = s.split()
    lines, line = [], ""
    for word in words:
        cand = (line + " " + word).strip()
        if len(cand) <= n:
            line = cand
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines[:2]


def push_age(iso):
    then = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    days = max(0, (datetime.now(timezone.utc) - then).days)
    if days == 0:
        return "TODAY", days
    if days < 30:
        return f"{days}D", days
    if days < 365:
        return f"{days // 30}M", days
    return f"{days // 365}Y", days


def quests_card(repos):
    w, h = 1180, 420
    by_name = {r["name"]: r for r in repos}
    b = []
    b.append(text(40, 24, "QUEST LOG", 2, CREAM))
    b.append(text(1140, 24, "ACTIVE REPOS", 2, MUTED, anchor="end"))
    b.append(dashed(w, 48))

    for i, (name, display, blurb, icon) in enumerate(FEATURED):
        repo = by_name.get(name)
        if not repo:
            continue
        col, row = i % 2, i // 2
        x, y = 40 + col * 560, 64 + row * 160
        cw, ch = 540, 146
        age, days = push_age(repo["pushed_at"])
        accent = GREEN if days < 30 else ORANGE
        b.append(rect(x, y, cw, ch, PANEL,
                      f'stroke="{DIM}" stroke-width="2" shape-rendering="crispEdges"'))
        b.append(rect(x, y, cw, 3, accent))
        b.append(pixel_map(x + 16, y + 18, 4, ICONS[icon], {"X": accent}))
        b.append(text(x + 58, y + 14, display, 2, CREAM))
        for j, line in enumerate(wrap(blurb, 38)):
            b.append(text(x + 58, y + 40 + j * 18, line, 2, MUTED))
        lang = (repo.get("language") or "N/A").upper()
        b.append(text(x + 58, y + 108, lang, 2, ORANGE_HI))
        b.append(text(x + 140, y + 108, f"STARS {repo['stargazers_count']}", 2, CREAM))
        b.append(text(x + 260, y + 108, f"ISSUES {repo['open_issues_count']}", 2, MUTED))
        b.append(text(x + 380, y + 108, f"PUSH {age}", 2, accent))

    b.append(text(40, 386, "MORE AT GITHUB.COM/THENONCONFORMIST", 2, MUTED))
    b.append(text(1140, 386, "FEATURED REPOS", 2, DIM, anchor="end"))
    return svg_doc(w, h, "".join(b), "Pixel quest log")


def main():
    user = api(f"/users/{USER}")
    repos = [r for r in api(f"/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]

    data = graphql(
        """query($login:String!){
          user(login:$login){
            contributionsCollection{
              contributionCalendar{
                totalContributions
                weeks{contributionDays{date contributionCount weekday}}
              }
              totalCommitContributions
              totalPullRequestContributions
              totalIssueContributions
              totalPullRequestReviewContributions
            }
          }
        }""",
        {"login": USER},
    )["user"]
    contributions = data["contributionsCollection"]

    languages = {}
    for repo in repos:
        try:
            for name, n in api(f"/repos/{repo['full_name']}/languages").items():
                languages[name] = languages.get(name, 0) + n
        except urllib.error.HTTPError:
            continue

    out = Path(__file__).resolve().parent.parent / "assets"
    out.joinpath("stats-pixel.svg").write_text(
        stat_card(user, repos, contributions, languages))
    out.joinpath("contrib-pixel.svg").write_text(
        contrib_card(contributions))
    out.joinpath("quests-pixel.svg").write_text(
        quests_card(repos))

    print("repos:", len(repos), "stars:", sum(r["stargazers_count"] for r in repos))
    print("contributions:", contributions["contributionCalendar"]["totalContributions"])
    print("languages:", sorted(languages.items(), key=lambda kv: kv[1], reverse=True)[:5])


if __name__ == "__main__":
    main()
