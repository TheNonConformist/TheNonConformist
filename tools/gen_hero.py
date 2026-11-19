#!/usr/bin/env python3
"""Generate the pixel-art profile hero card (SVG).

Everything is drawn on a pixel grid: glyphs are hand-built 5x7 bitmaps,
the crab and trophy icons are pixel maps, and the only animations are SMIL.
No external fonts, no anti-aliasing.
"""

from pathlib import Path

W, H = 1180, 440
BG = "#0a0c10"
PANEL = "#10141c"
CREAM = "#e8e3d5"
MUTED = "#7d8290"
DIM = "#2a303c"
RUST = "#e2603f"
RUST_HI = "#ff9a6b"
RUST_DK = "#a33f2a"
GREEN = "#3ddc84"
CYAN = "#58c8d8"

FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10011", "10101", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000"] * 7,
    ".": ["00000", "00000", "00000", "00000", "00000", "00110", "00110"],
    ":": ["00000", "00110", "00110", "00000", "00110", "00110", "00000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    ">": ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "·": ["00000", "00000", "00110", "00110", "00000", "00000", "00000"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "[": ["01110", "01000", "01000", "01000", "01000", "01000", "01110"],
    "]": ["01110", "00010", "00010", "00010", "00010", "00010", "01110"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    ",": ["00000", "00000", "00000", "00000", "00110", "00110", "01100"],
    "#": ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
}


def glyph_path(rows):
    parts = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            if row[x] == "1":
                run = 1
                while x + run < len(row) and row[x + run] == "1":
                    run += 1
                parts.append(f"M{x} {y}h{run}v1h-{run}z")
                x += run
            else:
                x += 1
    return "".join(parts)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, scale, color, anchor="start", opacity=1.0, anim=None):
    s = s.upper()
    w = (len(s) * 6 - 1) * scale
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    uses = []
    for i, ch in enumerate(s):
        if ch == " ":
            continue
        gid = ord(ch) if ch in FONT else ord(" ")
        uses.append(f'<use xlink:href="#g{gid}" x="{i * 6}"/>')
    a = f'<animate attributeName="opacity" {anim}/>' if anim else ""
    return (
        f'<g transform="translate({x:g} {y:g}) scale({scale})" fill="{color}" '
        f'opacity="{opacity}">{a}{"".join(uses)}</g>'
    )


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" {extra}/>'


def pixel_map(x, y, cell, rows, colors, opacity=1.0):
    out = []
    for ry, row in enumerate(rows):
        rx = 0
        while rx < len(row):
            c = row[rx]
            if c == ".":
                rx += 1
                continue
            run = 1
            while rx + run < len(row) and row[rx + run] == c:
                run += 1
            out.append(
                rect(x + rx * cell, y + ry * cell, run * cell, cell, colors[c],
                     'shape-rendering="crispEdges"')
            )
            rx += run
    return f'<g opacity="{opacity}">{"".join(out)}</g>'


def meter(x, y, filled, total=10):
    seg_w, gap, h = 16, 3, 14
    out = []
    for i in range(total):
        out.append(rect(x + i * (seg_w + gap), y, seg_w, h,
                        RUST if i < filled else "#1a1f28"))
    return f'<g>{"".join(out)}</g>'


def build():
    defs = ['<defs>']
    for ch, rows in FONT.items():
        defs.append(f'<g id="g{ord(ch)}"><path d="{glyph_path(rows)}"/></g>')
    defs.append(
        '<pattern id="dither" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="2" height="2" fill="{CREAM}" opacity="0.025"/></pattern>'
    )
    defs.append(
        '<clipPath id="inner"><rect x="20" y="20" width="1140" height="400"/></clipPath>'
    )
    defs.append("</defs>")

    body = []

    # background + frame
    body.append(rect(0, 0, W, H, BG))
    body.append(rect(0, 0, W, H, "url(#dither)"))
    frame = (
        "M20 6H1160V20H1174V420H1160V434H20V420H6V20H20Z"
    )
    body.append(f'<path d="{frame}" fill="none" stroke="{CREAM}" stroke-width="4" '
                'shape-rendering="crispEdges"/>')
    body.append(rect(18, 18, 1144, 404, "none",
                     f'stroke="{DIM}" stroke-width="2" shape-rendering="crispEdges"'))

    # top bar
    body.append(text(40, 34, "PLAYER ONE", 2, CREAM))
    body.append(text(1140, 34, "SYS ONLINE", 2, MUTED, anchor="end"))
    body.append(
        f'<rect x="994" y="36" width="8" height="8" fill="{GREEN}">'
        '<animate attributeName="opacity" values="1;1;0.15;0.15;1" '
        'keyTimes="0;0.55;0.6;0.95;1" dur="2.4s" repeatCount="indefinite"/></rect>'
    )
    for x in range(40, 1140, 10):
        body.append(rect(x, 66, 6, 2, DIM))

    # column separators
    for x in (400, 820):
        for y in range(84, 368, 10):
            body.append(rect(x, y, 2, 6, DIM))

    # left: crab
    crab_rows = [
        ".......EE....EE.........",
        "......EEEE..EEEE........",
        "......E@EE..EE@E........",
        "......EEEE..EEEE........",
        ".......HHHHHH...........",
        "..CCC..BBBBBBBB..CCC....",
        ".CCCCC.BBBBBBBB.CCCCC...",
        "CCCCCC.BBBBBBBB.CCCCCC..",
        "CCCCCCBBBBBBBBBBCCCCCC..",
        ".CCCCC.BBBMMBBB.CCCCC...",
        "..CCC..SSSSSSSS..CCC....",
        ".......BBBBBBBB.........",
        "......LL.LL.LL.LL.......",
        "......LL.LL.LL.LL.......",
    ]
    crab = {"B": RUST, "H": RUST_HI, "C": "#ff7a54", "S": RUST_DK,
            "L": "#f4865f", "E": CREAM, "@": BG, "M": BG}
    cx, cy, cell = 114, 90, 8
    body.append(pixel_map(cx, cy, cell, crab_rows, crab))
    # blink: cover each pupil with an eyelid that grows
    for ry, row in enumerate(crab_rows):
        for rx, ch in enumerate(row):
            if ch == "@":
                px, py = cx + rx * cell, cy + ry * cell
                body.append(
                    f'<rect x="{px}" y="{py}" width="{cell}" height="0" fill="{CREAM}">'
                    '<animate attributeName="height" values="0;0;7;0" '
                    'keyTimes="0;0.9;0.94;0.98" dur="4.8s" repeatCount="indefinite"/>'
                    '</rect>'
                )

    body.append(text(60, 240, "THE NONCONFORMIST", 2, CREAM))
    body.append(text(60, 268, "SYSTEMS ENGINEER", 2, MUTED))
    body.append(text(60, 308, "LVL 22", 3, RUST))
    body.append(text(200, 312, "XP 22/128", 2, DIM))
    body.append(text(60, 344, "EST. 2025", 2, DIM))

    # middle: attributes
    body.append(text(410, 92, "ATTRIBUTES", 2, CREAM))
    stats = [("RUST", 9, "96"), ("C", 8, "88"), ("PYTHON", 7, "74"), ("LINUX", 9, "92")]
    y = 136
    for name, filled, val in stats:
        body.append(text(410, y - 1, name, 2, CREAM))
        body.append(meter(530, y, filled))
        body.append(text(735, y - 1, val, 2, GREEN))
        y += 46

    body.append(text(410, 318, "EQUIPMENT", 2, CREAM))
    chips = [("NVIM", 60), ("ARCH", 60), ("TMUX", 60), ("DOCKER", 84), ("GIT", 48)]
    chip_x = 410
    for name, cw in chips:
        body.append(rect(chip_x, 340, cw, 26, "#12161e",
                         f'stroke="{DIM}" stroke-width="2" shape-rendering="crispEdges"'))
        body.append(text(chip_x + 6, 348, name, 2, MUTED))
        chip_x += cw + 8

    # right: trophies
    body.append(text(830, 92, "TROPHIES", 2, CREAM))
    body.append(text(1140, 92, "4 / 8", 2, DIM, anchor="end"))

    icons = {
        "shark": [
            "...X....",
            "..XXX...",
            ".XXXX...",
            "XXXXX...",
            ".XXXXX..",
            "..XXXX..",
            "...XXX..",
            "..X.X.X.",
        ],
        "brain": [
            ".XXX....",
            "XXXXX...",
            "XX.XX...",
            "XXXXX...",
            ".XXX....",
            "..X.....",
            "..XX....",
            "..X.....",
        ],
        "bolt": [
            "....XX..",
            "...XX...",
            "..XX....",
            ".XXXXX..",
            "...XX...",
            "..XX....",
            ".XX.....",
            "........",
        ],
        "hat": [
            "...XX...",
            "..XXXX..",
            ".XXXXXX.",
            "XXXXXXXX",
            "........",
            "XXXXXXXX",
            ".X.X.X.X",
            "........",
        ],
    }
    rows = [("shark", "PULL SHARK", "X2", GREEN),
            ("brain", "GALAXY BRAIN", "X2", GREEN),
            ("bolt", "QUICKDRAW", "EARNED", MUTED),
            ("hat", "YOLO", "EARNED", MUTED)]
    ry = 132
    for icon, label, tier, tcolor in rows:
        body.append(pixel_map(830, ry, 3, icons[icon], {"X": CREAM}))
        body.append(text(866, ry + 4, label, 2, CREAM))
        body.append(text(1140, ry + 4, tier, 2, tcolor, anchor="end"))
        ry += 50
    body.append(text(830, 334, "NEXT 128 MERGED PRS", 2, DIM))

    # footer
    for x in range(40, 1140, 10):
        body.append(rect(x, 376, 6, 2, DIM))
    body.append(text(40, 394, "> BUILD SMALL · SHIP FAST", 2, MUTED))
    body.append(text(1140, 394, "GITHUB.COM/THENONCONFORMIST", 2, MUTED, anchor="end"))
    body.append(text(590, 394, "PRESS START", 2, GREEN, anchor="middle",
                     anim='values="1;1;0;0;1" keyTimes="0;0.6;0.66;0.96;1" '
                          'dur="2.1s" repeatCount="indefinite"'))

    # subtle scanline
    body.append(
        f'<rect x="20" y="20" width="1140" height="4" fill="{CREAM}" opacity="0.05" '
        'clip-path="url(#inner)">'
        '<animate attributeName="y" values="20;416" dur="7s" repeatCount="indefinite"/>'
        '</rect>'
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        'role="img" aria-label="TheNonConformist pixel character sheet">'
        + "".join(defs) + "".join(body) + "</svg>"
    )
    return svg


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "hero-pixel.svg"
    out.write_text(build())
    print(f"wrote {out} ({len(build())} bytes)")
