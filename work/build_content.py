# -*- coding: utf-8 -*-
"""Build content/{ar,en}/sections/*.md from book/Ref.clean.md and content/en/book.md.

Sections are paired by slug and order so /ar/<slug> and /en/<slug> come from the same key.
PDF page markers are stripped; where a marker split a sentence across a page break, the
paragraph is rejoined — but only across a marker, and never through an image caption.
"""
import re, os, json, glob

SLUGS = [
    ("حارة العقر", "harat-al-aqur", "Harat Al Aqur"),
    ("قلعة نزوى الشهباء", "nizwa-fort", "Nizwa Fort — Al Qal'a Al Shahba"),
    ("حصن نزوى", "nizwa-castle", "Nizwa Castle"),
    ("مسجد الشواذنة", "shawadhna-mosque", "Al Shawadhna Mosque"),
    ("مسجد مزارعة", "mazaraa-mosque", "Mazara'a Mosque"),
    ("جامع نزوى ومركز التعريف بالإسلام", "nizwa-friday-mosque",
     "The Friday Mosque of Nizwa and the Islam Information Centre"),
    ("نزل نزوى التراثية", "nizwa-heritage-inn", "Nizwa Heritage Inn"),
    ("سور العقر", "al-aqur-wall", "The Al Aqur Wall"),
    ("البيت العماني في حارة العقر", "the-omani-house", "The Omani house in Harat Al Aqur"),
    ("حارة العقر في حكم دولة اليعاربة", "under-the-yaariba", "Harat Al Aqur under the Ya'ariba"),
    ("الأبواب والأسقف", "doors-and-ceilings", "Doors and ceilings"),
    ("مدارس تعليم القران الكريم", "quran-schools", "Qur'an schools"),
    ("المجالس", "the-sablahs", "The *sablahs*"),
    ("بيت الصاروج", "bait-al-sarooj", "Bait Al Sarooj"),
    ("شعار نزوى عاصمة الثقافة الإسلامية", "capital-of-islamic-culture",
     "The emblem of Nizwa, Capital of Islamic Culture"),
    ("تنور مزارعة", "mazaraa-oven", "The Mazara'a oven"),
    ("قبر الشيخ الأصم", "sheikh-al-asamm", "The grave of Sheikh Al Asamm"),
    ("مقبرة الفرس", "persians-graveyard", "The Persians' graveyard"),
    ("مستشفى الطبيب تومس", "thoms-hospital", "Dr Thoms's hospital"),
    ("قنوات تصريف المياه", "drainage-channels", "The water drainage channels"),
    ("السيارات السياحية", "tourist-buggies", "The tourist buggies"),
    ("الأوقاف", "the-awqaf", "The endowments (*awqaf*)"),
    ("مجرى الأودية", "the-wadis", "The wadi courses"),
    ("فلج ضوت", "falaj-dawt", "Falaj Dawt"),
    ("الآبار", "the-wells", "The wells"),
    ("احتفالات عيدي الفطر والأضحى", "the-two-eids", "The Eid al-Fitr and Eid al-Adha celebrations"),
    ("متحف أبي المؤثر", "abu-al-muthir-museum", "Abu Al Mu'thir Museum"),
    ("ساعة المدة", "saat-al-mudda", "The *sa'at al-mudda* — the time clock"),
    ("سوق نزوى", "nizwa-souq", "Nizwa Souq"),
    ("مطعم العقر التراثي", "al-aqur-restaurant", "Al Aqur Heritage Restaurant"),
]
AR_BY_TITLE = {ar: (slug, en) for ar, slug, en in SLUGS}

MARKER = re.compile(r"^<!-- PDF page \d+ -->$")

# The book's closing pages (شكر وتقدير, الخاتمة, الفهرس) carry no heading in the PDF
# glyph stream, so split_headings() leaves them under the last section - which put
# the author's acknowledgements inside the restaurant entry. They are lifted out
# by their opening words and written to content/ar/back-matter/ instead.
BACK_MATTER = (
    ("acknowledgements", "شكر وتقدير", "شكراً من القلب"),
    ("afterword", "الخاتمة", "بحمد الله وتوفيقه"),
)
# The printed index is a run of title/page-number pairs. It is a page-number
# artefact of the paper book, and the site has its own navigation, so it is dropped.
TOC_OPENER = "المقدمة 5"
ENDS_SENTENCE = (".", "؟", "!", "؛", ":", "»", '"')
CAPTION = ("[صورة]", "[image]")


def is_caption(t):
    return t.lstrip().startswith(CAPTION)


def clean_title(s):
    return s.replace("*", "").strip()


def split_headings(text, level="## "):
    out, title, buf = [], None, []
    for line in text.split("\n"):
        if line.startswith(level):
            if title is not None:
                out.append((title, "\n".join(buf)))
            title, buf = line[len(level):].strip(), []
        elif title is not None:
            buf.append(line)
    if title is not None:
        out.append((title, "\n".join(buf)))
    return out


def strip_markers(body):
    """Drop page markers; rejoin only sentences the marker itself broke."""
    blocks, cur = [], []
    for line in body.split("\n"):
        if MARKER.match(line.strip()):
            if cur:
                blocks.append(("para", " ".join(cur).strip())); cur = []
            blocks.append(("marker", ""))
            continue
        if not line.strip():
            if cur:
                blocks.append(("para", " ".join(cur).strip())); cur = []
        else:
            cur.append(line.strip())
    if cur:
        blocks.append(("para", " ".join(cur).strip()))

    out, pending_marker = [], False
    for kind, text in blocks:
        if kind == "marker":
            pending_marker = True
            continue
        if not text:
            continue
        # two captions can share a source line; give each its own block
        if is_caption(text) and text.count("[صورة]") + text.count("[image]") > 1:
            parts = re.split(r"(?=\[صورة\]|\[image\])", text)
            for part in (x.strip() for x in parts):
                if part:
                    out.append(part)
            pending_marker = False
            continue
        if (pending_marker and out
                and not is_caption(text) and not is_caption(out[-1])
                and not out[-1].rstrip().endswith(ENDS_SENTENCE)):
            out[-1] = out[-1].rstrip() + " " + text
        else:
            out.append(text)
        pending_marker = False
    return out


def split_back_matter(blocks):
    """Separate the book's closing pages from the last section's own text."""
    entry, back = [], {}
    for b in blocks:
        for key, title, opener in BACK_MATTER:
            if b.startswith(opener):
                back[key] = (title, b)
                break
        else:
            if not b.startswith(TOC_OPENER):
                entry.append(b)
    return entry, back


def write_back_matter(back):
    d = "content/ar/back-matter"
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(d + "/*.md"):
        os.remove(f)
    for key, (title, text) in back.items():
        fm = "---\nslug: %s\nlang: ar\ntitle: %s\n---\n\n" % (key, title)
        open("%s/%s.md" % (d, key), "w", encoding="utf-8").write(fm + text + "\n")
    return sorted(back)


def write(slug, lang, title, blocks, order):
    fm = "---\nslug: %s\nlang: %s\ntitle: %s\norder: %d\n---\n\n" % (slug, lang, title, order)
    path = "content/%s/sections/%02d-%s.md" % (lang, order, slug)
    open(path, "w", encoding="utf-8").write(fm + "\n\n".join(blocks).strip() + "\n")


for d in ("content/ar/sections", "content/en/sections"):
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(d + "/*.md"):
        os.remove(f)

ar_raw = open("book/Ref.clean.md", encoding="utf-8").read()
ar_body = ar_raw[ar_raw.index("<!-- PDF page 3 -->"):]
ar_sections = split_headings(ar_body)
en_sections = {clean_title(t): b for t, b in
               split_headings(open("content/en/book.md", encoding="utf-8").read())}
foreword_ar = ar_body[:ar_body.index("\n## ")]

index = []
write("foreword", "ar", "المقدمة", strip_markers(foreword_ar), 0)
write("foreword", "en", "Foreword", strip_markers(en_sections["Foreword"]), 0)
index.append({"slug": "foreword", "order": 0, "ar": "المقدمة", "en": "Foreword"})

order, missing, back_written = 0, [], []
for ar_title, ar_text in ar_sections:
    if ar_title not in AR_BY_TITLE:
        continue
    order += 1
    slug, en_title = AR_BY_TITLE[ar_title]
    en_text = en_sections.get(clean_title(en_title))
    if en_text is None:
        missing.append(en_title); en_text = ""
    ar_blocks = strip_markers(ar_text)
    if slug == "al-aqur-restaurant":
        ar_blocks, back = split_back_matter(ar_blocks)
        back_written = write_back_matter(back)
    write(slug, "ar", ar_title, ar_blocks, order)
    write(slug, "en", clean_title(en_title), strip_markers(en_text), order)
    index.append({"slug": slug, "order": order, "ar": ar_title, "en": clean_title(en_title)})

json.dump(index, open("content/sections.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("paired sections: %d" % len(index))
print("back matter lifted out of the last entry:", back_written or "none")
print("unmatched EN:", missing or "none")
print("files still holding a marker:",
      [p for p in glob.glob("content/*/sections/*.md") if "PDF page" in open(p, encoding="utf-8").read()] or "none")
