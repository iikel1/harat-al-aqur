"""Check every foreground/background token pair in src/styles/global.css against WCAG AA.

Parses the oklch() token values straight out of the stylesheet, in both the light
:root block and the dark prefers-color-scheme block, so the numbers can never
drift from what actually ships. Run it after touching any colour token.

    python work/check_contrast.py

Only pairings the templates actually make are listed in PAIRS. Adding a token to
the stylesheet does not add it here - if you start printing --ink-faint on a new
surface, add that pair, or the check will keep passing while the page fails.
"""
import math
import pathlib
import re
import sys

TARGET_BODY = 4.5   # WCAG AA, text under 18pt
TARGET_UI = 3.0     # WCAG AA, large text and UI boundaries


def oklch_to_linear(lightness, chroma, hue):
    h = math.radians(hue)
    a, b = chroma * math.cos(h), chroma * math.sin(h)
    l = (lightness + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (lightness - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (lightness - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def relative_luminance(oklch):
    """WCAG relative luminance is defined on LINEAR-light sRGB, which is exactly
    what the OKLab matrix produces. Do not gamma-encode on the way in - doing so
    double-decodes and silently inflates every ratio by roughly 2x."""
    r, g, b = (max(0.0, min(1.0, c)) for c in oklch_to_linear(*oklch))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def parse(css, opener):
    """Pull `--name: oklch(L C H)` pairs out of the block starting at `opener`."""
    start = css.find(opener)
    if start == -1:
        sys.exit("block not found: " + opener.strip())
    body = css[start + len(opener):]
    body = body[:body.find("\n  }" if opener.startswith("  ") else "\n}")]
    return {name: tuple(float(x) for x in value.split())
            for name, value in re.findall(r"--([\w-]+):\s*oklch\(([^)]+)\)", body)}


# (foreground, background, target) - every pairing the templates actually make.
PAIRS = [
    ("ink", "bg", TARGET_BODY), ("ink", "surface", TARGET_BODY),
    ("ink", "surface-sunk", TARGET_BODY), ("ink", "clay-wash", TARGET_BODY),
    ("ink-muted", "bg", TARGET_BODY), ("ink-muted", "surface", TARGET_BODY),
    ("ink-muted", "surface-sunk", TARGET_BODY), ("ink-muted", "clay-wash", TARGET_BODY),
    # --ink-faint never lands on clay-wash: the only clay-wash panels are
    # route.astro's .nomeasure (ink-muted) and .tag--gone (clay-deep).
    ("ink-faint", "bg", TARGET_BODY), ("ink-faint", "surface", TARGET_BODY),
    ("ink-faint", "surface-sunk", TARGET_BODY),
    ("clay", "bg", TARGET_BODY), ("clay", "surface", TARGET_BODY),
    ("clay", "surface-sunk", TARGET_BODY),
    ("clay-deep", "surface-sunk", TARGET_BODY), ("clay-deep", "clay-wash", TARGET_BODY),
    ("on-clay", "clay", TARGET_BODY), ("on-clay", "clay-deep", TARGET_BODY),
    # --rule / --rule-light are decorative hairlines and are exempt by design;
    # --rule-strong borders interactive controls and owes 3:1 (WCAG 1.4.11).
    ("rule-strong", "bg", TARGET_UI), ("rule-strong", "surface", TARGET_UI),
    ("rule-strong", "surface-sunk", TARGET_UI),
]


def check(name, tokens):
    print("\n=== " + name + " ===")
    fails = []
    for fg, bg, target in PAIRS:
        if fg not in tokens or bg not in tokens:
            sys.exit("unknown token in PAIRS: " + fg + " / " + bg)
        r = ratio(tokens[fg], tokens[bg])
        ok = r >= target
        if not ok:
            fails.append((name, fg, bg, r, target))
        print("  {:32} {:6.2f}  (needs {})  {}".format(
            fg + " on " + bg, r, target, "ok" if ok else "FAIL"))
    return fails


def main():
    css = pathlib.Path("src/styles/global.css").read_text(encoding="utf-8")
    light = parse(css, ":root {")
    dark = dict(light)
    dark.update(parse(css, "  :root {"))  # the nested block inside the media query
    fails = check("light", light) + check("dark", dark)
    if fails:
        print("\n{} pair(s) below target:".format(len(fails)))
        for theme, fg, bg, r, target in fails:
            print("  {}: {} on {} = {:.2f}, needs {}".format(theme, fg, bg, r, target))
        sys.exit(1)
    print("\nall pairs pass in both themes")


if __name__ == "__main__":
    main()
