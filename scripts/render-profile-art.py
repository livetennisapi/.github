#!/usr/bin/env python3
"""Render profile artwork with a local Geist font and fonttools[woff]."""

import argparse
import math
from html import escape
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


def lettering(faces, text, x, y, size, color="var(--ink)", weight=650):
    face = faces[weight]
    glyphs = face.getGlyphSet()
    cmap = face.getBestCmap()
    scale = size / face["head"].unitsPerEm
    parts = []
    cursor = 0
    for character in text:
        name = cmap[ord(character)]
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        if pen.getCommands():
            parts.append(f'<path transform="translate({cursor} 0)" d="{pen.getCommands()}"/>')
        cursor += face["hmtx"][name][0]
    return (
        f'<g aria-label="{escape(text, quote=True)}" fill="{color}" '
        f'transform="translate({x} {y}) scale({scale:.6f} {-scale:.6f})">'
        + "".join(parts) + "</g>"
    )


def tennis_ball(cx, cy, radius):
    r = radius
    return f'''<g transform="translate({cx} {cy})">
<circle r="{r}" fill="var(--ball)"/>
<path d="M {-r*.68:.2f} {-r*.73:.2f} C {r*.10:.2f} {-r*.36:.2f}, {r*.10:.2f} {r*.36:.2f}, {-r*.68:.2f} {r*.73:.2f}
M {r*.68:.2f} {-r*.73:.2f} C {-r*.10:.2f} {-r*.36:.2f}, {-r*.10:.2f} {r*.36:.2f}, {r*.68:.2f} {r*.73:.2f}"
fill="none" stroke="var(--base)" stroke-width="{r*.10:.2f}"/>
</g>'''


def sculpture(cx, cy, radius):
    parts = []
    for index in range(25):
        offset = (index - 12) / 12
        start_x = cx - radius * 1.6
        start_y = cy + offset * radius * .5
        end_x = cx + radius * .97 * math.cos(offset * math.pi / 2)
        end_y = cy + radius * .97 * math.sin(offset * math.pi / 2)
        bright = index % 4 == 0
        parts.append(
            f'<path d="M {start_x:.2f} {start_y:.2f} '
            f'C {cx-radius*.15:.2f} {cy+offset*radius*1.65:.2f}, '
            f'{cx-radius*.45:.2f} {cy-offset*radius*1.8:.2f}, {end_x:.2f} {end_y:.2f}" '
            f'fill="none" stroke="var(--wire)" stroke-width="{1.6 if bright else 1}" opacity="{.85 if bright else .42}"/>'
        )
    for angle in [-.86, -.23, .71, 1.4, 2.4, 3.43, 4.45]:
        x, y = cx + radius*math.cos(angle), cy+radius*math.sin(angle)
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.5" fill="var(--accent)"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="var(--wire)" stroke-width="1.3"/>')
    for rotation in [-40, -20, 0, 20, 40]:
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{radius*.37}" ry="{radius}" '
                     f'transform="rotate({rotation} {cx} {cy})" fill="none" '
                     'stroke="var(--wire)" stroke-width="1" opacity=".65"/>')
    parts.append(tennis_ball(cx, cy, radius * .39))
    return "".join(parts)


def artwork(faces, mobile):
    width, height = (720, 700) if mobile else (1280, 450)
    body = [f'<rect width="{width}" height="{height}" rx="14" fill="var(--base)"/>']
    if mobile:
        body.append(sculpture(440, 472, 166))
        body.append(tennis_ball(55, 54, 13))
        body.append(lettering(faces, "Live Tennis API", 81, 63, 26, weight=600))
        body.append(lettering(faces, "From the court.", 40, 159, 72))
        body.append(lettering(faces, "Into your code.", 40, 242, 72))
        body.append(lettering(faces, "REST + WebSocket", 43, 665, 28, "var(--muted)", 500))
    else:
        body.append(sculpture(1036, 232, 176))
        body.append(tennis_ball(72, 65, 13))
        body.append(lettering(faces, "Live Tennis API", 98, 74, 27, weight=600))
        body.append(lettering(faces, "From the court.", 54, 197, 85))
        body.append(lettering(faces, "Into your code.", 54, 296, 85))
        body.append(lettering(faces, "REST + WebSocket", 59, 391, 28, "var(--muted)", 500))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">
<title id="title">Live Tennis API. From the court. Into your code.</title>
<desc id="description">A tennis ball at the center of connected data paths. REST and WebSocket.</desc>
<style>
:root {{ --base: #f5f8f6; --ink: #15261d; --muted: #50645a; --ball: #138139; --accent: #138139; --wire: #459467; }}
@media (prefers-color-scheme: dark) {{ :root {{ --base: #090a0c; --ink: #ffffff; --muted: #acb9b2; --ball: #00ff41; --accent: #00ff41; --wire: #36bb79; }} }}
</style>
{"".join(body)}
</svg>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, required=True, help="Local Geist variable font, WOFF2 or TTF")
    args = parser.parse_args()
    source = TTFont(args.font)
    faces = {weight: instantiateVariableFont(source, {"wght": weight}, inplace=False) for weight in (500, 600, 650)}
    output = Path(__file__).resolve().parent.parent / "profile" / "assets"
    output.mkdir(exist_ok=True)
    for mobile in (False, True):
        path = output / ("hero-mobile.svg" if mobile else "hero.svg")
        path.write_text(artwork(faces, mobile))
        print(path.relative_to(output.parent.parent))


if __name__ == "__main__":
    main()
