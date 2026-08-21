import pymupdf, re

LTR = re.compile(r'[0-9A-Za-z]')

def line_chars(line):
    items = []          # (xkey, char)
    for s in line['spans']:
        size = s['size'] or 1
        cs = [c for c in s['chars'] if c['c'] != '\u00c9']
        n = len(cs); i = 0
        while i < n:
            j = i
            while j < n and (cs[j]['bbox'][2] - cs[j]['bbox'][0]) == 0:
                j += 1
            if j > i and j < n:                       # ligature group i..j
                grp = cs[i:j+1]
                base = cs[j]['bbox'][0]
                m = len(grp)
                for k, c in enumerate(reversed(grp)):
                    items.append((base + (m - k) * 0.001, c['c'], 0.0))
                i = j + 1
            else:
                c = cs[i]
                w = (c['bbox'][2] - c['bbox'][0]) / size
                items.append((c['bbox'][0], c['c'], w))
                i += 1
    items.sort(key=lambda t: -t[0])
    # restore dropped lam in lam-alef ligatures rendered as a wide bare alef
    out = []
    for idx, (x, ch, w) in enumerate(items):
        if ch == '\u0627' and w > 0.45:
            prev = out[-1] if out else ''
            if prev != '\u0644':
                out.append('\u0644')
        out.append(ch)
    # un-reverse latin/digit runs
    res = []; buf = []
    for ch in out:
        if LTR.match(ch) or (buf and ch in '.,/-:'):
            buf.append(ch)
        else:
            if buf:
                res.extend(reversed(buf)); buf = []
            res.append(ch)
    if buf:
        res.extend(reversed(buf))
    return ''.join(res)

def page_text(page):
    rd = page.get_text('rawdict')
    blocks = [b for b in rd['blocks'] if b['type'] == 0]
    outl = []
    for b in blocks:
        for l in b['lines']:
            t = line_chars(l)
            if t.strip():
                outl.append(t.rstrip())
        outl.append('')
    return '\n'.join(outl)

d = pymupdf.open('book/REFRENCE.pdf')
parts = []
for i in range(d.page_count):
    t = page_text(d[i])
    t = re.sub('\ufffd+', '', t)
    t = t.replace('\uf081', ' [صورة]').replace('\uf082', ' [صورة]')
    for sp in ('\u2009', '\u2005', '\u200a', '\xa0'):
        t = t.replace(sp, ' ')
    t = t.replace('\x08', '')
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    parts.append('\n\n===== PAGE %d =====\n%s' % (i + 1, t.strip()))
open('work/clean2.txt', 'w', encoding='utf-8').write(''.join(parts))
print('ok')
