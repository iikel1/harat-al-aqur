# -*- coding: utf-8 -*-
"""Trace Dr Al Salmi's plan of the Al Aqur Wall into coordinates.

Input   assets/photos/p23-1.jpeg  — the plan as printed in the book (753x871),
        credited in the acknowledgements to د. الوليد بن زاهر السالمي.
Output  content/data/wall-plan.json — the wall circuit as a polygon, plus the
        position of every tower and gate the plan marks, in a 0-1000 square.

How the plan draws things, measured off the image rather than assumed:

  wall     a thin light-orange line, ~2px, dashed along some stretches
  tower    a solid filled disc, ~7-10px across, mean colour ~(233,142,89)
  gate     a thick dark-red bar across the wall, mean colour ~(193,78,26),
           often drawn as a pair of stacked bars — these are merged back
           into one gate here

The two are separated by luminance: discs sit near 155, bars near 100. Building
elevations (the fort, the castle, the mosques) are drawn in the same palette, so
anything further than TOUCHING_PX from the traced circuit is discarded — that is
what keeps the fort's round tower out of the tower list.

NOTHING HERE IS SURVEYED. The plan is a drawing in a book, traced at 753px wide.
Positions are good enough to point at a tower on a map; they are not coordinates
to navigate by, and the file records no latitude or longitude.

Run:  python work/trace_wall_plan.py
"""
import json
import math
import numpy as np
import cv2
from PIL import Image

PDF = 'book/REFRENCE.pdf'
PLAN_PAGE = 22            # zero-based: PDF page 23, which carries the plan AND its legend
PLAN = 'assets/photos/p23-1.jpeg'
OUT = 'content/data/wall-plan.json'

# Colour separation, measured from the image.
SATURATION = 55        # r - b, above this is "drawn in the plan's orange"
INK_MAX = 185          # ignore the pale fills
GATE_LUM = 130         # below this is a gate bar, above it a tower disc

TOUCHING_PX = 9        # how close a mark must sit to the circuit to belong to it
MIN_BLOB = 12          # ignore specks of JPEG noise
MAX_TOWER = 140        # a disc bigger than this is a building, not a tower
GATE_MERGE_PX = 14     # stacked bars closer than this are one gate

DILATE = 3             # closes the dashed stretches so the circuit is one loop
SIMPLIFY = 1.6         # Douglas-Peucker tolerance, in source pixels


def load_mask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    lum = (r + g + b) // 3
    return (((r - b) > SATURATION) & (lum < INK_MAX)).astype('uint8') * 255, lum


def wall_contour(m):
    """The circuit, recovered by closing the dashes and taking what is enclosed."""
    d = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=DILATE)
    h, w = d.shape
    ff = d.copy()
    cv2.floodFill(ff, np.zeros((h + 2, w + 2), np.uint8), (0, 0), 128)
    enclosed = (ff != 128).astype('uint8') * 255
    contours, _ = cv2.findContours(enclosed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest = max(contours, key=cv2.contourArea)
    return cv2.approxPolyDP(biggest, SIMPLIFY, True).reshape(-1, 2), biggest


def marks(m, lum, contour):
    """Every disc and bar drawn on the circuit."""
    eroded = cv2.erode(m, np.ones((3, 3), np.uint8), iterations=1)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(eroded, connectivity=8)
    towers, gates = [], []
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if area < MIN_BLOB:
            continue
        cx, cy = float(cent[i][0]), float(cent[i][1])
        # On the wall, or somewhere else in the drawing?
        if abs(cv2.pointPolygonTest(contour, (cx, cy), True)) > TOUCHING_PX:
            continue
        brightness = int(lum[lab == i].mean())
        if brightness < GATE_LUM:
            gates.append({'x': cx, 'y': cy, 'area': int(area)})
        elif area <= MAX_TOWER:
            towers.append({'x': cx, 'y': cy, 'area': int(area)})
    return towers, gates


def merge(points, radius):
    """A gate drawn as two stacked bars is one gate."""
    out = []
    for p in sorted(points, key=lambda d: -d['area']):
        for q in out:
            if (p['x'] - q['x']) ** 2 + (p['y'] - q['y']) ** 2 <= radius ** 2:
                q['x'] = (q['x'] * q['n'] + p['x']) / (q['n'] + 1)
                q['y'] = (q['y'] * q['n'] + p['y']) / (q['n'] + 1)
                q['n'] += 1
                break
        else:
            out.append({'x': p['x'], 'y': p['y'], 'n': 1})
    return out


def great_tower(gray, scale, ox, oy):
    """The fort's great round tower, which the plan draws as a crenellated circle.

    It is the one building the plan renders as a true footprint rather than as a
    little picture, so it is the only structure inside the wall worth placing.
    NOTE the plan is not to scale for individual buildings: this circle measures
    about 64 m across, where Nizwa Fort's tower is usually given as roughly 45 m.
    Its POSITION is the plan's; its size should be read as the drawing's, not the
    ground's. The page says so.
    """
    sub = cv2.GaussianBlur(gray[40:190, 300:470], (5, 5), 0)
    best = None
    for p2 in (28, 34, 40, 46):
        found = cv2.HoughCircles(sub, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                                 param1=100, param2=p2, minRadius=30, maxRadius=80)
        if found is None:
            continue
        for x, y, rad in np.round(found[0]).astype(int):
            if best is None or rad > best[2]:
                best = (x + 300, y + 40, rad)
    if not best:
        return None
    x, y, rad = best
    return {'id': 'fort-tower', 'x': round(x * scale + ox, 1), 'y': round(y * scale + oy, 1),
            'radius': round(rad * scale, 1)}


# The legend printed around the plan on the same page, keyed by the English name
# the book itself prints. Arabic is the book's own wording from that legend.
# Counting it: 14 towers + 3 "gate and tower" + 1 gate alone = 17 towers and
# 4 gates, which is exactly what the drawing shows.
LEGEND = {
    'Alkwareg Tower': ('برج الكوارج', 'tower'),
    'Balleg Tower': ('برج بلج', 'tower'),
    'Mahmoud Tower': ('برج محمود', 'tower'),
    'Alal’ia Tower': ('برج العلياء', 'tower'),
    'Qatet A’tawi Tower': ('برج قطعة الطوي', 'tower'),
    'Alqal’ah Tower': ('برج القلعة', 'tower'),
    'Almethabha Tower': ('برج المذبحة', 'tower'),
    'Ghowair Tower': ('برج غوير', 'tower'),
    'Merzah (Bustan Qassasm) Tower': ('برج ميرزة (بستان قسام)', 'tower'),
    'Kharis Balleg Tower': ('برج خريص بلج', 'tower'),
    'Harret A’zzamah Algharbi Tower': ('برج حارة الزامة الغربي', 'tower'),
    'Harret A’zzamah A’sharqi Tower': ('برج حارة الزامة الشرقي', 'tower'),
    'Bustan Alaqur A’sharqi Tower': ('برج بستان العقر الشرقي', 'tower'),
    'Bustan Alaqur Algharbi (Sikkat Alqaber) Tower':
        ('برج بستان العقر الغربي (سكة القبر)', 'tower'),
    'Alsuq Gate': ('صباح السوق', 'gate'),
    # A "gate and tower" label names two things standing together. Split into the
    # gate's name and the tower's name so neither is printed as both.
    'Alshujbi Gate & Tower': ('صباح وبرج الشجبي', 'both'),
    'Alsabkhe Gate & Tower': ('صباح وبرج الصبخة', 'both'),
    'Abi Almu’thir Gate & Tower': ('صباح وبرج أبي المؤثر', 'both'),
}

# The two halves of each combined label, written out rather than split by string
# surgery, so the Arabic reads properly in both cases.
SPLIT_LABEL = {
    'Alshujbi Gate & Tower': {
        'tower': ('برج الشجبي', 'Alshujbi Tower'),
        'gate': ('صباح الشجبي', 'Alshujbi Gate'),
    },
    'Alsabkhe Gate & Tower': {
        'tower': ('برج الصبخة', 'Alsabkhe Tower'),
        'gate': ('صباح الصبخة', 'Alsabkhe Gate'),
    },
    'Abi Almu’thir Gate & Tower': {
        'tower': ('برج أبي المؤثر', 'Abi Almu’thir Tower'),
        'gate': ('صباح أبي المؤثر', 'Abi Almu’thir Gate'),
    },
}
# Titles printed on the same page that name nothing on the circuit.
NOT_A_LABEL = ('NIZWA', 'FORT, CASTLE', 'Nizwa Fort', 'Nizwa Castle', 'AlAqur Wall')


def legend_labels(place):
    """Read the plan's own legend off the PDF page and put each label in plan units.

    The labels sit beside the features they name, with a leader line, so a label
    lands within roughly 60 plan units of its mark while neighbouring towers are
    about 180 apart. That gap is what makes matching by distance safe.
    """
    import pymupdf
    page = pymupdf.open(PDF)[PLAN_PAGE]
    rects = [r for xref in [i[0] for i in page.get_images(full=True)]
             for r in page.get_image_rects(xref)]
    if not rects:
        return []
    box = max(rects, key=lambda r: r.width * r.height)
    with Image.open(PLAN) as im:
        iw, ih = im.size

    spans = []
    for blk in page.get_text('dict')['blocks']:
        for line in blk.get('lines', []):
            for sp in line['spans']:
                txt = sp['text'].strip()
                if sum(c.isascii() and c.isalpha() for c in txt) < 3:
                    continue
                x0, y0, x1, y1 = sp['bbox']
                spans.append({'t': txt, 'x': (x0 + x1) / 2, 'y': (y0 + y1) / 2})

    # A label can be set over two or three lines; stack them back together.
    merged = []
    for sp in spans:
        for g in merged:
            if abs(g['x'] - sp['x']) < 30 and abs(g['y2'] - sp['y']) < 11:
                g['t'] += ' ' + sp['t']
                g['y2'] = sp['y']
                break
        else:
            merged.append({'t': sp['t'], 'x': sp['x'], 'y': sp['y'], 'y2': sp['y']})

    out = []
    for g in merged:
        if any(g['t'].startswith(p) for p in NOT_A_LABEL):
            continue
        entry = LEGEND.get(g['t'])
        if not entry:
            continue
        ix = (g['x'] - box.x0) / box.width * iw
        iy = (g['y'] - box.y0) / box.height * ih
        x, y = place(ix, iy)
        out.append({'en': g['t'], 'ar': entry[0], 'applies': entry[1], 'x': x, 'y': y})
    return out


def attach_legend(labels, towers, gates):
    """Give each mark the legend name nearest to it, closest pair first.

    Greedy on distance rather than nearest-per-label: two labels can share a
    nearest mark, and the closer one should win it.
    """
    pairs = []
    for li, lab in enumerate(labels):
        pool = []
        if lab['applies'] in ('tower', 'both'):
            pool += [('tower', i, m) for i, m in enumerate(towers)]
        if lab['applies'] in ('gate', 'both'):
            pool += [('gate', i, m) for i, m in enumerate(gates)]
        for kind, i, m in pool:
            pairs.append((math.hypot(m['x'] - lab['x'], m['y'] - lab['y']), li, kind, i))
    pairs.sort()

    taken, used = set(), {}
    for dist, li, kind, i in pairs:
        lab = labels[li]
        # a "gate and tower" label names one of each, so allow it twice
        key = (li, kind) if lab['applies'] == 'both' else (li,)
        if key in used or (kind, i) in taken:
            continue
        target = (towers if kind == 'tower' else gates)[i]
        half = SPLIT_LABEL.get(lab['en'], {}).get(kind)
        target['ar'] = half[0] if half else lab['ar']
        target['en'] = half[1] if half else lab['en']
        if half:
            target['legend_label'] = lab['en']
        target['label_distance'] = round(dist, 1)
        used[key] = True
        taken.add((kind, i))
    return sum(1 for m in towers + gates if m.get('ar'))


def snap_to_wall(point, poly):
    """Pull a mark onto the circuit.

    The discs and bars are detected at their own centres, while the circuit is
    recovered by dilating and filling, which pushes the traced line a few pixels
    outward, and is then simplified. The two therefore miss each other by around
    five metres at the model's scale - enough that a tower floats beside the wall
    instead of standing in it, and enough that a gateway never gets cut through.

    The book is explicit that the towers are attached to the wall
    ("الأبراج المتصلة به") and that the gates are its only openings, so putting a
    mark back on the line asserts what the source says rather than inventing a
    position. The detected point is kept alongside as `raw`.
    """
    px, py = point
    best, bestd = point, float('inf')
    for i in range(len(poly)):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % len(poly)]
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        t = 0.0 if L == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L))
        qx, qy = ax + t * dx, ay + t * dy
        d = (px - qx) ** 2 + (py - qy) ** 2
        if d < bestd:
            bestd, best = d, (qx, qy)
    return best, bestd ** 0.5


def compass(point, cx, cy):
    """Which side of the circuit a mark sits on. Geometry, not judgement — the
    plan is drawn north-up, so this is measured from the circuit's centroid."""
    import math
    angle = (math.degrees(math.atan2(-(point[1] - cy), point[0] - cx)) + 360) % 360
    for lo, hi, name in ((22.5, 67.5, 'north-east'), (67.5, 112.5, 'north'),
                         (112.5, 157.5, 'north-west'), (157.5, 202.5, 'west'),
                         (202.5, 247.5, 'south-west'), (247.5, 292.5, 'south'),
                         (292.5, 337.5, 'south-east')):
        if lo <= angle < hi:
            return name, round(angle)
    return 'east', round(angle)


def main():
    a = np.asarray(Image.open(PLAN).convert('RGB')).astype(int)
    m, lum = load_mask(a)
    poly, raw = wall_contour(m)
    towers, gates = marks(m, lum, raw)
    gates = merge(gates, GATE_MERGE_PX)

    # Normalise into a 0-1000 square, keeping the plan's aspect and its north-up
    # orientation (the plan carries a compass rose pointing up).
    h, w = m.shape
    scale = 1000.0 / max(w, h)
    ox, oy = (1000 - w * scale) / 2, (1000 - h * scale) / 2
    place = lambda x, y: [round(x * scale + ox, 1), round(y * scale + oy, 1)]

    doc = {
        'source': 'assets/photos/p23-1.jpeg — the plan of the Al Aqur Wall as printed in the '
                  'book, credited to Dr Al Walid bin Zahir Al Salmi.',
        'traced_by': 'work/trace_wall_plan.py',
        'caution': 'Traced from a 753px drawing in a book. Good enough to point at a feature '
                   'on a map; NOT a survey, and carries no latitude or longitude. The plan is '
                   'drawn north-up.',
        'viewBox': [0, 0, 1000, 1000],
        'wall': [place(x, y) for x, y in poly],
    }

    outline = doc['wall']
    cx = sum(p[0] for p in outline) / len(outline)
    cy = sum(p[1] for p in outline) / len(outline)

    def described(kind, items, prefix):
        rows = []
        for i, it in enumerate(sorted(items, key=lambda d: (d['y'], d['x'])), 1):
            raw = place(it['x'], it['y'])
            snapped, moved = snap_to_wall(raw, outline)
            side, bearing = compass(snapped, cx, cy)
            rows.append({'id': '%s%d' % (prefix, i),
                         'x': round(snapped[0], 1), 'y': round(snapped[1], 1),
                         'raw': raw, 'snapped_by': round(moved, 1),
                         'side': side, 'bearing': bearing})
        return rows

    doc['centroid'] = [round(cx, 1), round(cy, 1)]
    gray = cv2.cvtColor(np.asarray(Image.open(PLAN).convert('RGB')), cv2.COLOR_RGB2GRAY)
    tower = great_tower(gray, scale, ox, oy)
    doc['landmarks'] = [tower] if tower else []
    doc['towers'] = described('tower', towers, 't')
    doc['gates'] = described('gate', gates, 'g')

    # The plan's own legend, printed around it on the same page, names the marks.
    labels = legend_labels(place)
    named = attach_legend(labels, doc['towers'], doc['gates'])
    doc['legend'] = {
        'source': 'The legend printed around the plan on the same PDF page of the book, '
                  'signed by the same hand that drew the plan.',
        'labels_found': len(labels),
        'marks_named': named,
    }
    json.dump(doc, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    print('wall outline points: %d' % len(doc['wall']))
    moved = [m['snapped_by'] for m in doc['towers'] + doc['gates']]
    print('marks snapped onto the circuit by %.1f-%.1f plan units (mean %.1f)'
          % (min(moved), max(moved), sum(moved) / len(moved)))
    print("towers found on the circuit: %d  (the book's text says fifteen)" % len(doc['towers']))
    print('gates found on the circuit: %d' % len(doc['gates']))
    print('legend labels read: %d, marks named from the legend: %d'
          % (doc['legend']['labels_found'], doc['legend']['marks_named']))
    for l in doc['landmarks']:
        print('landmark: %s at (%.1f, %.1f) radius %.1f plan units' % (l['id'], l['x'], l['y'], l['radius']))
    for t in doc['towers']:
        print('   %-4s %-11s %3d deg  (%6.1f,%6.1f)' % (t['id'], t['side'], t['bearing'], t['x'], t['y']))
    for g in doc['gates']:
        print('   %-4s %-11s %3d deg  (%6.1f,%6.1f)' % (g['id'], g['side'], g['bearing'], g['x'], g['y']))
    print('-> %s' % OUT)


if __name__ == '__main__':
    main()
