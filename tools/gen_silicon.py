#!/usr/bin/env python3
"""Generate the SILICON die-shot hero (SVG).

Top-down GPU floorplan on a pixel grid: 8 GPCs, 80 SMs, L2 slices, four HBM3
stacks, PHY lanes, PCIe, an SM zoom panel and live warp traffic.
"""

from pathlib import Path

from gen_hero import FONT, glyph_path, rect, text

W, H = 1180, 440
BG = "#05070b"
PACKAGE = "#080b10"
SUB = "#0b1018"
DIE = "#0e141d"
BLOCK = "#131a24"
BLOCK2 = "#1a2330"
GRID = "#22303f"
CREAM = "#d8d3c6"
MUTED = "#6d7280"
DIM = "#232c38"
ORANGE = "#e2603f"
ORANGE_HI = "#ff9a6b"
GREEN = "#3ddc84"
CYAN = "#58c8d8"
AMBER = "#ffb454"
RED = "#ff5a6e"


def arect(x, y, w, h, fill, children, opacity=1.0, extra=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
            f'opacity="{opacity}" {extra}>{children}</rect>')


def defs():
    out = ['<defs>']
    for ch, rows in FONT.items():
        out.append(f'<g id="g{ord(ch)}"><path d="{glyph_path(rows)}"/></g>')
    out.append(
        '<pattern id="dither" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="2" height="2" fill="{CREAM}" opacity="0.02"/></pattern>'
    )
    out.append(
        '<pattern id="subgrid" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<path d="M16 0H0V16" fill="none" stroke="{GRID}" stroke-width="1" opacity="0.28"/>'
        "</pattern>"
    )
    out.append(
        '<pattern id="diegrid" width="8" height="8" patternUnits="userSpaceOnUse">'
        f'<path d="M8 0H0V8" fill="none" stroke="#16202b" stroke-width="1" opacity="0.9"/>'
        "</pattern>"
    )
    out.append(
        '<clipPath id="inner"><rect x="20" y="20" width="1140" height="400"/></clipPath>'
    )
    out.append("</defs>")
    return "".join(out)


def build():
    b = []
    b.append(rect(0, 0, W, H, BG))
    b.append(rect(0, 0, W, H, "url(#dither)"))
    frame = "M20 6H1160V20H1174V420H1160V434H20V420H6V20H20Z"
    b.append(f'<path d="{frame}" fill="none" stroke="{CREAM}" stroke-width="3" '
             'shape-rendering="crispEdges"/>')
    b.append(rect(16, 16, 1148, 408, "none",
                  f'stroke="{DIM}" stroke-width="1" shape-rendering="crispEdges"'))

    # header
    b.append(text(40, 20, "NC-01", 3, CREAM))
    b.append(text(150, 24, "SILICON / FLOORPLAN", 2, MUTED))
    b.append(text(800, 26, "ACTIVE", 2, GREEN))
    b.append(arect(782, 28, 7, 7, GREEN,
                   '<animate attributeName="opacity" values="1;1;0.15;0.15;1" '
                   'keyTimes="0;0.5;0.56;0.94;1" dur="2.4s" repeatCount="indefinite"/>'))
    b.append(text(1140, 26, "REV C · 5NM · 1.8G", 2, MUTED, anchor="end"))
    for x in range(40, 1140, 10):
        b.append(rect(x, 50, 6, 2, DIM))

    # package + substrate
    b.append(rect(40, 68, 780, 300, PACKAGE, f'stroke="{GRID}" stroke-width="2"'))
    b.append(rect(44, 72, 772, 292, "url(#subgrid)"))
    # package corner marks
    for x, y, sx, sy in ((48, 76, 1, 1), (812, 76, -1, 1),
                         (48, 360, 1, -1), (812, 360, -1, -1)):
        b.append(rect(x, y, 10 * sx, 2, CREAM, 'opacity="0.5"') if sx > 0
                 else rect(x + 10 * sx, y, 10, 2, CREAM, 'opacity="0.5"'))
        b.append(rect(x, y, 2, 10 * sy, CREAM, 'opacity="0.5"') if sy > 0
                 else rect(x, y + 10 * sy, 2, 10, CREAM, 'opacity="0.5"'))

    # HBM stacks
    for x in (60, 116, 696, 752):
        b.append(text(x + 4, 96, "HBM3", 1, AMBER))
        for layer in range(4):
            y = 108 + layer * 52
            b.append(rect(x, y, 48, 44, "#151b24",
                          f'stroke="{GRID}" stroke-width="1" shape-rendering="crispEdges"'))
            b.append(rect(x + 4, y + 4, 40, 2, "#26303c"))
            for tx in (8, 18, 28, 38):
                b.append(rect(x + tx, y + 8, 1, 30, ORANGE, 'opacity="0.5"'))
            b.append(rect(x + 6, y + 40, 36, 1, AMBER, 'opacity="0.35"'))
        b.append(rect(x + 3, 316, 42, 4, "#26303c"))
        for bx in (8, 20, 32, 40):
            b.append(rect(x + bx, 320, 4, 3, AMBER, 'opacity="0.6"'))

    # PHY lanes
    for x in (172, 672):
        b.append(rect(x, 108, 18, 208, "#0c121a", f'stroke="{GRID}" stroke-width="1"'))
        for i in range(10):
            b.append(rect(x + 4, 114 + i * 20, 10, 2, ORANGE, 'opacity="0.55"'))
        b.append(text(x + 3, 330, "PHY", 1, MUTED))

    # HBM <-> PHY traces + packets
    for side, x1, x2 in ((0, 164, 172), (1, 670, 696)):
        for y in (120, 160, 200, 240, 280):
            b.append(rect(min(x1, x2), y, abs(x2 - x1), 1, ORANGE, 'opacity="0.28"'))
    for i, y in enumerate((122, 162, 202, 242, 282)):
        b.append(arect(164, y - 2, 6, 5, AMBER,
                       f'<animateTransform attributeName="transform" type="translate" '
                       f'values="0 0;{28 if i % 2 == 0 else -28} 0;0 0" '
                       f'dur="{2 + i * 0.3:.1f}s" repeatCount="indefinite"/>',
                       opacity=0.8))

    # die
    b.append(rect(190, 92, 480, 256, DIE, f'stroke="{GRID}" stroke-width="2"'))
    b.append(rect(192, 94, 476, 252, "url(#diegrid)"))
    b.append(rect(190, 80, 480, 3, ORANGE, 'opacity="0.7"'))
    b.append(text(196, 74, "12V", 1, MUTED))
    b.append(text(204, 334, "NC-01 · DIE 01 · 5NM", 1, MUTED))

    # die measurement ticks
    for ty in range(100, 348, 16):
        b.append(rect(184, ty, 5, 1, CREAM, 'opacity="0.35"'))
        b.append(rect(671, ty, 5, 1, CREAM, 'opacity="0.35"'))
    for tx in range(200, 670, 16):
        b.append(rect(tx, 86, 1, 5, CREAM, 'opacity="0.35"'))
        b.append(rect(tx, 347, 1, 5, CREAM, 'opacity="0.35"'))

    # GPCs: 8 clusters, 10 SMs each (5 x 2)
    for g in range(8):
        col, row = g % 4, g // 4
        x = 204 + col * 112
        y = 108 + row * 88
        active = g == 0
        b.append(rect(x, y, 104, 78, BLOCK,
                      f'stroke="{GREEN if active else GRID}" stroke-width="1"'))
        b.append(text(x + 4, y + 4, f"GPC {g}", 1, GREEN if active else MUTED))
        for sm in range(10):
            sx = x + 7 + (sm % 5) * 19
            sy = y + 18 + (sm // 5) * 21
            b.append(rect(sx, sy, 16, 18,
                          "#1b3a2c" if active else BLOCK2,
                          f'stroke="{GREEN if active else GRID}" stroke-width="1"'))
            b.append(rect(sx + 3, sy + 3, 10, 2,
                          GREEN if active else "#2a3a4c", 'opacity="0.8"'))
            b.append(rect(sx + 3, sy + 8, 10, 2,
                          GREEN if active else "#2a3a4c", 'opacity="0.5"'))

    # warp traffic inside active GPC
    for i in range(5):
        b.append(arect(214 + i * 18, 132, 4, 4, GREEN,
                       f'<animateTransform attributeName="transform" type="translate" '
                       f'values="0 0;0 20;18 20;18 0;0 0" dur="{2.2 + i * 0.35:.1f}s" '
                       f'begin="{i * 0.3:.1f}s" repeatCount="indefinite"/>',
                       opacity=0.9))

    # L2 slices
    for i in range(8):
        x = 204 + i * 55
        b.append(rect(x, 282, 52, 30, "#16222c", f'stroke="{GRID}" stroke-width="1"'))
        b.append(rect(x + 4, 286, 44, 2, CYAN, 'opacity="0.6"'))
        b.append(rect(x + 4, 306, 44, 1, CYAN, 'opacity="0.25"'))
    b.append(text(648, 290, "L2", 1, CYAN))
    b.append(arect(204, 282, 26, 30, GREEN,
                   '<animate attributeName="x" values="204;618" dur="3.6s" '
                   'repeatCount="indefinite"/>', opacity=0.12))
    # thermal pulse on active GPC
    b.append(arect(204, 108, 104, 78, RED,
                   '<animate attributeName="opacity" values="0.02;0.09;0.02" '
                   'dur="3s" repeatCount="indefinite"/>', opacity=0.02))

    # PCIe lanes
    for i in range(16):
        x = 330 + i * 10
        b.append(rect(x, 352, 7, 12, GREEN if i % 3 == 0 else ORANGE,
                      'opacity="0.8"'))
    b.append(text(500, 356, "PCIE", 1, MUTED))

    # SM zoom panel
    b.append(rect(860, 68, 280, 160, PACKAGE, f'stroke="{GRID}" stroke-width="2"'))
    b.append(text(872, 76, "SM / ZOOM", 2, CREAM))
    b.append(text(1128, 80, "0.1", 1, MUTED, anchor="end"))
    for i in range(4):
        y = 108 + i * 15
        b.append(rect(872, y, 40, 10, BLOCK2, f'stroke="{GRID}" stroke-width="1"'))
        b.append(rect(876, y + 3, 6, 4, GREEN, 'opacity="0.8"'))
        b.append(rect(884, y + 3, 22, 2, "#2a3a4c"))
        b.append(rect(906, y + 5, 3, 2, GREEN, 'opacity="0.7"'))
    b.append(text(872, 170, "WARP", 1, MUTED))

    for i in range(32):
        x = 944 + (i % 8) * 8
        y = 108 + (i // 8) * 8
        b.append(rect(x, y, 6, 6, ORANGE if i % 4 == 0 else BLOCK2,
                      f'stroke="{GRID}" stroke-width="1"'))
    b.append(text(944, 146, "FP32 X32", 1, MUTED))

    for i in range(4):
        b.append(rect(1040 + i * 12, 108, 9, 9, CYAN,
                      f'stroke="{GRID}" stroke-width="1" opacity="0.8"'))
    b.append(text(1040, 132, "TENSOR", 1, MUTED))

    b.append(rect(872, 178, 256, 16, "#16222c", f'stroke="{GRID}" stroke-width="1"'))
    b.append(text(878, 182, "L1 / SMEM", 1, CREAM))
    b.append(text(1122, 182, "256K", 1, CYAN, anchor="end"))
    b.append(text(872, 206, "4 WARP · 32 FP32 · 4 TENSOR", 1, MUTED))

    # telemetry
    rows = [
        ("PROCESS", "5NM", CREAM),
        ("SMS", "80 / 80", GREEN),
        ("HBM", "32G / 3.2T", AMBER),
        ("POWER", "320W", CREAM),
        ("TEMP", "61C", GREEN),
    ]
    ty = 246
    for label, value, color in rows:
        b.append(text(860, ty, label, 2, MUTED))
        b.append(text(980, ty, value, 2, color))
        ty += 24
    b.append(rect(860, 236, 280, 1, DIM))

    # footer
    for x in range(40, 1140, 10):
        b.append(rect(x, 384, 6, 2, DIM))
    b.append(text(40, 402, "> 8 GPC · 80 SM · 4 HBM · 256K L2", 2, MUTED))
    b.append(text(1140, 402, "GITHUB.COM/THENONCONFORMIST", 2, MUTED, anchor="end"))

    # clock sweep + global scanline
    b.append(arect(190, 92, 2, 256, CREAM,
                   '<animate attributeName="x" values="190;668" dur="6s" '
                   'repeatCount="indefinite"/>', opacity=0.06))
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
        'role="img" aria-label="TheNonConformist — SILICON GPU die floorplan">'
        + defs() + "".join(b) + "</svg>"
    )
    return svg


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "hero-silicon.svg"
    svg = build()
    out.write_text(svg)
    print(f"wrote {out} ({len(svg)} bytes)")
