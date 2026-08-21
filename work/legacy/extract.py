import pymupdf, re, sys

LTR = re.compile(r'[0-9A-Za-z\-/%.,:]+')

def fix_span(chars):
    """Reverse zero-width ligature groups; drop kashida artifacts."""
    chars = [c for c in chars if c['c'] != '\u00c9']
    out = []
    i = 0
    n = len(chars)
    while i < n:
        j = i
        # a ligature group = run of zero-width chars + the following char
        while j < n and (chars[j]['bbox'][2] - chars[j]['bbox'][0]) == 0:
            j += 1
        if j > i and j < n:
            grp = chars[i:j+1]
            out.extend(reversed([c['c'] for c in grp]))
            i = j + 1
        else:
            out.append(chars[i]['c'])
            i += 1
    return ''.join(out)

def page_text(page):
    rd = page.get_text('rawdict')
    lines = []
    for b in rd['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            spans = []
            for s in l['spans']:
                t = fix_span(s['chars'])
                if t.strip():
                    spans.append((s['bbox'][0], s['bbox'][2], t))
            if not spans:
                continue
            spans.sort(key=lambda x: -x[0])          # RTL: rightmost span first
            txt = ''.join(s[2] for s in spans)
            lines.append((l['bbox'][1], l['bbox'][0], txt))
    lines.sort(key=lambda x: (round(x[0], 1), -x[1]))
    return '\n'.join(l[2] for l in lines)

d = pymupdf.open('book/REFRENCE.pdf')
parts = []
for i in range(d.page_count):
    t = page_text(d[i])
    t = re.sub('\ufffd+', '', t)
    t = t.replace('\uf081', ' [صورة]').replace('\uf082', ' [صورة]')
    t = t.replace('\u2009', ' ').replace('\u2005', ' ').replace('\u200a', ' ').replace('\xa0', ' ')
    t = t.replace('\x08', '')
    t = re.sub(r'[ \t]+', ' ', t)
    parts.append('\n\n===== PAGE %d =====\n%s' % (i + 1, t.strip()))
open('work/clean.txt', 'w', encoding='utf-8').write(''.join(parts))
print('ok')
