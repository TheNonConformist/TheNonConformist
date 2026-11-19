#!/usr/bin/env python3
"""Generate the NIGHT SHIFT pixel hero (SVG)."""

import random
from pathlib import Path

from gen_hero import FONT, glyph_path, pixel_map, rect, text

W, H = 1180, 440
BG = "#06080c"
WALL = "#0a0e15"
CREAM = "#d8d3c6"
DIMCREAM = "#b9b4a6"
MUTED = "#6d7280"
DIM = "#242a35"
RUST = "#e2603f"
NEON = "#ff5a6e"
GREEN = "#3ddc84"
SCREEN = "#04120a"


def arect(x, y, w, h, fill, children, opacity=1.0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
            f'opacity="{opacity}">{children}</rect>')


def build():
    random.seed(7)
    defs = ['<defs>']
    for ch, rows in FONT.items():
        defs.append(f'<g id="g{ord(ch)}"><path d="{glyph_path(rows)}"/></g>')
    defs.append(
        '<pattern id="dither" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="2" height="2" fill="{CREAM}" opacity="0.022"/></pattern>'
    )
    defs.append(
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#0a1220"/><stop offset="1" stop-color="#0e1726"/>'
        "</linearGradient>"
    )
    defs.append(
        '<radialGradient id="screenglow" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{GREEN}" stop-opacity="0.16"/>'
        f'<stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>'
        "</radialGradient>"
    )
    defs.append(
        '<clipPath id="inner"><rect x="20" y="20" width="1140" height="400"/></clipPath>'
    )
    defs.append(
        '<clipPath id="screen"><rect x="548" y="138" width="344" height="164"/></clipPath>'
    )
    defs.append("</defs>")

    b = []
    b.append(rect(0, 0, W, H, BG))
    b.append(rect(0, 0, W, H, "url(#dither)"))
    frame = "M20 6H1160V20H1174V420H1160V434H20V420H6V20H20Z"
    b.append(f'<path d="{frame}" fill="none" stroke="{DIMCREAM}" stroke-width="4" '
             'shape-rendering="crispEdges"/>')
    b.append(rect(18, 18, 1144, 404, "none",
                  f'stroke="{DIM}" stroke-width="2" shape-rendering="crispEdges"'))

    # top bar
    b.append(text(40, 30, "NIGHT SHIFT", 2, CREAM))
    b.append(text(1140, 30, "03:12 AM", 2, MUTED, anchor="end"))
    b.append(arect(1024, 32, 8, 8, GREEN,
                   '<animate attributeName="opacity" values="1;1;0.15;0.15;1" '
                   'keyTimes="0;0.5;0.55;0.95;1" dur="2.2s" repeatCount="indefinite"/>'))
    for x in range(40, 1140, 10):
        b.append(rect(x, 56, 6, 2, DIM))

    # ---------------- window ----------------
    b.append(rect(40, 74, 430, 256, "#0b111c", f'stroke="{DIMCREAM}" stroke-width="4"'))
    b.append(rect(52, 86, 406, 232, "url(#sky)"))

    # stars
    for _ in range(22):
        sx, sy = random.randrange(58, 452, 4), random.randrange(92, 200, 4)
        b.append(rect(sx, sy, 2, 2, CREAM, 'opacity="0.35"'))

    # moon (pixel circle)
    moon = [
        "..XXXX..",
        ".XXXXXX.",
        "XXXXXXXX",
        "XXX.XXXX",
        "XXXXXXXX",
        ".XXXXXX.",
        "..XXXX..",
    ]
    b.append(pixel_map(100, 120, 6, moon, {"X": CREAM}, opacity=0.9))

    # skyline
    buildings = [
        (52, 210, 54, 108), (110, 238, 40, 80), (154, 196, 46, 122),
        (204, 246, 34, 72), (242, 222, 58, 96), (304, 250, 44, 68),
        (352, 204, 50, 114), (406, 236, 52, 82),
    ]
    for x, y, w, h in buildings:
        b.append(rect(x, y, w, h, "#05070b"))
        for wy in range(y + 10, y + h - 8, 12):
            for wx in range(x + 8, x + w - 8, 12):
                if random.random() < 0.42:
                    b.append(rect(wx, wy, 3, 4, random.choice([GREEN, CREAM, RUST]),
                                  'opacity="0.55"'))

    # rain
    for i in range(20):
        rx = random.randrange(56, 452)
        ry = random.randrange(90, 260)
        ln = random.randrange(8, 18)
        opacity = random.choice([0.22, 0.3, 0.38, 0.46])
        b.append(
            f'<g opacity="{opacity}"><line x1="{rx}" y1="{ry}" x2="{rx-6}" '
            f'y2="{ry+ln}" stroke="{CREAM}" stroke-width="2">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 -40;0 260" dur="{random.uniform(1.1, 2.4):.2f}s" '
            f'begin="{random.uniform(0, 2.4):.2f}s" repeatCount="indefinite"/>'
            "</line></g>"
        )

    # window mullions
    b.append(rect(248, 86, 4, 232, DIMCREAM))
    b.append(rect(52, 198, 406, 4, DIMCREAM))
    # sill
    b.append(rect(32, 330, 446, 10, "#14181f", f'stroke="{DIM}" stroke-width="2"'))

    # ---------------- desk ----------------
    b.append(rect(480, 332, 680, 40, "#130f0c"))
    b.append(rect(480, 332, 680, 3, "#2a2018"))
    b.append(rect(480, 372, 680, 8, "#0b0907"))

    # monitor glow / stand
    b.append(rect(500, 92, 440, 260, "url(#screenglow)"))
    b.append(rect(690, 326, 60, 16, "#0c0f14"))
    b.append(rect(646, 342, 148, 8, "#0c0f14"))
    b.append(rect(520, 106, 400, 224, "#10141c",
                  f'stroke="{DIM}" stroke-width="4" shape-rendering="crispEdges"'))
    b.append(rect(548, 134, 344, 172, "#000000"))
    b.append(rect(548, 138, 344, 164, SCREEN))
    b.append(text(536, 314, "NC-01", 2, DIM))
    b.append(arect(890, 316, 6, 6, GREEN,
                   '<animate attributeName="opacity" values="1;0.4;1" dur="3s" repeatCount="indefinite"/>'))

    # screen text
    lines = [
        ("$", "ssh night@localhost"),
        (">", "mount /dev/rust"),
        (">", "init --systems"),
        (">", "ship --fast"),
        ("", "[ OK ] ready"),
    ]
    ty = 160
    for prompt, cmd in lines:
        if prompt:
            b.append(text(566, ty, prompt, 2, GREEN))
        b.append(text(590, ty, cmd, 2, GREEN if cmd.startswith("[") else CREAM))
        ty += 22
    b.append(arect(742, ty - 24, 10, 14, GREEN,
                   '<animate attributeName="opacity" values="1;1;0;0;1" '
                   'keyTimes="0;0.5;0.55;0.95;1" dur="1.1s" repeatCount="indefinite"/>'))

    # scanlines + slight bloom
    for sy in range(140, 302, 4):
        b.append(rect(548, sy, 344, 1, "#000000", 'opacity="0.28"'))
    b.append(rect(548, 138, 344, 164, "url(#screenglow)", 'opacity="0.5"'))

    # keyboard
    b.append(rect(544, 352, 340, 20, "#0c0f14",
                  f'stroke="{DIM}" stroke-width="2" shape-rendering="crispEdges"'))
    for ky in range(356, 370, 6):
        for kx in range(550, 872, 12):
            b.append(rect(kx, ky, 8, 4, "#1a1f28"))
    b.append(rect(640, 368, 70, 4, "#1a1f28"))
    b.append(rect(884, 358, 22, 2, "#1a1f28"))

    # mug + steam
    b.append(rect(398, 296, 32, 34, "#1a1f28",
                  f'stroke="{DIMCREAM}" stroke-width="2" shape-rendering="crispEdges"'))
    b.append(rect(430, 304, 8, 12, "none", f'stroke="{DIMCREAM}" stroke-width="3"'))
    b.append(rect(404, 300, 20, 3, RUST))
    for i, sx in enumerate((406, 414, 422)):
        b.append(
            f'<rect x="{sx}" y="300" width="3" height="3" fill="{CREAM}" opacity="0">'
            f'<animate attributeName="y" values="290;260" dur="2.4s" begin="{i*0.5}s" '
            'repeatCount="indefinite"/>'
            '<animate attributeName="opacity" values="0;0.4;0" dur="2.4s" '
            f'begin="{i*0.5}s" repeatCount="indefinite"/></rect>'
        )

    # cactus
    b.append(rect(486, 314, 28, 24, "#1a1512"))
    b.append(rect(484, 310, 32, 6, "#2a2018"))
    b.append(rect(496, 284, 8, 30, GREEN, 'opacity="0.8"'))
    b.append(rect(488, 292, 8, 6, GREEN, 'opacity="0.8"'))
    b.append(rect(488, 292, 5, 18, GREEN, 'opacity="0.8"'))
    b.append(rect(504, 288, 8, 6, GREEN, 'opacity="0.8"'))
    b.append(rect(507, 288, 5, 16, GREEN, 'opacity="0.8"'))

    # ---------------- neon sign ----------------
    for dx, op in ((2, 0.18), (0, 1)):
        b.append(text(1045 + dx, 96 + dx, "NON", 3, NEON, anchor="middle",
                      opacity=op))
        b.append(text(1045 + dx, 128 + dx, "CONFORM", 3, NEON, anchor="middle",
                      opacity=op))
        b.append(text(1045 + dx, 160 + dx, "IST", 3, NEON, anchor="middle",
                      opacity=op))
    b.append(text(1045, 192, "EST. 2025", 2, MUTED, anchor="middle"))
    b.append(text(1045, 212, "4 / 8 BADGES", 2, DIM, anchor="middle"))
    b.append(arect(960, 80, 170, 120, NEON,
                   '<animate attributeName="opacity" values="0;0.035;0;0.02;0" '
                   'keyTimes="0;0.1;0.2;0.7;1" dur="6s" repeatCount="indefinite"/>',
                   opacity=0))

    # ---------------- status readout ----------------
    rows = [("OS", "ARCH", CREAM), ("SHELL", "ZSH", CREAM),
            ("LANG", "RUST", RUST), ("MODE", "SHIP", GREEN)]
    sy = 238
    for label, value, color in rows:
        b.append(text(950, sy, label, 2, MUTED))
        b.append(text(1040, sy, value, 2, color))
        sy += 26
    b.append(rect(950, 340, 190, 2, DIM))

    # ---------------- footer ----------------
    for x in range(40, 1140, 10):
        b.append(rect(x, 386, 6, 2, DIM))
    b.append(text(40, 404, "> BUILD SMALL · SHIP FAST · READ THE SOURCE", 2, MUTED))
    b.append(text(1140, 404, "GITHUB.COM/THENONCONFORMIST", 2, MUTED, anchor="end"))

    # global scanline
    b.append(
        f'<rect x="20" y="20" width="1140" height="3" fill="{CREAM}" opacity="0.04" '
        'clip-path="url(#inner)">'
        '<animate attributeName="y" values="20;416" dur="8s" repeatCount="indefinite"/>'
        "</rect>"
    )

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        'role="img" aria-label="TheNonConformist — NIGHT SHIFT pixel CRT room">'
        + "".join(defs) + "".join(b) + "</svg>"
    )
    return svg


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "hero-nightshift.svg"
    svg = build()
    out.write_text(svg)
    print(f"wrote {out} ({len(svg)} bytes)")
