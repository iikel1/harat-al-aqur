# -*- coding: utf-8 -*-
"""Extract every embedded photo from book/REFRENCE.pdf into assets/photos/,
and write a catalogue mapping each file to its PDF page, book section and caption."""
import pymupdf, json, os, re, collections

os.makedirs("assets/photos", exist_ok=True)

# --- page -> section, derived from the recovered text ---------------------
clean = open("book/book/Ref.clean.md", encoding="utf-8").read()
page_section, page_captions = {}, collections.defaultdict(list)
current, page = "أمامية", 0
for line in clean.split("\n"):
    m = re.match(r"<!-- PDF page (\d+) -->", line)
    if m:
        page = int(m.group(1))
        page_section[page] = current
        continue
    if line.startswith("## "):
        current = line[3:].strip()
        page_section[page] = current
    elif "[صورة]" in line:
        cap = line.replace("[صورة]", "").strip()
        if cap:
            page_captions[page].append(cap)
last = "أمامية"
for p in range(1, 66):
    if p in page_section:
        last = page_section[p]
    else:
        page_section[p] = last

# --- extract ---------------------------------------------------------------
doc = pymupdf.open("book/REFRENCE.pdf")
seen, catalogue = {}, []
for pno in range(doc.page_count):
    page = doc[pno]
    imgs = page.get_images(full=True)
    # order by placement, top-left first
    placed = []
    for img in imgs:
        try:
            rects = page.get_image_rects(img[0])
        except Exception:
            rects = []
        r = rects[0] if rects else None
        placed.append((r.y0 if r else 9e9, r.x0 if r else 9e9, img, r))
    placed.sort(key=lambda t: (t[0], t[1]))

    for idx, (_, _, img, rect) in enumerate(placed, 1):
        xref = img[0]
        if xref in seen:
            catalogue.append({**seen[xref], "also_on_page": pno + 1})
            continue
        info = doc.extract_image(xref)
        w, h, ext = info["width"], info["height"], info["ext"]
        mp = w * h / 1e6
        kind = "photo" if mp >= 0.10 else "decor"
        name = "p%02d-%d.%s" % (pno + 1, idx, ext)
        with open(os.path.join("assets/photos", name), "wb") as f:
            f.write(info["image"])
        rec = {
            "file": name,
            "pdf_page": pno + 1,
            "section": page_section.get(pno + 1, ""),
            "width": w, "height": h, "megapixels": round(mp, 2),
            "bytes": len(info["image"]),
            "kind": kind,
            "placed_w_pt": round(rect.width, 1) if rect else None,
            "placed_h_pt": round(rect.height, 1) if rect else None,
            "full_bleed": bool(rect and rect.width > 700),
            "page_captions": page_captions.get(pno + 1, []),
        }
        seen[xref] = rec
        catalogue.append(rec)

json.dump(catalogue, open("assets/photos/catalogue.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

photos = [c for c in catalogue if c.get("kind") == "photo"]
decor = [c for c in catalogue if c.get("kind") == "decor"]
print("extracted %d files (%d photos, %d decorative)" % (len(seen), len(photos), len(decor)))
print("hero-capable (>=1.0 MP): %d" % len([c for c in photos if c["megapixels"] >= 1.0]))
print("full-bleed placements: %d" % len([c for c in photos if c["full_bleed"]]))
