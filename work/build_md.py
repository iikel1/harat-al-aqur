# -*- coding: utf-8 -*-
"""Rebuild a readable book/Ref.clean.md from book/REFRENCE.pdf.

The shipped docs/archive/Ref.md came from an extractor that dumped the PDF's visual glyph
order, so every line was mirrored and every lam-alef ligature was mangled.
This rebuilds from the glyph stream instead:
  * ligature glyphs (runs of zero-width chars) are un-reversed
  * lam-alef ligatures that ToUnicode flattened to a bare wide alef get their lam back
  * chars are re-sorted right-to-left, latin/digit runs flipped back to LTR
  * the U+00C9 kashida artifact and the trailing U+FFFD block are dropped
  * lines are regrouped into columns and paragraphs
"""
import pymupdf, re

ALNUM = re.compile(r"[0-9A-Za-z]")
CONT = set(".,/-:'’()&")

TITLES = [
    "حارة العقر", "قلعة نزوى الشهباء", "حصن نزوى", "مسجد الشواذنة",
    "مسجد مزارعة", "جامع نزوى ومركز التعريف بالإسلام", "نزل نزوى التراثية",
    "سور العقر", "البيت العماني في حارة العقر", "حارة العقر في حكم دولة اليعاربة",
    "الأبواب والأسقف", "مدارس تعليم القران الكريم", "المجالس", "بيت الصاروج",
    "شعار نزوى عاصمة الثقافة الإسلامية", "تنور مزارعة", "قبر الشيخ الأصم",
    "مقبرة الفرس", "مستشفى الطبيب تومس", "قنوات تصريف المياه",
    "السيارات السياحية", "الأوقاف", "مجرى الأودية", "فلج ضوت", "الآبار",
    "احتفالات عيدي الفطر والأضحى", "متحف أبي المؤثر", "ساعة المدة",
    "سوق نزوى", "مطعم العقر التراثي",
]


def norm(s):
    return re.sub(r"\s+", " ", s.replace("ـ", "")).strip()


def line_text(line):
    items = []
    for s in line["spans"]:
        size = s["size"] or 1
        cs = [c for c in s["chars"] if c["c"] != "É"]
        n, i = len(cs), 0
        while i < n:
            j = i
            while j < n and (cs[j]["bbox"][2] - cs[j]["bbox"][0]) == 0:
                j += 1
            if j > i and j < n:                       # one ligature glyph -> many chars
                grp = [c["c"] for c in cs[i:j + 1]]
                base = cs[j]["bbox"][0]
                if grp[-1].isspace():
                    # a space glyph cannot really encode letters: overset/hidden text
                    grp = [grp[-1]]
                elif len(grp) == 2 and set(grp) & {"ل"} and set(grp) & set("اأإآ"):
                    grp = ["ل", next(c for c in grp if c != "ل")]   # lam-alef, always in this order
                else:
                    grp = list(reversed(grp))
                m = len(grp)
                for k, ch in enumerate(grp):
                    items.append((base + (m - k) * 0.001, ch, 0.0, True))
                i = j + 1
            else:
                c = cs[i]
                items.append((c["bbox"][0], c["c"], (c["bbox"][2] - c["bbox"][0]) / size, False))
                i += 1
    items.sort(key=lambda t: -t[0])

    out, prev_lig = [], False
    for _, ch, w, lig in items:
        if ch == "ا" and w > 0.45 and not (prev_lig and out and out[-1] == "ل"):
            out.append("ل")                      # ligature lost its lam
        out.append(ch)
        prev_lig = lig

    res, buf = [], []
    for ch in out:
        if ALNUM.match(ch) or (buf and ch in CONT):
            buf.append(ch)
        else:
            if buf:
                res.extend(reversed(buf)); buf = []
            res.append(ch)
    res.extend(reversed(buf))
    txt = "".join(res)
    # latin phrases also come out with their words in reverse order
    return re.sub(r"[A-Za-z][A-Za-z0-9'’()&,.\- ]{3,}",
                  lambda m: " ".join(reversed(m.group(0).split())), txt)


def scrub(t):
    t = re.sub("�+", "", t)
    t = t.replace("", "[صورة]").replace("", "[صورة]")
    for sp in (" ", " ", " ", "\xa0"):
        t = t.replace(sp, " ")
    return re.sub(r"[ \t]+", " ", t.replace("\x08", "")).strip()


def page_lines(page):
    """[(text, x0, x1, y0)] for every text line on the page."""
    out = []
    for b in page.get_text("rawdict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            t = scrub(line_text(l))
            if t and not t.isdigit():                 # drop printed folio numbers
                x0, y0, x1, _ = l["bbox"]
                out.append((t, x0, x1, y0))
    return out


def columns(lines):
    """Group lines into columns, ordered right-to-left; each column top-to-bottom."""
    cols = []
    # seed from the widest lines: a short trailing line must not start its own column
    for ln in sorted(lines, key=lambda r: (-(r[2] - r[1]), -r[1])):
        for c in cols:
            lo, hi = max(c["x0"], ln[1]), min(c["x1"], ln[2])
            if hi - lo > 0.5 * min(c["x1"] - c["x0"], ln[2] - ln[1]):
                c["lines"].append(ln)
                c["x0"] = min(c["x0"], ln[1])
                c["x1"] = max(c["x1"], ln[2])
                break
        else:
            cols.append({"x0": ln[1], "x1": ln[2], "lines": [ln]})
    cols.sort(key=lambda c: -c["x1"])
    for c in cols:
        c["lines"].sort(key=lambda r: r[3])
    return cols


# Residual ToUnicode artifacts the geometric rules cannot resolve; each was
# checked against the rendered page.
# Where a real lam glyph is followed by a wide alef, the alef is sometimes a plain
# final alef (justification broke the ligature) and sometimes the lam-alef ligature
# itself. The two are identical in width, so the rule over-inserts a lam in a handful
# of words. Every case was found by scanning all words containing "لل".
CORRECTIONS = {
    "الإسللام": "الإسلام",
    "أسللاف": "أسلاف",
    "القللاع": "القلاع",
    "بإصللاح": "بإصلاح",
    "خللال": "خلال",
    "فللا ": "فلا ",
    "مللاك": "ملاك",
    "وظللام": "وظلام",
    "رجًللا": "رجلاً",
    "جمالا وإيضاحاً": "جمالاً وإيضاحاً",
    "عاملا إيجابياً": "عاملاً إيجابياً",
}


TITLESET = {norm(x) for x in TITLES}
doc = pymupdf.open("book/REFRENCE.pdf")

pages = []
for i in range(doc.page_count):
    blocks = []
    for col in columns(page_lines(doc[i])):
        width = max((r[2] - r[1]) for r in col["lines"])
        para = []
        for t, x0, x1, _ in col["lines"]:
            if norm(t) in TITLESET:
                if para:
                    blocks.append(("p", " ".join(para))); para = []
                blocks.append(("h", norm(t)))
                continue
            para.append(t)
            if (x1 - x0) < 0.86 * width or t.endswith((".", "؟", "!", ":")):
                blocks.append(("p", " ".join(para))); para = []
        if para:
            blocks.append(("p", " ".join(para)))
    pages.append(blocks)

md = [
    "# حارة العقر — ولاية نزوى",
    "",
    "> نص كتاب *حارة العقر* لسليمان بن محمد السليماني، مستخرج من `REFRENCE.pdf`",
    "> (مكتبة خزائن الآثار، بركاء ـ سلطنة عُمان، 1442هـ / 2021م، ISBN 978-9933-29-448-9).",
    "> أُعيد ترتيب النص من مجرى الحروف في الملف، فقد كان الاستخراج السابق معكوساً.",
    "> **ملاحظة:** التشكيل في مقاطع الشعر غير موثوق، والصور غير مستخرجة (أُشير إليها بـ `[صورة]`).",
    "",
]
for pno, blocks in enumerate(pages, 1):
    if not blocks:
        continue
    md.append("<!-- PDF page %d -->" % pno)
    md.append("")
    for kind, text in blocks:
        md.append(("## " + text) if kind == "h" else text)
        md.append("")

text = "\n".join(md)
for bad, good in CORRECTIONS.items():
    text = text.replace(bad, good)
open("book/Ref.clean.md", "w", encoding="utf-8").write(text)
print("wrote book/Ref.clean.md")
