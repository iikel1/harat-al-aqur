"""Build the site icons from the mark.

    python work/build_icons.py   # src/components/Mark.astro -> public/icon.svg, public/apple-touch-icon.png

The geometry is READ OUT OF THE COMPONENT, so `src/components/Mark.astro` stays
the single source of truth for the mark. Change the four runs there and re-run
this; never hand-edit the files in public/.

Two icons, because they are composited differently:

  icon.svg              transparent, clay stroke. Modern browsers scale it and
                        it sits fine on a light or a dark tab strip.
  apple-touch-icon.png  180x180, opaque. iOS composites a home-screen icon on
                        black and squares off transparency, so this one is
                        painted on the site's own --bg rather than left clear.

PIL cannot rasterise SVG, so the PNG is stroked directly from the same polyline
points: supersampled 4x, round joins and caps drawn explicitly, then downscaled.
"""

from __future__ import annotations

import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = ROOT / 'src' / 'components' / 'Mark.astro'
PUBLIC = ROOT / 'public'

# The tokens, straight from src/styles/global.css.
CLAY = (0.550, 0.100, 45)   # --clay
BG = (0.965, 0.010, 78)     # --bg

# Must match the <svg> in Mark.astro.
VIEWBOX = (-7, -7, 114, 114)
STROKE = 5.2


# --------------------------------------------------------------------------- #
# colour                                                                      #
# --------------------------------------------------------------------------- #
def oklch_to_rgb(L: float, C: float, h_deg: float) -> tuple[int, int, int]:
    """OKLCh -> 8-bit sRGB. The stylesheet is authored in oklch; PIL is not."""
    h = math.radians(h_deg)
    a, b = C * math.cos(h), C * math.sin(h)

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_**3, m_**3, s_**3

    lin = (
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )

    def encode(u: float) -> int:
        u = max(0.0, min(1.0, u))
        u = 12.92 * u if u <= 0.0031308 else 1.055 * u ** (1 / 2.4) - 0.055
        return round(u * 255)

    return tuple(encode(v) for v in lin)  # type: ignore[return-value]


# --------------------------------------------------------------------------- #
# geometry                                                                    #
# --------------------------------------------------------------------------- #
def read_runs() -> list[list[tuple[float, float]]]:
    """Pull the four open wall runs out of Mark.astro."""
    src = MARK.read_text(encoding='utf-8')
    runs = []
    for d in re.findall(r'<path\s*\n?\s*d="([^"]+)"', src):
        pts = [
            (float(x), float(y))
            for x, y in re.findall(r'([-\d.]+)\s+([-\d.]+)', d)
        ]
        runs.append(pts)
    if len(runs) != 4:
        raise SystemExit(f'expected 4 runs in Mark.astro, found {len(runs)}')
    return runs


def build_svg(runs) -> str:
    x, y, w, h = VIEWBOX
    clay = '#%02x%02x%02x' % oklch_to_rgb(*CLAY)
    paths = '\n  '.join(
        '<path d="M%s" />' % ' L'.join(f'{px:g} {py:g}' for px, py in run)
        for run in runs
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" '
        f'fill="none" stroke="{clay}" stroke-width="{STROKE}" '
        f'stroke-linecap="round" stroke-linejoin="round">\n'
        f'  <title>Harat Al Aqur</title>\n  {paths}\n</svg>\n'
    )


def build_png(runs, size: int = 180, ss: int = 4) -> 'Image.Image':
    from PIL import Image, ImageDraw

    vx, vy, vw, vh = VIEWBOX
    big = size * ss
    # Inset the mark a little; a home-screen icon that bleeds to the corners
    # reads as cropped once iOS rounds it off.
    pad = big * 0.13
    scale = (big - 2 * pad) / vw

    img = Image.new('RGB', (big, big), oklch_to_rgb(*BG))
    draw = ImageDraw.Draw(img)
    clay = oklch_to_rgb(*CLAY)
    w = STROKE * scale
    r = w / 2

    def to_px(p):
        return (pad + (p[0] - vx) * scale, pad + (p[1] - vy) * scale)

    for run in runs:
        pts = [to_px(p) for p in run]
        # joint='curve' rounds the interior joins; the caps are drawn on top.
        draw.line(pts, fill=clay, width=round(w), joint='curve')
        for px, py in (pts[0], pts[-1]):
            draw.ellipse((px - r, py - r, px + r, py + r), fill=clay)

    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    runs = read_runs()
    PUBLIC.mkdir(exist_ok=True)

    svg = PUBLIC / 'icon.svg'
    svg.write_text(build_svg(runs), encoding='utf-8')
    print(f'{svg.relative_to(ROOT)} - {svg.stat().st_size} bytes')

    png = PUBLIC / 'apple-touch-icon.png'
    build_png(runs).save(png)
    print(f'{png.relative_to(ROOT)} - 180x180, {png.stat().st_size} bytes')


if __name__ == '__main__':
    main()
