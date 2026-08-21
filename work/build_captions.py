# -*- coding: utf-8 -*-
"""Build content/data/captions.json — the book's photo captions, paired to its photographs.

The Arabic is taken byte-exact from assets/photos/catalogue.json (`page_captions`,
which extract_photos.py reads off each page). The English is reviewed data, held
in EN_CAPTIONS below, because three things make automatic pairing unsafe:

  1. page 24 — a 574-character run of body text is misdetected as a caption by
     extract_photos.py, because the caption and the column text share a band.
  2. page 47 — two captions are run together into one string, separated only by a
     double space.
  3. page 34 — the book prints two sablah photographs side by side. Arabic reads
     them right-to-left, the translation lists them left-to-right, so the two
     captions appear in OPPOSITE order in the two languages. Pairing by position
     would label each photograph with the other one's name.

Because of (3) the English here is keyed to the Arabic explicitly, never by index.

Scope: a caption is bound to a single photograph only where its page holds exactly
one photograph and one caption. The book routinely prints three or four
photographs to a page under one caption, and nothing in the extraction records
which photograph a caption sits beneath — so elsewhere the caption labels the
page's group. Do not narrow a group caption to one file by guessing.

Run:  python work/build_captions.py
"""
import json
import datetime

CATALOGUE = 'assets/photos/catalogue.json'
OUT = 'content/data/captions.json'

# Captions dropped as not being captions at all, as (page, exact prefix).
NOT_A_CAPTION = [(24, 'مترين ويزيد من متانته')]

# Captions that arrived as one string and are two, as (page, separator).
SPLIT = [(47, '  ')]

# The reviewed English, keyed by the Arabic it translates.
EN_CAPTIONS = {
    'قلعة نزوى 1902م': 'Nizwa Fort, 1902',
    'صورة قديمة لجامع نزوى': 'An old photograph of the Friday Mosque of Nizwa',
    'نزل نزوى التراثية': 'Nizwa Heritage Inn',
    'صور قديمة لمكتب نزل نزوى التراثية': 'Old photographs of the Nizwa Heritage Inn office',
    'صباح أبي المؤثر': "Sabah Abi Al Mu'thir",
    'صباح السوق': 'Sabah Al Souq',
    'صباح وبرج الشجبي': 'Sabah and the Al Shajbi Tower',
    'صباح وبرج الصبخة من الشرق والغرب': 'Sabah and the Al Sabkha Tower, from east and west',
    'واجهة سوق نزوى ويظهر سور العقر ببنائه الحديث':
        'The frontage of Nizwa Souq, with the Al Aqur Wall in its modern rebuilding',
    'صورة للسور من برج المذبحة ويظهر في الصورة فلج ضوت':
        'The wall seen from Al Mathbaha Tower, with Falaj Dawt visible',
    'مدرسة الجليلين': 'Al Jalilain School',
    # Deliberately keyed by name, not position — see (3) in the docstring.
    'سبلة النيري': 'Sablat Al Nairi',
    'سبلة الكوارج': 'Sablat Al Kawarij',
    'نموذج لعملية دفن الشواء': 'The burial of the shuwa',
    'صورة قديمة من منطقة سعال لجرفة 82 التاريخية':
        "An old photograph from the Sa'al area, of the historic Jurfa 82",
    'قبر الإمام الوارث بن كعب الخروصي': "The grave of Imam Al Warith bin Ka'b Al Kharusi",
    'فلج دارس': 'Falaj Daris',
    'فلج ضوت': 'Falaj Dawt',
    'نموذج للأبار: الأولى موجودة بداخل إحدى البيوت دائرية الشكل يصل قطرها إلى متر واحد، والأخرى إحدى آبار المزارع مربعية الشكل يصل قطرها 4.5 متر ويظهر جليا الصف العجيب في الحجارة والتي يصل وزن الحجر الواحد منها أكثر من 40 كيلو جرام.':
        'Two well types: the first, inside one of the houses, is circular and about one metre '
        'across; the other, a farm well, is squared and about 4.5 metres across. The remarkable '
        'coursing of the stone is clearly visible — single stones weighing more than 40 kilograms.',
    'صورة ليلية لسوق نزوى': 'Nizwa Souq at night',
    'صورة قديمة لسوق الصنصرة من الباب الغربي':
        'An old photograph of the Al Sansara souq from the western door',
}


# Figures the book prints WITHOUT a caption but which can be identified with
# certainty, so they are not left anonymous. Keep this list short and evidenced:
# each entry needs a reason recorded here, not a guess from the picture alone.
EXTRA = {
    # The plan of the wall. The acknowledgements credit its preparation to
    # Dr Al Walid bin Zahir Al Salmi; the image is unmistakably that plan -
    # the full circuit with its towers, its gates and a north arrow.
    'p23-1.jpeg': {
        'ar': 'مخطط سور العقر — إعداد الدكتور الوليد بن زاهر السالمي',
        'en': 'The plan of the Al Aqur Wall — prepared by Dr Al Walid bin Zahir Al Salmi',
    },
}


def clean(page, captions):
    """Apply the three documented repairs to one page's raw captions."""
    out = []
    for c in captions:
        c = c.strip()
        if any(page == p and c.startswith(prefix) for p, prefix in NOT_A_CAPTION):
            continue
        parts = [c]
        for p, sep in SPLIT:
            if page == p and sep in c:
                parts = [x.strip() for x in c.split(sep) if x.strip()]
        for part in parts:
            if part and part not in out:  # the book repeats a caption across a spread
                out.append(part)
    return out


def main():
    catalogue = json.load(open(CATALOGUE, encoding='utf-8'))

    pages = {}
    for photo in catalogue:
        page = pages.setdefault(photo['pdf_page'], {'photos': [], 'raw': photo.get('page_captions') or []})
        page['photos'].append(photo['file'])

    result, missing = {}, []
    for page in sorted(pages):
        captions = clean(page, pages[page]['raw'])
        if not captions:
            continue
        photos = sorted(pages[page]['photos'])
        entries = []
        for ar in captions:
            en = EN_CAPTIONS.get(ar)
            if en is None:
                missing.append((page, ar))
            entries.append({'ar': ar, 'en': en or ''})
        # One photograph, one caption is the only case where the pairing is certain.
        scope = 'photo' if len(photos) == 1 and len(entries) == 1 else 'group'
        result[str(page)] = {'scope': scope, 'photos': photos, 'captions': entries}

    # Identified figures that the book leaves uncaptioned.
    by_file = {photo['file']: photo for photo in catalogue}
    for file, cap in EXTRA.items():
        photo = by_file.get(file)
        if not photo:
            print('EXTRA refers to a missing file:', file)
            continue
        page = str(photo['pdf_page'])
        if page in result:
            print('EXTRA collides with a page that already has captions:', page)
            continue
        result[page] = {'scope': 'photo', 'photos': [file], 'captions': [cap]}

    doc = {
        'checked': datetime.date.today().isoformat(),
        'source': 'Arabic: assets/photos/catalogue.json (page_captions, from the book). '
                  'English: reviewed translation held in work/build_captions.py. '
                  'A small number of uncaptioned figures are identified in that file too.',
        'policy': "A caption is bound to a single photograph only where scope is 'photo' - "
                  "its page holds exactly one photograph and one caption. Where scope is "
                  "'group' the caption labels every photograph on that page, because the book "
                  "prints several to a page under one caption and the extraction does not "
                  "record which photograph a caption sits beneath. Do not narrow a group "
                  "caption to one file by guessing.",
        'pages': result,
    }
    json.dump(doc, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    captioned = sum(len(p['photos']) for p in result.values())
    exact = sum(1 for p in result.values() if p['scope'] == 'photo')
    print('pages with captions: %d  (%d exact, %d group)' % (len(result), exact, len(result) - exact))
    print('photographs now carrying a caption: %d of %d' % (captioned, len(catalogue)))
    print('captions with no reviewed English:', missing or 'none')


if __name__ == '__main__':
    main()
