# حارة العقر / Harat Al-Aqr, Nizwa — full dossier

Everything gathered on the Al-Aqr quarter of Nizwa: the source book in this repo, what it
says, what has happened to the quarter since it was written, and what the quarter contains
today.

Compiled 20 August 2026. Ratings, prices and project figures are a snapshot at that date.

**Contents**

1. [The source material](#1-the-source-material)
2. [What the book says](#2-what-the-book-says)
3. [The restoration programme, 2016–2026](#3-the-restoration-programme-20162026)
4. [What Harat Al-Aqr contains today](#4-what-harat-al-aqr-contains-today)
5. [Discrepancies and open questions](#5-discrepancies-and-open-questions)
6. [Sources](#6-sources)
7. [Appendix A — full Arabic text of the book](#appendix-a--full-arabic-text-of-the-book)

---

## 1. The source material

| File | What it is |
|---|---|
| `REFRENCE.pdf` | 65-page illustrated book, *حارة العقر* by **سليمان بن محمد السليماني**. Adobe InDesign CS5.5, created 11 Nov 2020. Publisher مكتبة خزائن الآثار (بركاء، عُمان), 1442 AH / 2021 CE, ISBN 978-9933-29-448-9. |
| `Ref.md` | **Broken.** A text dump of the PDF in *visual* glyph order — every line mirrored, ligatures mangled. Not usable as text. |
| `Ref.clean.md` | Rebuilt by `work/build_md.py` straight from the PDF glyph stream. ~35 k chars, 30 sections. Reproduced in full as [Appendix A](#appendix-a--full-arabic-text-of-the-book). |
| `AL-AQR.md` | This document. |

### Why `Ref.md` is broken, and how the clean text was recovered

The PDF stores Arabic in logical order but with a font whose `ToUnicode` table is lossy.
Whatever produced `Ref.md` read glyph positions instead of the character stream, so:

- every line came out reversed — `ةظوفحم قوقحلا عيمج` for `جميع الحقوق محفوظة`
- lam-alef ligatures were flattened or transposed — `الإسلام` became `اإلسام`
- U+00C9 `É` appears 1 334× as a justification-kashida artifact, *inside* words
- 2 988 consecutive U+FFFD on the last page

`work/build_md.py` repairs this geometrically rather than by guessing:

1. A glyph mapping to several characters emits them with **zero width** except one. Those
   runs are one ligature, reassembled in logical order. Lam-alef pairs are always emitted
   ل-then-alef, since a lam-alef ligature cannot mean anything else.
2. A lam-alef ligature whose `ToUnicode` collapsed to a bare alef appears as an alef of
   width > 0.45 em (a normal alef is ≈ 0.2 em). Its lam is restored.
3. A "space" glyph carrying letter characters is overset/hidden text and is dropped.
4. Characters are re-sorted right-to-left; Latin and digit runs are flipped back to LTR.
   This is what puts `سنة 1650م` back where it belongs instead of at the line start, and
   what turns the wall-map legend's `Tower ah'Alqal` back into `Alqal'ah Tower`.
5. Lines are regrouped into columns — several pages are two-column — and into paragraphs.

**Residual imperfections**, all flagged in the file header: poetry diacritics on PDF pages
13 and 32 are scrambled beyond geometric repair; the Qur'anic verse on page 17 is set in a
private-use font and comes out as `ﮙ ﮚ ﮛ…`; photographs are not extracted, marked
`[صورة]`; four words are hand-corrected against the rendered page (the `CORRECTIONS` map).

### Book structure (30 sections)

المقدمة · حارة العقر · قلعة نزوى الشهباء · حصن نزوى · مسجد الشواذنة · مسجد مزارعة ·
جامع نزوى ومركز التعريف بالإسلام · نزل نزوى التراثية · سور العقر · البيت العماني في حارة
العقر · حارة العقر في حكم دولة اليعاربة · الأبواب والأسقف · مدارس تعليم القرآن الكريم ·
المجالس · بيت الصاروج · شعار نزوى عاصمة الثقافة الإسلامية · تنور مزارعة · قبر الشيخ الأصم
· مقبرة الفرس · مستشفى الطبيب تومس · قنوات تصريف المياه · السيارات السياحية · الأوقاف ·
مجرى الأودية · فلج ضوت · الآبار · احتفالات عيدي الفطر والأضحى · متحف أبي المؤثر · ساعة
المدة · سوق نزوى · مطعم العقر التراثي

The author states in the conclusion that the book was written as a **tourist guide**
(`مرشدًا سياحيًا`), deliberately short, and was to appear in **nine languages** with
per-language additions on historic ties between Oman and the target country.

---

## 2. What the book says

### Dates

| Date | Event |
|---|---|
| pre-Islam | Al-Aqr already settled (the author's reading of the site evidence) |
| 9 AH | **مسجد الشواذنة** built — "the second mosque built in Oman" |
| 2nd c. AH (~1200 yrs) | **حصن نزوى** begun under Imam محمد بن عبد الله بن أبي عفان; **جامع نزوى** founded on Wadi Kalbuh |
| 3rd c. AH | **مسجد مزارعة** built; fort extended under Imam الصلت بن مالك الخروصي |
| 7th c. AH | الشيخ الأصم — أبو عبد الله عثمان بن عبد الله بن أحمد العزري |
| 853 AH | flood destroys the older Al-Aqr wall |
| 936 AH | mihrab of مسجد الشواذنة carved and signed |
| 1650 CE | Imam **سلطان بن سيف اليعربي** expels the Portuguese; Nizwa Fort funded from the Diu campaign booty, 12 years to build |
| 2nd half 11th c. AH | present **سور العقر** founded by Imam سلطان بن سيف, 7 years to build |
| 1 Dhu al-Hijja 1150 AH | ~4 000 Persian troops enter Nizwa, ambushed inside the quarter → **مقبرة الفرس** |
| 1902 | dated photograph of Nizwa Fort |
| 1950s (implied) | British air-force rockets hit the fort; "only slight" damage |
| 1992 | Nizwa Souq wins a best-architectural-design award |
| 2003 | مسجد الشواذنة restored by وزارة التراث |
| 2015 | Nizwa is Capital of Islamic Culture; commemorative tower built at the souq front |
| 1 Dhu al-Qa'da 1439 / 23 Apr 2018 | **نزل نزوى التراثية** opened by the Wali of Nizwa, الشيخ حمد بن سالم بن سيف الأغبري |
| 2020 | مسجد مزارعة restored from its own waqf |

### Measurements

- **Wall (سور العقر):** ~2 km; 1.5–2 m thick; 5–6 m high; **15 towers**, 150–200 m apart;
  tower bases 4–5 m diameter, mostly cylindrical, some square.
- **Gates (صباح):** four — أبي المؤثر (S), الشجبي (W), السوق (NE), الصبخة (E).
  **صباح السوق was demolished** during fort/souq restoration; only photographs survive.
- **Towers named:** المذبحة، ميرزة (بستان قسام)، بلج، خريص بلج، العلياء، غوير، الكوارج،
  محمود، السوق، القلعة، بستان العقر الشرقي/الغربي (سكة القبر)، الصبخة، قطعة الطوي،
  حارة الزامة الشرقي/الغربي. Wall map drawn by د. الوليد بن زاهر السالمي.
- **Houses:** 300+, 60–200 m². Five sub-quarters, each with a مجلس/سبلة — سبلة الكوارج and
  سبلة النيري are named. Ground floor: مجلس, bedrooms, دهليز, a date store called النضد,
  a washroom called الشروني, and a well. Fittings: الموقعة (grain-grinding stone), جحلة
  (water jar), خرس (pottery), مناديس (chests), روازن (wall niches). Doors carved wood,
  ceilings palm trunks, windows with four openings so the upper lights open alone.
- **Wells:** house wells < 1 m diameter; farm wells 3–4 m wide, up to 20 m deep.
- **Waqf:** ~70 distinct types of endowment in Al-Aqr alone.
- **ساعة المدة:** a sundial for falaj shares. الأثر = ½ hour, نصف أثر = ¼ hour, ربع أثر =
  7½ minutes; night shares measured with **السحلة**, a pierced copper vessel floated in a
  full jar; administered by **عريف الفلج**. It stood in front of مدرسة الجلجلان behind
  مسجد الشواذنة and served فلج ضوت. **Now gone** — the author notes no photograph of it
  could be found.
- **Aflaj:** فلج ضوت is over 1 200 years old; types are عيني، غيلي، داوودي; فلج دارس is
  the largest and most famous in Oman, and Falaj Dawt's flow tracks it.
- **Souq:** seven sub-souqs — السوق الشرقي (الصنصرة) for spices and traditional remedies;
  سوق الفضة والحرفيين (khanjars: النزواني، السعيدي/الصافاني); سوق الذهب; سوق الأسلحة with
  a Friday auction; سوق الجمعة; سوق التمور والحلوى; and مناداة الأغنام, the Friday
  livestock auction from 07:00 lasting ~3 hours — cattle from Dhofar and North Batinah,
  sheep from Sharqiyah, Dhahirah and Wusta.

### People worth indexing

**Author** سليمان بن محمد السليماني, of قرية العقر — and, as it turns out, currently
running the quarter's endowment (see §3). **Reviewer** محمد بن عبد الله السيفي, author of
*الحلل السندسية في الكتابات المسجدية*. **Photographer** سامي بن سالم الهنائي. **Archive
photographs** علي بن أحمد القسيمي, ناصر بن محمد الفرقاني. **Wall map** د. الوليد بن زاهر
السالمي. **Director of Nizwa Heritage Inn** راشد بن عبد الله الفارسي. **Final review**
خالد بن عيسى السليماني.

Historic figures: Imams سلطان بن سيف اليعربي، الصلت بن مالك الخروصي، الوارث بن كعب
الخروصي (drowned in Wadi Kalbuh going to free prisoners from a flood)، محمد بن عبد الله
الخليلي (cured of blindness by the American Dr Thomas)؛ الشيخ سيف بن محمد الفارسي, whose
رائية is quoted؛ السيد طارق بن تيمور البوسعيدي, father of Sultan Haitham, once resident in
**بيت الصاروج**.

---

## 3. The restoration programme, 2016–2026

The book stops at 2021. Most of the story postdates it.

### Headline figures

| Figure | Value | As of |
|---|---|---|
| Heritage houses restored | **89** | Dec 2025 |
| Youth business ventures | **81+** (78 in an earlier count) | Dec 2025 |
| Direct jobs | **400+** (300+ earlier) | Dec 2025 |
| Visitors | **600 000** in Q1 alone | 2023 |
| Visitors after the wall opened | **3 000–5 000 per day** | 2024 |
| Al Dakhiliyah heritage/tourism sites | **415 081 visitors** | full-year 2024 |
| Rehabilitation began | **2017** (wall works from Jan 2020) | — |

**شركة بوارق نزوى الدولية للاستثمار** was founded in **2016 by 126 local investors** and
started by converting six buildings into inns and restaurants. It operates the inn group
(**36 rooms**) and was the first operator of electric tourist buggies in the Sultanate.

**The book's author, سليمان بن محمد السليماني, is named in the press as مدير/وكيل أوقاف
العقر** — he is not merely the quarter's chronicler but currently runs its endowment.
Useful if you need a primary contact or permissions.

Other officials to cite: الشيخ صالح بن ذياب الربيعي (Wali of Nizwa), الشيخ هلال بن سعيد
الحجري (Governor of Al Dakhiliyah), أحلام بنت حمد القصابية (Director of Heritage &
Tourism, Al Dakhiliyah), أحمد بن صالح الراشدي (Undersecretary, Ministry of Endowments),
د. إسحاق بن هلال الشرياني (adviser to the Al-Aqr waqf).

### The wall, phase by phase

Work began **January 2020** — the third major restoration in the wall's history — led by
Bawariq Nizwa with the wall's custodians. As restored: **~2 000 m, 16 towers**, running
from صباح الصبخة to برج حارة الزامة الغربي.

| Phase | Opened | Detail | Cost |
|---|---|---|---|
| 1 | 8 Jan 2024 (wall & square) | first restored stretch | **OMR 400 000** |
| 3 | Dec 2024 | 275 m, incl. a **75 m step-free accessible entrance** for wheelchairs and strollers | **OMR 370 000**, 4 months |
| 4 | 29 Dec 2025 | electric lift, tower restorations | — |

Total expected cost of the full wall restoration: **OMR 2.5–3 million**. Alongside it,
**Al Aqr Plaza** provides commercial and cultural services including VR exhibits and 3D
models. A separate **paving project** — replacing asphalt with flat stone, plus water,
sewerage and fibre — costs ~**OMR 340 000**, funded by the governorate, was 60 % complete
in Sept 2025 and is **due to finish at the end of 2026**. Al Dakhiliyah's wider heritage
package exceeds **OMR 4.5 m** across seven sites in Bidbid, Izki, Nizwa, Adam and Bahla.

### 2026

- **3 Jan** — second *مسير نزوى السياحي*, **3 000+ participants**, under the patronage of
  the Minister of Economy سعيد بن محمد الصقري, organised by the Oman Chamber of Commerce
  (Al Dakhiliyah branch) with فريق الصمود للمغامرات of Nizwa Club. The route went through
  Harat Al-Aqr and along its wall and took in **فلج ضوت** alongside Daris, Al-Ghantaq,
  Al-Khoubi and Al-Sa'ali — the same falaj the book documents.
- **12 Mar — MIPIM Awards, Cannes. Al-Aqr did *not* win.** It was shortlisted in **Best
  Urban Regeneration** (التجديد العمراني); the category went to **Nordhavn, Copenhagen**.
  Ten category winners plus a Special Jury Award (Sydney Fish Market). Al Thuraya City
  (Muscat), the other Omani finalist, also did not win. *"One of 40 finalists from 19
  countries"* is quotable; *"award-winning"* is not.
- **17 Mar** — Oman Observer feature on Omani historic quarters as tourist destinations;
  context only, no new Al-Aqr figures.
- **22–23 Apr — Shell Oman dedicates the 7th edition of *هدية شل للوطن* to Harat Al-Aqr.**
  Launched at **متحف عمان عبر الزمان** in Manah under the patronage of the Minister of
  Finance **سلطان بن سالم الحبسي**. Three pillars: restore the **remaining** stretch of
  wall plus heritage buildings and pathways; build an **integrated visitor centre**;
  connect the quarter to **solar power** (framed against Oman Vision 2040). A fourth
  strand funds entrepreneur and SME capacity building. Delivered with أوقاف عقر نزوى, the
  Governor's office and the Ministry of Heritage & Tourism. Named: **علي الجنيبي**
  (Country Chairman, Shell Oman), **د. إسحاق بن هلال الشرياني** (waqf adviser),
  **الأحنف الزبيدي** (Social Investment Manager). **No budget disclosed.**
- **May–Aug** — nothing found. Next milestones: the paving project completing at end-2026,
  and the Shell visitor centre.

---

## 4. What Harat Al-Aqr contains today

Snapshot **20 August 2026**. Ratings and review counts from Google Maps that day; prices
are indicative bands for late-August 2026 and will drift.

**Scope caveat:** Google's directory for *حارة العقر القديمة* uses a loose radius, so a few
entries sit just outside the wall (flagged ⚠). The quarter's own count is **81+ ventures**,
well above the ~32 businesses with a Maps listing — many stalls, workshops and home-based
producers are not individually listed anywhere. Treat the tables as the mapped subset, not
a census.

### Accommodation

Roughly **a dozen heritage inns**, nearly all conversions of houses inside or on the edge
of the walled quarter. Nothing above three stars; the model is the restored mud-brick
house, not the hotel.

| Inn | Rating (reviews) | Indicative rate | Notes |
|---|---|---|---|
| **IHYAA Inn — نزل إحياء** | 4.2 (384) Google · **8.2 (957) Booking**, location 9.6 | ~OMR 25 | **The former نزل نزوى التراثية / Nizwa Heritage Inn**, rebranded *إحياء* by Bawariq Nizwa; Booking's URL is still `nizwa-heritage-inn`. Six room types including shared and external bathrooms; **2 restaurants**, room service, airport shuttle, free parking/WiFi. Breakfast ~OMR 7. 3-min walk to Nizwa Fort. |
| **Antique Inn — Nizwa** | 4.2 (456) | ~OMR 18 | 3-star, **outdoor pool**, garden, terrace, tour desk, 24 h front desk, paid shuttle. 2-min walk to the fort. |
| **نزل عطره** | 4.9 (210) | ~OMR 24 | |
| **Alaqur View Inn — نزل واجهة العقر** | 4.9 (190) | ~OMR 20 | |
| **نزل البستان — AlBustan Inn** | 4.3 (285) | — | |
| **Aldar Inn — نزل الدار** | 4.5 (133) | ~OMR 28 | pool, free parking, WiFi, A/C |
| **نزل بيت المعلم** | 4.7 (76) | ~OMR 43 | 3-star |
| **نزل مزارعة التراثية / Mazarah Heritage Inn** | 4.8 (13) | ~OMR 64 | the most expensive listed |
| **Riad_Nizwa** | 4.0 (60) | ~OMR 16 | Agoda |
| **Bait Al Aqr** | — | — | Al Aqr Street, Nizwa Souq. Shared lounge, garden, BBQ, terrace. 5-min walk to the fort. |
| **بيت الحارة**, **البيت العماني للضيافة** | — | — | named in Oman Daily; no Maps presence found |
| **بيت الصاروج** | — | — | the book's grandest house, once home to Sayyid Tariq bin Taimur; converted to **10 rooms**, part of the 36-room Bawariq portfolio |

### Food and drink

Google's directory counts **11** in this category; the fuller list, with review counts as a
proxy for footfall:

| Venue | Rating (reviews) | Price | Type / hours |
|---|---|---|---|
| **أناة كافيه** | 4.6 (**1,123**) | OMR 2–4 | café, to 23:00 — busiest venue in the quarter |
| **مطعم العقر — Al Aqur Restaurant** | 3.8 (**947**) | OMR 2–10 | the book's *مطعم العقر التراثي*; Omani food, to 23:00 |
| **Tawad Cafe — تواد كافيه** | 4.9 (**926**) | OMR 2–4 | café, to 00:00 — highest-rated at scale |
| **Niz Cafe** | 4.6 (535) | OMR 2–4 | to 23:00 |
| **مطعم كوارج** | 4.5 (213) | OMR 2–4 | overlooks Nizwa Souq; opens 07:30 Fri |
| **براتا جبن العقر** | 4.7 (194) | OMR 0–2 | breakfast/paratha, to 23:30 |
| **Spaks Italian Restaurant — سباكس** | 4.3 (161) | OMR 2–4 | pizza, to 02:00 |
| **مقيل كافيه** | 4.7 (140) | OMR 2–4 | owner **سعود بن سالم الفرقاني**; traditional Omani architecture and furnishing |
| **رواق كافيه — RAWAQ CAFE** | 4.2 (138) | OMR 2–4 | |
| **Sabalat Alaqer — سبلة العقر** | 4.4 (105) | OMR 2–4 | multiple seating areas, family-friendly, view seating |
| **الشرع — فرع نزوى** | 4.5 (57) | OMR 2–4 | café / ice cream |
| **KUCU NIZWA AL AQUR** | 3.7 (27) | OMR 2–4 | chicken, to 01:00 |
| **مطعم سبلة العقر — sablah** | 5.0 (16) | OMR 0–2 | |
| **حارة العقر** (café) | 5.0 (7) | — | |
| **عربة ذرة العقر** | 4.7 (3) | — | corn cart, evenings from 16:30; reviewed as *"مشروع شباب مميز"* |
| ⚠ **سبلة العقر للمأكولات العمانية** | 3.5 (200) | OMR 2–4 | on شارع الوكالات, outside the quarter |

### Shops

Google counts **6**; only two are genuinely retail rather than cafés double-listed:

- **سوار للمجوهرات — Sewar Jewellery** — 5.0 (32), to 22:00
- **محل غيور** — 4.9 (24), to 23:00, an old-style shop kept in period character

The heavyweight retail is next door rather than inside the wall: **Nizwa Souq**, with the
seven sub-souqs the book documents.

### Sights, museums and heritage assets

| | Rating (reviews) | |
|---|---|---|
| **حارة العقر القديمة** (the quarter itself) | 4.7 (494) | open 24 h, free |
| **سور حارة العقر القديمة** (the wall) | 4.7 (231) | open 24 h; walkable along the restored stretches |
| **متحف نزوى — Nizwa Museum** | 4.8 (106) | inside the quarter; opens 08:00 |
| **متحف أبي المؤثر** | — | above صباح أبي المؤثر, on the wall itself; wall-walk plus a guard room and tower climb |
| **فلج ضوت** | 4.2 (6) | the falaj the book documents; still flowing, still on walking routes |
| **برج صباح الصبخة**, **باب الصبخة**, **مدرسة الجليلين** | — | listed heritage points |
| **Al Aqr Plaza** | — | commercial and cultural block: VR exhibits and 3D models of the quarter |
| **حاضنة أعمال هيئة تنمية المؤسسات الصغيرة والمتوسطة** | 5.0 (1) | SME incubator, Nizwa Souq — the machinery behind the 81 ventures |

Plus, from the book and still standing: **مسجد الشواذنة** (936 AH mihrab), **مسجد مزارعة**
(restored 2020), **قبر الشيخ الأصم**, **مقبرة الفرس**, **سبلة الكوارج**, **سبلة النيري**,
**تنور مزارعة**, and **جامع نزوى** with its Islam information centre — immediately
adjacent, along with **قلعة نزوى** and **حصن نزوى**.

### Activities and experiences

- **Walking the wall** — the headline attraction. Phase 3 added a **75 m step-free
  entrance** usable with wheelchairs and strollers; phase 4 added an **electric lift**.
- **Electric buggies** — open-sided, **six-seater**, run by Bawariq Nizwa, the first such
  operator in the Sultanate. Guided loops of the alleys; the book notes they run through
  the winter season.
- **VR tour** — 360° 3D headset experience in which an animated **Imam Sultan bin Saif
  al-Ya'rubi** guides you round the fort. Arabic and English, more languages in
  translation. It was built as a **digital adaptation of this very book**, by its author,
  who also floated turning it into a video game. Shown at Al Aqr Plaza and taken to
  schools, universities and exhibitions.
- **مسير نزوى السياحي** — annual guided walk each January; 3 000+ participants in 2026.
- **Eid shuwa at تنور مزارعة** — communal meat pits fired at both Eids. Some pits have
  their own waqf, so participants pay nothing and contribute labour instead.
- **Friday livestock auction (مناداة الأغنام)** — from 07:00 at the souq, roughly three
  hours, goats then cattle. The book calls it the busiest such auction in the Sultanate.
- **Craft workshops** — repeatedly named as a *plan* in press and in the Shell programme
  rather than an established offer. Currently a gap, not a product.

### Reading the numbers

- **Cafés dominate.** The top three venues by review volume are all cafés, carrying
  ~2 600 reviews between them — more than the quarter's own listing and its wall combined.
  The quarter functions as a café district that happens to be historic.
- **The anchor restaurant underperforms its traffic.** مطعم العقر has the second-highest
  review count (947) but the lowest rating of the majors (3.8), and it is the one venue
  the book itself promotes.
- **Beds are cheap and small-scale.** Most inns sit at OMR 18–28 a night. There is no
  upper-tier property inside the wall; the nearest four-star (Golden Tulip Nizwa) is
  outside it.
- **Evening is the peak.** Most food and drink runs to 23:00–02:00; the museum shuts at
  the end of the afternoon. Against 3 000–5 000 visitors a day, the daytime interpretive
  offer is thin — which is exactly what the Shell-funded visitor centre is meant to fix.

---

## 5. Discrepancies and open questions

### Resolve before publishing anything

1. **مسجد الشواذنة founding date.** Book: **9 AH**. Arabic Wikipedia and Oman Daily:
   **7 AH**. Al-Watan: **8 AH**. All agree on the 936 AH / 1529 CE mihrab and the 2003
   restoration. The book's "second mosque built in Oman" claim also needs a source.
2. **Age of the quarter.** Book implies pre-Islamic settlement. Press variously says
   1 200 years (Oman Observer, MIPIM material), 1 500 years, and 4 000 years (Al-Watan and
   the 2026 walk coverage). No two agree.
3. **Wall length.** Book: "in the region of two kilometres". Oman Observer / Oman Daily:
   **1 950 m**. Recent Omani coverage: **2 000 m**.
4. **Towers and gates.** Book: 15 towers, 4 gates. Recent official coverage: **16 towers,
   3 gates** — consistent with the book's own note that صباح السوق was demolished, but the
   tower count differs. A 2021 Oman Daily piece says **17**.
5. **Who began حصن نزوى.** Book: Imam محمد بن عبد الله بن أبي عفان, 2nd c. AH. Most
   reference works: Imam **الصلت بن مالك الخروصي**, 3rd c. AH / 9th CE, with the book
   casting him only as the extender. For the *wall*, Al-Sahwa dates al-Salt's original to
   **237 AH** and the Ya'rubi rebuild to **1050 AH**, compatible with the book.
6. **Fort construction dates.** Book: 12 years after the 1650 expulsion. Arabic Wikipedia
   and others: begun **1656**, finished **1668**.
7. ~~Restoration cost.~~ **Resolved.** The "RO 4,000" in one Oman Observer English piece
   is a garble. Al-Sahwa (Jan 2024) gives **OMR 400 000 for phase 1** and **OMR 2.5–3 m
   for the whole wall**; Oman Daily's "over OMR 3 million" is the full-project figure.

### Not yet verified

- **مقبرة الفرس** and the 1150 AH massacre — no independent source found.
- **قبر الشيخ الأصم** and the "deaf sheikh" anecdote — book only.
- **The 1992 souq architecture award** — no citation found; the awarding body is unnamed.
- **مستشفى الطبيب تومس** — the American mission doctor is almost certainly **Dr Wells
  Thoms** of the Arabian Mission, but this needs confirming and the spelling fixing.
- **ساعة المدة** — the book says no photograph exists; worth checking whether one has since
  surfaced from another wilayat, since the book says examples survive elsewhere.

### A standing caution on sourcing

Oman Daily's coverage of the wall reproduces the book's figures **verbatim**. The book's
author runs the quarter's endowment, and the endowment's own X account (@awqafnizwa) is
also a primary source. The book, the press and the project's communications are largely
**one voice, not three** — corroboration between them is not independent corroboration.

---

## 6. Sources

**The quarter and its history**

- [حارة العقر التاريخية بولاية نزوى — جريدة عمان](https://www.omandaily.om/print-article?articleId=1150773)
- [حـارة العقـر بولاية نزوى.. أعيد تجديدها واستغلالها سياحيًا منذ 5 سنوات — جريدة عمان](https://www.omandaily.om/%D9%88%D9%84%D8%A7%D9%8A%D8%A7%D8%AA/%D8%AD%D9%80%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%B9%D9%82%D9%80%D8%B1-%D8%A8%D9%88%D9%84%D8%A7%D9%8A%D8%A9-%D9%86%D8%B2%D9%88%D9%89-%D8%A3%D8%B9%D9%8A%D8%AF-%D8%AA%D8%AC%D8%AF%D9%8A%D8%AF%D9%87%D8%A7)
- [حارة العقر بنزوى من حارة مهجورة إلى حارة تعج بالحياة — الوطن](https://alwatan.om/details/473663)
- [Nizwa: Bridging sustainable development and heritage — Oman Observer](https://www.omanobserver.om/article/1171723/oman/nizwa-bridging-sustainable-development-and-heritage)
- [Restored Al Aqur wall now pride of Nizwa — Oman Observer](https://www.omanobserver.om/article/1148249/features/restored-al-aqur-wall-now-pride-of-nizwa)
- [سور العقر بنزوى يستعيد أمجاده — الصحوة](https://alsahwa.om/?p=206243) — phase costs, 16 towers, daily visitors, Al Aqr Plaza
- [Archnet: Al-Aqur](https://www.archnet.org/sites/22148) — 403 on fetch, open in a browser

**Restoration programme**

- [إطلاق مشروع تطوير حارة العقر بولاية نزوى — جريدة عمان](https://www.omandaily.om/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF%D9%8A%D8%A9/na/%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D9%85%D8%B4%D8%B1%D9%88%D8%B9-%D8%AA%D8%B7%D9%88%D9%8A%D8%B1-%D8%AD%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%B9%D9%82%D8%B1-%D8%A8%D9%88%D9%84%D8%A7%D9%8A%D8%A9-%D9%86%D8%B2%D9%88%D9%89)
- [افتتاح المرحلة الرابعة من مشروع سور العقر — وجهات](https://wejhatt.com/?p=113362)
- [المحروقي يجتمع مع اللجنة الرئيسية لتطوير حارة العقر — وجهات](https://wejhatt.com/?p=104252) — phase 3 detail
- [تواصل مشروع تبليط حارة العقر واستبدال الأسفلت بالحجارة المسطّحة — جريدة عمان](https://www.omandaily.om/%D8%B9%D9%85%D8%A7%D9%86-%D8%A7%D9%84%D9%8A%D9%88%D9%85/na/%D8%AA%D9%88%D8%A7%D8%B5%D9%84-%D9%85%D8%B4%D8%B1%D9%88%D8%B9-%D8%AA%D8%A8%D9%84%D9%8A%D8%B7-%D8%AD%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%B9%D9%82%D8%B1-%D8%A8%D9%86%D8%B2%D9%88%D9%89-%D9%88%D8%A7%D8%B3%D8%AA%D8%A8%D8%AF%D8%A7%D9%84-%D8%A7%D9%84%D8%A3%D8%B3%D9%81%D9%84%D8%AA-%D8%A8%D8%A7%D9%84%D8%AD%D8%AC%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D9%85%D8%B3%D8%B7%D8%AD%D8%A9)
- [بوارق نزوى: توقيع اتفاقيات لتطوير نزل نزوى التراثية — جريدة عمان](https://www.omandaily.om/print-article?articleId=15704)
- [إطلاق الهوية الجديدة لمشروعات "نزل نزوى التراثية" — جريدة عمان](https://www.omandaily.om/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF%D9%8A%D8%A9/na/%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%A7%D9%84%D9%87%D9%88%D9%8A%D8%A9-%D8%A7%D9%84%D8%AC%D8%AF%D9%8A%D8%AF%D8%A9-%D9%84%D9%85%D8%B4%D8%B1%D9%88%D8%B9%D8%A7%D8%AA-%D9%86%D8%B2%D9%84-%D9%86%D8%B2%D9%88%D9%89-%D8%A7%D9%84%D8%AA%D8%B1%D8%A7%D8%AB%D9%8A%D8%A9) — the *إحياء* rebrand

**2026**

- [MIPIM Awards 2026 — Winners](https://www.mipimawards.com/mipimawards2026/en/page/winners-2026) — confirms Al-Aqr did not win
- [11 sustainable projects named winners of 2026 Mipim Awards — Real Asset Insight](https://realassetinsight.com/2026/03/13/11-sustainable-projects-named-winners-of-2026-mipim-awards/)
- [Al Aqr, Al Thuraya projects shortlisted for the MIPIM Awards — Oman Observer](https://www.omanobserver.om/article/1183945/oman/al-aqr-al-thuraya-projects-shortlisted-for-the-prestigious-mipim-awards)
- [Harat Al Aqur to get facelift with new initiative — Oman Observer, 22 Apr 2026](https://www.omanobserver.om/article/1188397/oman/harat-al-aqur-to-get-facelift-with-new-initiative)
- [إطلاق النسخة الـ7 من "هدية شل للوطن" لدعم تطوير حارة العقر — وجهات، 23 أبريل 2026](https://wejhatt.com/?p=117402)
- [مسير نزوى السياحي يستكشف المقوّمات السياحية بالولاية — جريدة عمان، 3 يناير 2026](https://www.omandaily.om/ampArticle/1193751)
- [Oman's historic neighbourhoods revived as vibrant tourist destinations — Oman Observer, 17 Mar 2026](https://www.omanobserver.om/article/1186334/oman/tourism/omans-historic-neighbourhoods-revived-as-vibrant-tourist-destinations)

**Sites, aflaj and city**

- [مسجد الشواذنة — ويكيبيديا](https://ar.wikipedia.org/wiki/%D9%85%D8%B3%D8%AC%D8%AF_%D8%A7%D9%84%D8%B4%D9%88%D8%A7%D8%B0%D9%86%D8%A9)
- [قلعة نزوى — ويكيبيديا](https://ar.wikipedia.org/wiki/%D9%82%D9%84%D8%B9%D8%A9_%D9%86%D8%B2%D9%88%D9%89)
- [فلج دارس (نزوى) — ويكيبيديا](https://ar.wikipedia.org/wiki/%D9%81%D9%84%D8%AC_%D8%AF%D8%A7%D8%B1%D8%B3_(%D9%86%D8%B2%D9%88%D9%89)) — 7 990 m of canal, داوودي type, one of five Omani aflaj inscribed by UNESCO in 2006; Nizwa has 17 aflaj
- [Nizwa — Wikipedia](https://en.wikipedia.org/wiki/Nizwa) — largest city of Ad Dakhiliyah, ~140 km from Muscat, population ≈ 83 500

**Experiences and businesses**

- [جولة افتراضية سياحية تعريفية في أروقة «حارة العقر» — جريدة عمان](https://www.omandaily.om/%D9%85%D9%86%D9%88%D8%B9%D8%A7%D8%AA/na/%D8%AC%D9%88%D9%84%D8%A9-%D8%A7%D9%81%D8%AA%D8%B1%D8%A7%D8%B6%D9%8A%D8%A9-%D8%B3%D9%8A%D8%A7%D8%AD%D9%8A%D8%A9-%D8%AA%D8%B9%D8%B1%D9%8A%D9%81%D9%8A%D8%A9-%D9%81%D9%8A-%D8%A3%D8%B1%D9%88%D9%82%D8%A9-%D8%AD%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%B9%D9%82%D8%B1-725442) — the VR tour
- [مقاهي الحارات القديمة.. تعزز السياحة وتجسد التراث — جريدة عمان](https://www.omandaily.om/ampArticle/1160758) — مقيل كافيه and its owner
- [IHYAA Inn — نزل إحياء on Booking.com](https://www.booking.com/hotel/om/nizwa-heritage-inn.html)
- [Antique Inn, Nizwa on Booking.com](https://www.booking.com/hotel/om/antique-inn.html)
- Google Maps directory for [حارة العقر القديمة](https://www.google.com/maps/place/%D8%AD%D8%A7%D8%B1%D8%A9+%D8%A7%D9%84%D8%B9%D9%82%D8%B1+%D8%A7%D9%84%D9%82%D8%AF%D9%8A%D9%85%D8%A9/@22.9308327,57.5314614,17z)
- [@awqafnizwa](https://x.com/awqafnizwa) and [@haratalaqur](https://x.com/haratalaqur) — the endowment's and the quarter's own accounts

---

## Appendix A — full Arabic text of the book

Recovered from `REFRENCE.pdf` as described in §1. HTML comments mark PDF page boundaries.
Photographs are not extracted; `[صورة]` marks a caption. Poetry diacritics are unreliable.

<!-- PDF page 2 -->

جميع الحقوق محفوظة

1442 هـ / 2021م

نشر وتـوزيـع:

مكتبة خزائن الآثار

سلطنة عمُان ـ بركاء

نقال: 0096895510025

التنفيذ الطباعي: مجموعة مسقط للأعمال التجارية رقم الإيداع الدولي: 978-9933-29-448-9 ISBN

<!-- PDF page 3 -->

بسم الله والحمد لله ذو المن والعطاء والجود والسخاء والعزة والنعماء الذي أعطى فأكرم ووهب فأبدع، أما بعد...

فما زالت حارة العقر بنزوى تنفض عنها غبار النسيان والإهمال، وتتوشح وشاح النهوض والاهتمام؛ لتعود منازل أهلها عامرة بعد الترميم، وجميلة بهندستها وحسن التصميم، وما زال ملاك بيوتها يصلحون ويرممون منازلهم حفاظاً على صنع الأجداد، ومنذ أن بدأت شركة بوارق نزوى التراثية في أول عملية ترميم تشهدها الحارة، تواصلت الجهود من جميع الأطراف في هذا الواجب الوطني، وإكمالاً لذلك وتماشياً مع مسيرة تطوير الحارة جاء هذا العمل ليلبي جانباً مهماً في المجال السياحي والثقافي، مدعوماً بالصور لتزيده جمالاً وإيضاحاً.

وبعد هذا الجهد المتواضع فإن أحسنت فيه فمن الله، وإن قصرَّت فهذا مبلغ همتي ومعرفتي، والحمد لله رب العالمين.

سليمان بن محمد السليماني

ولاية نزوى ـ قرية العقر

<!-- PDF page 4 -->

### حارة العقر

عند الحديث عن حارة العقر فهذا يعني أننا سوف نتحدث عن تاريخ نزوى، وهو يعني أيضاً أننا سنتحدث عن تاريخ عمان، فنزوى كانت عاصمة عمان في أغلب الحقب الإسلامية، وحارة العقر هي مقر الحكم العماني والذي منه تسُنَ الأوامر والقرارات النافذة، ومنها تتحرك الجيوش الجراّرة، وتنطلق التوجيهات إلى الأساطيل العمانية في الخليج والمحيط الهندي، فهي بذلك أحد أهم الحارات القديمة في عمان دون منازع، فالاهتمام بها هو اهتمام بالتاريخ العماني، والحفاظ عليها هو واجب كل مواطن، فهي إرث الأجداد للأحفاد وأمانة تتعاقب عليها الأجيال، فلا خير فيمن يضيع الأمانة، ولا قدر لمن لا يدرك ثمن الميراث، فميراث عمان العلم والتاريخ، ونزوى هي حاضنة العلماء ومقر الساسة والحكماء، ولن أطيل في أمجادها فالقلعة الشهباء لا تخفى على قليل النظر، والسوق العتيق خير شاهد فيها وأثر.

<!-- PDF page 5 -->

يحيط بحارة العقر سور متين عليه خمسة عشر برجاً وأربع بوابات، ويزيد عدد منازلها عن 300 بيت، بنيت من الطين والحجارة الصلبة والصاروج، وتدل الشواهد فيها أنها عامرة بالسكان منذ ما قبل الإسلام، بداخلها خمسة مساجد قديمة والكثير من المدارس والمجالس،

ويتخلل بيوتها سكك وأزقة ضيقة، وتتداخل منازلها في بعضها البعض لكثرة ساكنيها وزحام قاصديها، وتضم الكثير من القبائل، بل إن أغلب القبائل العمانية المعروفة موجودة فيها، كانت تغلق أبوابهـا ليلاً فلا يمكـن الدخـول إليها بعد الإغلاق.

<!-- PDF page 6 -->

سأتحدث في هذا الكتاب عن حارة العقر فقط، التي هي داخل السور؛ لأن حدود هذه الحارة في الأصل يمتد إلى مقبرة الأئمة غرباً (حي العين) وغاف الشيخ جنوباً وإلى مجرى الوادي من الشمال والشرق، وفي هذه المناطق توجد الكثير من الشواهد والآثار القديمة التي تستحق الزيارة، ويوجد عدد كبير من قبور أئمة عمان وكبار علمائها وزعمائها، وهي زاخرة بالأبراج والمساجد والأفلاج وغيرها من الآثار التاريخية، لكنني اقتصرت على هذا المكان حتى لا أطيل أو أخرج عن الغاية التي من أجلها قام هذا العمل، وفي الصفحات القادمة سأبين أهم الشواهد المعروفة فيها.

<!-- PDF page 11 -->

### قلعة نزوى الشهباء

هي أحد أهم وأكثر الأماكن استقطابا للسواح في عمان، بل هي وجهة رئيسة لكل زائر لسلطنة عمان عموما ومدينة نزوى خصوصا، فهي فخر دولة اليعاربة، وتاج في التاريخ العماني الكبير، وهي من الجانب الهندسي فن معماري فريد بشكلها ومداخلها ومدافعها وآبارها، وطرق الدفاع فيها، أما مصدر تمويل البناء فبعد أن طرد الإمام سلطان بن سيف اليعربي المحتل البرتغالي من عمان سنة 1650م، قام بمطاردتهم في الخليج العربي وفي كل شبر وجُدِوا فيه في المحيط الهندي وبالأخص في الهند وشرق إفريقيا، وقد شن عليهم في مدينة (ديو) بمومباي في الهند ثلاث حملات شديدة كانت كفيلة بإضعاف الإمبراطورية الأقوى في العالم في ذلك الحين لتذيقها الهزائم المتتالية، وبذلك حصل الأسطول العماني على الكثير من الغنائم، عمل بها الإمام مشاريع تحصينية وزراعية في عمان وأهمها هذه القلعة الشهباء، واستغرق العمل بها اثني عشر عاما، واستخدم في بنائها الصاروج العماني، ويقوي قاعدتها صخور كبيرة وقوية جلبت

<!-- PDF page 12 -->

من الجبال، لذلك لم تتأثر القلعة بقصف صواريخ سلاح الجو الإنجليزي إلا شيئا يسيراً جداً، وبها الكثير من أنواع الدفاع التي تجعل العدو يعجز عن الصعود إليها والتي لا يستطيع الزائر معرفتها بدون مرشد، وبها سراديب سرية وأسرار عجيبة، وتضم هذه القلعة الشهباء الكثير من المدافع والأسلحة والتي يعتبر كثير منها غنائم حرب.

[صورة] قلعة نزوى 1902م

<!-- PDF page 13 -->

من روائع الشيخ العلامة سيف بن محمد الفارسي في رائيته العمانية وهو يذكر أعمال الإمام سيف بن سلطان بن مالك اليعربي رحمهم الله أن قال:

سُلَ القلَعْةَ الراَّسيِ رسَاَ الشمُّ أسُهُّا

معَاَرفِ وصلَ لا يحَلِ بها النكُّر

هُيِ القلَعة الساَّمي سمَاَ النجَّم سمَكْهُاَ

تنُبَيِّك نزَوْىَ أنَ ساَحتَهَا العقَرْ

وُّقفِ حوَلْهَاَ مسُتْنَبْئِاً عنَ مشُيِدْهِا

نعَمَ عزَمْ سلُطْاَن وهمَاَّتهُ الغرُ

<!-- PDF page 14 -->

### حصن نزوى

بدأ تشييد حصن نزوى في القرن الثاني الهجري قبل ألف ومئتي سنة، في عهد الإمام محمد بن عبد الله بن أبي عفان ثم تتابعت الزيادات عليه في عهد الإمام الصلت بن مالك الخروصي والأئمة الذين جاءوا من بعده، ولعل أكثر الزيادات كانت في زمن الإمام الصلت بن مالك تزامنا مع قوة عمان البرية والبحرية وأسطولها الكبير الذي وجهه الإمام لنجدة أهل سقطرى من ظلم النصارى بعد أن استنجدت به امرأة تسمى فاطمة السقطرية بقصيدة مشهورة تشرح فيه ما قام به النصارى، وبذاك الأسطول أيضا طهر الإمام المحيط الهندي من القراصنة بعد أن شكى له إمبراطور الهند تعرضهم للتجار ونهبهم للسفن، ليهدي بذلك إمبراطور الهند سيفاً هندياً ثميناً للإمام الصلت.

كما يعتبر هذا الحصن من الحصون العمانية الفخمة، وبه عدد من الغرف والآبار والمخازن والسجون وغرف للتعليم والمؤونة وغيرها من الغرف، وقد بنيت قلعة نزوى محاذية له.

<!-- PDF page 15 -->

### مسجد الشواذنة

هو ثاني مسجد بني في عمان حيث بني في السنة التاسعة للهجرة، ويدل قدم بناء المسجد أن حارة العقر كانت آنذاك أهم المناطق في عمان وأن أهلها دخلوا إلى الإسلام عند وصول دعوة النبي ژ أو ربما قبل ذلك ويتميز المسجد بمحراب جميل جدا أبدع فيه الناحت ليكون مثالا للنقوش الإسلامية العمانية وكان صنعه سنة 936 هجرية، وكعادة العمانيين فقد وثق اسمه على النقوش بخط جميل، وقد خضع المسجد للكثير من عمليات الترميم منذ بنائه الأول والذي يزيد عن 1400 سنة إلى ترميمه الأخير عام 2003 والذي قامت به وزارة التراث العمانية، وقد تخرج منه الكثير من العلماء، كان بعضهم يرابط فيه بين صلاتي العشاء والفجر للعلم والمذاكرة.

<!-- PDF page 17 -->

### مسجد مزارعة

هو أحد المساجد القديمة في حارة العقر يعود بنيانه إلى القرن الثالث الهجري، وهو مسجد قائم على قاعدة مرتفعة كما هو الحال في المساجد القديمة، ويحتوي المسجد في محرابه على الآية الكريمة: ﴿ ﮙ ﮚ ﮛ ﮜ ﮝ ﮞ ﮟ ﮠ ﮡ ﮢ ﮣ ﮤ ﮥﮦ ﮧﮨ ﮩﮪ ﮫ ﮬ ﮭ ﮮ ﮯ ﮰ﴾.

ويعد هذا المسجد من أوسع المساجد في حارة العقر، وتوجد على سقفه تواريخ تسقيفات قديمة وعلى جداره كتابات تؤرخ لحقب زمنية مختلفة جمعها الأستاد محمد بن عبد الله السيفي في كتاب (الحلل السندسية في الكتابات المسجدية)، وقد أعيد ترميمه في عام 2020م وصرف عليه من وقفه الخاص حيث يعتبر من المساجد الغنية بالأوقاف، وقد سعى وكلاء المسجد على ترميمه بالطين والصاروج والحجارة والأخشاب؛ فقد خسرت الحارة سابقا الكثير من المباني التاريخية المهمة التي هدمت لإعادة البناء بالمواد الحديثة، وأهمها جامع نزوى ومسجد الشيخ والمقصود به الشيخ بشير بن المنذر.

<!-- PDF page 18 -->

وقصة البناء الأول لهذا المسجد أن رجلاً قام بالإنفاق عليه دون أن يعلم عنه أحد، فكان يبعث بالنفقة اليومية لعمال البناء، وشاء الله أن يتوفى هذا الرجل الصالح قبل أن يكتمل العمل، فتساءل الناس عن سبب عدم إكمال البناء؛ فذهب رجل إلى مسؤول العمال فأخبره المسؤول أنه كان هناك رجل يدفع لهم الأجرة وقد توفاه الله وقد أوصى بعدم ذكر اسمه، فقال الرجل لمسؤول العمال: أكملوا البناء وأنا أتكفل بالباقي ولا تذكروا اسمي؛ فشاء الله أن يتعاقب اثنان على بناء هذا المسجد لا تعرف أسماؤهم، وما زال المسجد عامراً بالمصلين إلى يومنا هذا.

<!-- PDF page 19 -->

[صورة] صورة قديمة لجامع نزوى

### جامع نزوى ومركز التعريف بالإسلام

وهو أحد الجوامع العمانية الشهيرة، بني على ضفة وادي كلبوه في القرن الثاني الهجري قبل حوالي 1200 سنة، ويقع شمال شرق قلعة نزوى، ويعد من ضمن أقدم الجوامع وله أوقاف كثيرة، تحولت إدارته إلى ديوان شؤون البلاط السلطاني؛ فأعيد بناؤه في بداية نهضة السلطان قابوس بن سعيد 5 ، وفيه كان يجتمع العلماء للبحث في المسائل العلمية والسياسية، وتنصيب الأئمة وحل القضايا المهمة، وعلى محرابه وقف الخطباء من العلماء والأئمة والصالحين على مر الحقب الزمنية لتاريخ عمان العظيم، وتوجد به قاعات وصفوف لتعلم الطلاب ومكتبة عامة كبيرة تحوي مختلف صنوف العلم، وأدخل فيه حديثا مركز التعريف بالإسلام؛ وذلك لكثرة الراغبين من غير المسلمين في معرفة مفاهيم الإسلام وسماحته، كما يجري حاليا إنشاء مركز آخر للتعريف بالإسلام غرب مسجد مزارعة يتبع وزارة الأوقاف والشؤون الدينية.

<!-- PDF page 21 -->

[صورة] نزل نزوى التراثية

### نزل نزوى التراثية

افتتح نزل نزوى التراثية تحت رعاية سعادة الشيخ حمد بن سالم بن سيف الأغبري والي نزوى، بتاريخ 1 ذي القعدة 1439هـ الموافق 23 ابريل 2018م. حيث قامت الشركة بهذه المبادرة منذ تأسيسها لتحويل الحارة لمقصد سياحي وللحفاظ على تراث الأجداد وتعريف الأجيال كيف عاش أسلافهم، ولتلُهْمِ الأهالي وأصحاب المنازل حسن استغلال المكان وإكمال المسيرة لترميم كل شواهد الحارة من منازل ومدارس ومجالس وأبراج وأسوار وهي الغاية المنشودة. ولهذا الموقع مكانة كبيرة عند كبار السن حيث كانوا يلتقون فيه للاطلاع والقراءة وتناول القهوة، ويظهر هذا الاهتمام لكثرة القاصدين للموقع من كبار السن ثم تسرد القصص والنوادر المتعلقة بالحارة وهم يستمتعون بشرب القهوة فيعيشون بذلك وكأنهم في الزمن الماضي.

<!-- PDF page 22 -->

[صورة] صور قديمة لمكتب نزل نزوى التراثية

<!-- PDF page 23 -->

برج الكوارج

Alkwareg Tower برج بلج

Balleg Tower

برج محمود

Mahmoud Tower برج العلياء

Alal’ia Tower

برج قطعة

الطوي

Qatet

A’tawi

Tower

صباح وبرج

الصبخة

Alsabkhe

& Gate

Tower

صباح وبرج

أبي المؤثر

Abi Almu’thir

Gate & Tower

الغربي (سكة القبر)

Bustan Alaqur Algharbi (Sikkat )Alqaber Tower

برج القلعة

Alqal’ah Tower

برج المذبحة

Almethabha Tower

صباح السوق

برج غوير

Alsuq Gate

Ghowair Tower

صباح وبرج

قلعة نزوى Nizwa Fortحصن نزوى Nizwa Castle الشجبي

Alshujbi

& Gate

Tower

برج ميرزة

(بستان قسام)

(Merzah Bustan

)Qassasm Tower

برج خريص بلج

Kharis Balleg Tower

سور العقر AlAqur Wall

برج حارة

برج حارة

الزامة الغربي

الزامة الشرقي

Harret A’zzamah

Harret A’zzamah

Algharbi Tower

A’sharqi Tower

برج بستان العقر

قلعة وحصن نزوى وسور العقر

NIZWA ,FORT CASTLE & ALAQUR WALL

برج بستان

العقر الشرقي

Bustan Alaqur

تصميم: الوليد بن زاهر السالمي

A’sharqi Tower

### سور العقر

من آثار مدينة نزوى الخالدة سور العقر وهو من الأسوار العريقة في عمان ومن التحصينات المهمة، وهو بحق تحفة معمارية نادرة له خصوصياته ومميزاته الهندسية التي ينفرد بها عن بقية الأسوار الموجودة، وكان هناك أثر لسور مندرس بقيت أطلاله بادية ويبدو أن السور القديم تأثر بفيضان الأودية في سنة 853 للهجرة، ويرجح بناؤه زمن الإمام الصلت بن مالك الخروصي، ثم إن الإمام سلطان بن سيف بن مالك اليعربي أسس سور العقر بعد خرابه، وجعل له مداخل محددة وأبراج حماية، وفخامة في ارتفاعه وعرضه، وعليه فإن تأسيس سور العقر الحالي كان في النصف الثاني من القرن الحادي عشر الهجري. وقد استغرق بنيان السور سبع سنوات، بناه الإمام سلطان تزامنا مع بنيان قلعة نزوى حيث كلف العمال بتشييده. وقد مر السور بعدد من الصيانات والإصلاحات وهو يحيط بحارة العقر ويبلغ امتداده في حدود كيلوين اثنين، ويعتبر الخط الدفاعي الأهم لساكني حارة العقر، ويتراوح سمكه بين متر ونصف إلى

<!-- PDF page 24 -->

مترين ويزيد من متانته قاعدة صخرية، ويتراوح ارتفاعه من خمسة إلى ستة أمتار ويحتوي السور على العديد من الأبراج المتصلة به وقيل يبلغ عددها خمسة عشر برجاً وتبلغ المسافة بين كل برجين (150 ـ )200 متر، ولكل برج من هذه الأبراج تسمية يعرف بها مثل برج المذبحة ويقع في الزاوية الشمالية على جانب الغربي من السور، وبرج ميرزة على الجانب الجنوبي من مسجد الشجبي ويسميه البعض برج بستان قسام، وبرج بلج على الجانب الشرقي على جهة الغرب من سوق نزوى، وبرج العلياء وهو الواقع أعلى من برج بلج، وبرج غوير يقع في السوق أمام بوابة السوق الشرقي المعروف باسم الصنصرة وكان السور متصلاً مع [صورة] صباح أبي المؤثر

[صورة] صباح أبي المؤثر

<!-- PDF page 25 -->

هذا البرج؛ وليس كما يظهر حديثاً بأنه مستقل بنفسه، وبرج السوق وبرج القلعة وبرج بستان العقر الأول وبرج بستان العقر الثاني، وبرج الصبخة، الذي يقع بجانب صباح الصبخة، وبرج قطعة الطوي، وبرج حارة الزامة، وبرج سكة القبر، وبرج خريص بلج.

وأكثر هذه الأبراج ذات شكل أسطواني وقاعدتها دائرية الشكل يتراوح قطر قاعدتها من 4 ـ 5 أمتار والبعض الآخر مكعب الشكل وقاعدته مربعة الشكل، وعند كل برج يوجد درج مرتبط بالسور وظيفته تسهيل مهمة العسكر في الصعود [صورة] صباح السوق

والهبوط إلى السور أثناء فترات الحراسة في الأبراج، كما يحتوي السور على أربعة مداخل أو بوابات وهي المنافذ الوحيدة لساكني الحارة تعرف هذه المداخل باسم (صباح) وهي: صباح أبي المؤثر في الجهة الجنوبية، وصباح الشجبي في الجهة الغربية، وصباح السوق في جهة الشمال الشرقي، وصباح الصبخة في الجهة الشرقية، و يوجد على كل بوابة حارس يقوم بعملية التنظيم، وقد تم هدم صباح السوق أثناء عمليات ترميم القلعة والسوق، ولم يبقى منه إلا بعض الصور.

<!-- PDF page 26 -->

[صورة] صباح وبرج الشجبي

[صورة] صباح وبرج الشجبي

<!-- PDF page 27 -->

[صورة] صباح وبرج الصبخة من الشرق والغرب

[صورة] واجهة سوق نزوى ويظهر سور العقر ببنائه الحديث

[صورة] صورة للسور من برج المذبحة ويظهر في الصورة فلج ضوت

<!-- PDF page 28 -->

### البيت العماني في حارة العقر

في الغالب: يضم البيت العمُاني في حارة العقر في دوره الأول: مجلس وغرف نوم ودهليز ومخزن للتمور يعرف باسم النضد ودورة مياه والتي كانت تسمى الشروني بالإضافة إلى بئر ماء خاص للبيت وقد يتشارك البيتان أحياناً بئـراً واحدة، ويختلف التقسيم الداخلي في الطابق الثاني حسب رغبة أهل البيت ولكن أكثر هذه المنازل كانت في طابقها الثاني جزء منها مفتوح للسماء، أما المطبخ فأكثر ما وجدته في الطابق العلوي وأحيانا في غرفة تتوسط الطابقين على الدرج، ومن أهم أثاث ومقتنيات المنزل (الموقعة) وهو حجر لدق الحبوب، ومكان عمل القهوة ومكانه في غرفة الضيوف أو الدهليز، وتصل مساحة المنازل من (60م إلى 200م) ولو تأملنا لوجدنا أنه لا توجد في العقر بيوت كبيرة جداً وشديدة الفخامة مثل التي توجد في بعض القرى في عمُان ويرجع ذلك لعدة أسباب، فعلى الرغم من أن العقر هي الحارة الرئيسية في عمُان إلا أنه غلب على سكانها طابع الاهتمام بالعلم والعمل وبالزراعة

ولم يكن لهم اهتمام بالرفاهية في بناء المنازل إلا أن ذلك طبعاً لم يمنعهم من الاهتمام من الإبداع الهندسي في البناء، كما أن الكثافة السكانية الكبيرة لم تكن تسمح بعمل منازل ذات مساحة كبيرة.

أما الأبواب فهي خشبية منقوشة، عليها عقود جميلة وأسقفها من جذوع النخيل وعليها زخارف ونقوش ومكتوب عليها تواريخ وآيات قرآنية وبعض أبيات الشعر، ونوافذها خشبية بأربع فتحات ليتمكن الساكن من فتح العلويات دون السفليات إن رغب ذلك.

ولا بد من أن تحتوي على جرة (جحلة) لماء الشرب وخرس من الفخار ومناديس للملابس وعلى الجدران روازن وأرفف ومعاليق وقد صممت جدرانها عريضة جداً ليتحمل البيت الثقل الذي عليه وليستغل أيضا لعمل روازن، وتحتوي بعض جدران البيوت على نقوش وبألوان أخضر وأحمر وأبيض.

<!-- PDF page 29 -->

### حارة العقر في حكم دولة اليعاربة

لعل أكبر نهضة عمرانية شهدتها حارة العقر كانت في عصر هذه الدولة؛ فبناء القلعة الشهباء فيها تبعته الكثير من الإصلاحات التحصينية التي تحتاج إليها الحارة؛ منها إعادة بناء سور العقر وترميمه بحدوده وهندسته الحالية، كما نالت مدينة نزوى مثل كل مدن عمان نصيبها من الرقي والازدهار في زمن دولة اليعاربة في سهولها وجبالها وقراها ومزارعها، نتيجة القوة البرية والبحرية والنهضة العمانية التي تلت طرد البرتغاليين، وانتهاء دولة النباهنة، وأصبحت عمان في القرنين السابع عشر والثامن عشر تجابه وتواجه وحدها في المحيط الهندي أكبر قوى العالم والتي تمثلت في القوى البرتغالية والإنجليزية والهولندية والفرنسية والفارسية، وأكثر هذه الدول سعت أولا إلى السيطرة على عمان، وعندما لم تستطع أقامت معها العلاقات الدبلوماسية والتجارية وعينت سفراء لها، وأصبح الدخول إلى المحيط الهندي يحتاج إذن من الأسطول العماني لأن سفن أسطولها البحري تجول فيه بل أصبحت كل هذه القوى والأساطيل الأجنبية تخشى مواجهة عمان.

أما في الجانب العلمي فقد عم العلم عمان نتيجة اهتمام الأئمة به بإقامة المدارس والصرف عليها وكثرة العلماء، وأبدع الأدباء في كتاباتهم وأشعارهم، وبديهيا جدا أن تتغير مظاهر الحياة بكل تفاصيلها، حتى داخل العائلة نفسها وفي فكر الرجال وحديث النساء وبين الأطفال في ألعابهم وطريقة بناء المنازل، وتعدد البضائع في الأسواق، فلا مكان للتقوقع والتخلف في دولة يبنى فيها أضخم القلاع والحصون ويجلب إليها غنائم حرب المدافع والباروت، ويشق في باطن أرضها الصخور الصماء لتتفجر الأفلاج في قنواتها دون أن يخشى العمال الظلمة الحالكة أو يتذرعوا بالعمق السحيق، ويهيئ سكان جبالها طرقاً لهم من وعر الجبال بصخور لها حمل ثقيل تقص وتحمل إلى مكانها ثم يحولون صم الجبال إلى مدرجات زراعية وواحة غناء، ويخرج أهلها إلى البحار والمحيطات شهورا للتجارة لا يخافون من هيجان الموج وظلام الليل، وقد يكون لمجابهة عدو تسلط على ضعيف، أو تلبية نداء المظلومين والمنهوبين من الظلمة في ساحل قارة أفريقيا.

ولأن حارة العقر كانت الساحة السياسية والدينية في ذلك الزمان فهي أكثر من يعايش تبعات ما ذكر بل أولها؛ لذلك فإن أول انعكاس للتأثير يبدأ فيها.

<!-- PDF page 30 -->

### الأبواب والأسقف

اعتاد العمانيون استخدام أجود أنواع الخشب في الأبواب والنوافذ المنزلية، وكذلك الأسقف، أما الأسقف فقد كان أغلب اعتمادهم على جذوع النخيل لقوتها وديمومتها وكثرة توفرها، أما الأبواب والنوافذ فبالإضافة لبعض الأخشاب العمانية كانوا يستخدمون الأخشاب الهندية القوية التي كانت تأتيهم عن طريق التجار العمانيين الذين يقطعون البحار شرقا وغربا، وكانوا كثيراً ما يوثقون على الأبواب والأسقف تاريخ العمل واسم الصانع وصاحب المنزل والحاكم الذي كان على عمان حينها.

<!-- PDF page 32 -->

ِكتب على هذا الباب:

كِتِاَبيِ فيِ الباَب المسَُواَّ المحُبَرَّ لًسِتِ تبَقَتَّ منِ ربَيِعْ المؤُخَرَّ لِثِاَلـِثَة تـَتـْلوُ الثمَّاَنيِن حجِةَّ وٍأَلَف يوُازيِ فيِ الحسَِاب المقُرَرَّ بِدِوَلةَ سلُطاَن بنْ سيَف بنْ ماَلكِ إٍمَِام البـَراَياَ اليعَرْبُِي المظُـَفرَّ لِقِاَضيِ القضُاَة الأرَيحَيِ محُمَدَّ فتَىَ اْبن عبُيَـداَن الفقَيِه المطُهَرَّ

تِرَدَىَّ ردَاَء العلِْم واَلحلِمْ واَلحجِىَ

.......... باِلــعـَـفـَـاف مـُــؤزَرَّ

وِنَجَاَّرهُ عبَدْ الإلِهَ أخَوُ النهَُّى

سلَيِل سنِاَن ذوُ الصفَّيِ المشُهَرَّ

نجد أن النجار كان ماهرا جدا ويتقن الشعر وفي هذه الأبيات الستة ذكر معلومات مهمة للأجيال المتعاقبة ووثق اسمه واسم صاحب المنزل ووظيفته ومنزلته العلمية والتاريخ واسم الإمام.

<!-- PDF page 33 -->

[صورة] مدرسة الجليلين

### مدارس تعليم القران الكريم

تنتشر في أغلب حارات عمان ـ كما هو الحال حديثا ـ الكثير من مدارس القرآن الكريم وعلوم اللغة والأدب وبعض العلوم الأخرى، وفي حارة العقر هناك مجموعة من المدارس بقيت بعض جدرانها كما رممت بعضها حديثاً، ولها أوقاف فرضت لها قديما. تخرج من هذه المدارس الصغيرة الكثير من العلماء الكبار الذين أصبحوا بعد ذلك رجالاً للدولة ولهم شأن كبير، ولم تكن مساحة المدرسة مهماً بقدر أهمية العلم والمعلم.

<!-- PDF page 34 -->

[صورة] سبلة النيري

### المجالس

تنقسم حارة العقر داخليا إلى خمس حارات، ولا تخلو حارة من هذه الحارات من مجلس أو سبلة يجتمع فيها الأهالي بشكل دائم، فيتبادلون فيها أحوالهم ويكرمون ضيفهم ويتشاركون طعامهم، إذ كانت حياتهم اجتماعية، وجيرتهم أخوية بروابط الدين وحسن الجوار.

[صورة] سبلة الكوارج

<!-- PDF page 35 -->

### بيت الصاروج

هو أحد أكبر البيوت في حارة العقر، وأكثرها فخامة وصلابة، وعلى الرغم من أن العديد من المنازل في هذه الحارة بنيت بالصاروج إلا أن هذا البيت تميز بهذا الاسم، وقد سكنه سابقا الكثير من الشخصيات السياسية المهمة منهم السيد طارق بن تيمور البوسعيدي والد السلطان هيثم بن طارق حفظه الله.

<!-- PDF page 36 -->

### شعار نزوى عاصمة الثقافة الإسلامية

اختيرت مدينة نزوى لتكون عاصمة الثقافة الإسلامية لعام 2015، وذلك لمكانتها العلمية الكبيرة ولإسهاماتها الدينية المتعددة على مر التاريخ العماني، كيف لا وهي بيضة الإسلام وتخت العرب ومركز الإمامة ومدينة العلم والعلماء، وهي إحدى أكثر المدن العربية نتاجاً علمياً، كما أنها تتبوأ مركزا متقدما في عدد العلماء وحجم الكتب والتأليف، وقد مر على نزوى فترات من الزمن دون أن يخلو بيت من بيوتها من وجود عالم فيه، وقد يغنيك في إجابة سؤالك العلمي تاجر أو حماّل أو عامل بناء لكثرة العلماء فيها، لذلك احتفل بها في العام 2015م لتكون عاصمة للثقافة الإسلامية، ونصب لها هذا البرج التذكاري في واجهة السوق شاهدا على ذلك..

<!-- PDF page 37 -->

### تنور مزارعة

اعتاد العمانيون شوي بعض لحوم ذبائحهم بدفنها في تنانير موقدة بحطب الأشجار الطبيعية في أيام عيدي الفطر والأضحى في قالب اجتماعي جميل، حيث يتجمع أهالي كل حارة لعمل الشواء العماني، وهي عادة اجتماعية ما تزال باقية إلى اليوم، وبعض هذه التنانير لا يدفع المشاركون فيها شيئاً من المال، لأن لها مواقيف خاصة؛ فهم يشتركون في العمل ويتسلون بذلك.

[صورة] نموذج لعملية دفن الشواء

<!-- PDF page 38 -->

### قبر الشيخ الأصم

يقع قبر الشيخ العلامة الأصم أبي عبد الله عثمان بن عبد الله بن أحمد العزري خلف مسجد الشواذنة وغرب مدرسة الجليلين، وهو من كبار علماء القرن السابع الهجري، وتضم ولاية نزوى قبور الكثير من الأئمة والعلماء ولكن اللافت في قبر هذا الشيخ وجوده في وسط الحارة؛ علماً إن أكثر قبور العلماء والأئمة توجد في المقبرة المعروفة في غرب الولاية وبعضها في أطراف القرى، ولم يكن هذا الشيخ أصم كما لقب، ولكن لذلك قصة طريفة يعرفها الأهالي، وهي أن امرأة جاءته تستفتي، ومن غير قصد صدر منها خلال حديثها صوت ريح، فتدارك الشيخ كي لا يحرجها وطلب منها إعادة سؤالها متع لا وهو ممسك أذنه أن سمعه ضعيف.

<!-- PDF page 39 -->

### مقبرة الفرس

توجد هذه المقبرة في سكة تعرف باسم سكة القبر، وذلك نسبة إلى وجود قبر في مدخلها؛ وهي مقبرة جماعية لعدد كبير من الفرس، عندما دخلوا عمان في أواخر دولة اليعاربة ودخلوا نزوى في 1 من ذي الحجة من سنة 1150هـ وعاثوا فيها فسادا، وكان عددهم كبيراً؛ قيل 4000 جندي دخلوا عليها في غفلة من أهلها، فقتلوا الأطفال والشيوخ وخطفوا النساء واستباحوا الحرمات، فعمد الأهالي إلى عمل كمين لهم بإدخالهم إلى الحارة وإغلاق أبوابها كي لا يستطيعوا الفرار منها فقتل أكثرهم، ونجت البلاد من شرهم، وقد دفن في هذه الحفرة عدد كبير منهم في قبر جماعي كبير لهم. وذلك دأب العمانيين في من غزاهم واستحل أرضهم لا يقر لهم قرار إلا بالقضاء عليه وإعادة الأمن للبلاد؛ ولأجل هذا سمى البعض عمان بمقبرة الغزاة.

<!-- PDF page 40 -->

### مستشفى الطبيب تومس

ما يزال كبار السن في نزوى يذكرون مستشفى الطبيب الأمريكي تومس؛ ليس لأنهم كانوا يعالجون عنده فحسب، لكنهم يحفظون علاجه لإمام عمان محمد بن عبد الله الخليلي عندما أصابه العمى في عينيه فشفاه الله بعلاج هذا الطبيب، كما يحكون عنه الكثير من القصص والأخبار التي شهدوها بأنفسهم، والتي كانت بسبب إعجابه الشديد بشخصية الإمام 5 .

وعندما عـاد إلى بلده حـدث القسيسين في أميركا عن إعجابه بالإمام 5 ، وأن الإمام 5 كان يمثل خلق النبي إبراهيم ‰ ، وحدث بهذا سماحة الشيخ الخليلي بنفسه.

<!-- PDF page 41 -->

### قنوات تصريف المياه

منذ قديم الزمان راعت الهندسة العمانية في بنائها تصريف مياه الأمطار في الحارات وبين المنازل في السكك، فلا تتعجب عندما تجد هده الفتحات منتشرة في الحارة، وقد تشاهد مياه الأمطار وهي تجري فيها وتمر أسفل المنازل حتى تصب في سواقي الافلاج والمزارع.

<!-- PDF page 42 -->

### السيارات السياحية

وقعت شركة بوارق نزوى الدولية للاستثمار ممثلة في نزل نزوى التراثية اتفاقية تشغيل السيارات الكهربائية للجولات السياحية مع إحدى الشركات العمانية، لتكون بذلك أول مشغل لهذه السيارات في السلطنة، استكمالا لمسيرة تطوير الحارة، وبإمكان أي سائح أخذ جولة سياحية وتعريفية بها حيث تنتشر الآن هذه السيارات بطول فصل الشتاء في حارة العقر.

<!-- PDF page 43 -->

### الأوقاف

حرص العمانيون في مختلف أنحاء عمان منذ دخول الإسلام أن يبقوا لأنفسهم صدقة جارية، وذلك بوقف شيء من ممتلكاتهم لأمر معين، فنجد الكثير من المزارع المنتشرة في الجوار هي أوقاف للمساجد والمدارس والفقراء والمساكين وأبناء السبيل وطلبة العلم والمعلمين، وكانت الأوقاف في عمان تعم كل احتياجات الناس كبيرها وصغيرها، حتى إن البعض كان يوقف بعض المستلزمات المنزلية والصحية التي قد يزهد فيها الكثيرون لرخصها، ولحرص الناس سابقا على هذه العادة الحميدة كان البعض يوقف نخلة من ماله أو نسبة من حصته في الفلج، أو غرفة في بيته لطحن الحبوب أو أي شيء يرى فيه عائداً مادياً أو خدمة ينتفع منها الناس، قيل أن أنواع الوقوفات في حارة العقر وحدها تصل إلى 70 نوعاً، وحفاظاً على الأوقاف فقد حرصت الحكومات المتعاقبة في عمان منذ القدم على تعيين وكيل نزيه أمين لكل وقف، ويحُاَسب من قبِلَ المسؤولين

<!-- PDF page 44 -->

بشكل مستمر، وما يزال هذا العمل جارياً إلى يومنا هذا.

ولقد كانت هذه الأوقاف على مر التاريخ سبباً في انتشار العلم والعلماء والكتب والمكتبات وكفيلة بأن تكون أيضا معينا للفقراء والمساكين في حياتهم.

<!-- PDF page 45 -->

### مجرى الأودية

تتركز أغلب المدن والقرى العمانية عند مجاري الأودية التي تنحدر من جبال عمان في شمالها وجنوبها، فهي الشريان الذي يغذي الأرض بالمياه، وفي مدينة نزوى وفي وسط سوقها تمر مجموعة من الأودية الكبيرة التي تنحدر من الجبل الأخضر وتقطع عشرات الكيلومترات قبل وصولها إلى مركز المدينة، وتقسم الولاية إلى قسمين فيقطع الوادي الطريق بين حارتي سعال و العقر، وعند هبوط الأودية يبقى جريانها لساعات قبل أن يضعف ثم يستمر جريانه الخفيف أحيانا لبضعة أيام مشكلِّة بذلك أنهارا جميلة في الولاية، وأشهر الأودية التي تمر من سوق نزوى: وادي الهجري وهو أكبرها وأغزرها ويخرج من قرية تنوف، وأيضا وادي المصلة والسويحرية وكمه وسميط ويسمى قديما مجموع هذه الأودية إذا وصلت سوق نزوى بوادي الأبيض، وتلتقي بوادي كلبوه قبيل دخولها السوق مع بعض الشعاب الأخرى، ويعد وادي كلبوه من أهم الأودية في عمان نظرا للمناطق والولايات الكثيرة التي

<!-- PDF page 46 -->

تستفيد وتخصب من هبوطه بسبب بطنه الرملي الذي يخزن كميات كبيرة جدا من المياه الجوفية، وهو الوادي الذي غرق فيه إمام عمان الوارث بن كعب الخروصي في قصته المشهورة، حيث نزلت أمطار غزيرة سال على إثرها وادي كلبوه وزاد منسوبه عن المعتاد لقوة جريانه، وكان في الضفة الأخرى سجن فيه عدد من المساجين فأخبر الإمام أن الوادي سيصل للسجن وقد يغرق المساجين، فأمر الإمام بإطلاق سراحهم، ولكن لم يجرؤ أحد على تخطي الوادي

فقال الإمام هم أمانتي وأنا سأذهب إليهم فإني سأسأل عنهم يوم القيامة فخاطر بنفسه فجرفه الوادي لقوته وقيل أنه جرف الكثير ممن لحقوا به. وهذا هو خلق وورع أئمة عمان وخوفهم على رعيتهم فعلى الرغم من أن المساجين سجنوا لجرم ارتكبوه إلا أن الإمام لم يفكر في روحه قط، وفقد حياته إثر ذلك. وقد وجدت جثة الإمام بعد انحسار منسوب الوادي ودفن في نفس المكان، وما يزال قبره معروف إلى اليوم.

<!-- PDF page 47 -->

[صورة] صورة قديمة من منطقة سعال لجرفة 82 التاريخية [صورة] قبر الإمام الوارث بن كعب الخروصي

<!-- PDF page 48 -->

[صورة] فلج دارس

### فلج ضوت

[صورة] فلج ضوت

هو أحد الأفلاج القديمة في ولاية نزوى، حيث يزيد عمره عن 1200 سنة حسب أقدم ذكر وجد عنه في المخطوطات، وتنقسم الأفلاج في السلطنة إلى العيني الغيلي والداودي، وتتميز الأفلاج ـ في عموم سلطنة عمان ـ

<!-- PDF page 49 -->

بالهندسة العجيبة، وبطريقة حفرها وقوة صبر الأجداد وإرادتهم في شقها من باطن الأرض لمسافات طويلة، حيث تجد طول قناة الفلج أحيانا ممتدة إلى عشرات الكيلومترات من عينه إلى أول منطقة يسقي فيها، وهذه القنوات الطويلة توجد بينها فتحات موزعة بطوله يستفاد منها أثناء عمليات الصيانة للتنفس والنزول والصعود وحمل الأتربة. ورغم صعوبة الحفر سابقاً لبساطة الأدوات وفي سواقي ضيقة ومظلمة، إلا أننا نجد عملاً راقياً يحتار فيه العقل ويعجز اللسان عن وصفه، وندرك به عظمة العمانيين وقوة إرادتهم في تسخير الطبيعة لخدمتهم، ويعد هذا الفلج من الأفلاج المتوسطة في نزوى من حيث قوة الجريان إذ يعد فلج دارس الأكبر والأشهر في عمان وكلما زادت قوة فلج دارس كان ذلك عاملاً إيجابياً لفلج ضوت.

### الآبار

لا يخلو البيت العماني قديما من بئر ماء خاصة به، تستخدم للشرب والاستحمام والطبخ والغسيل، وتتميز هذه الآبار عن آبار المزارع بضيق قطرها، إذ لا يزيد عن متر واحد في المتوسط، بينما يصل قطر آبار المزارع أحيانا إلى 3 أو 4 أمتار، وبعمق يصل إلى 20 متراً، ينقص ويزيد حسب توفر المياه في ذلك المكان، ويتميز ماء الآبار والأفلاج بدفئه في الشتاء وبرودته في الصيف.

[صورة] نموذج للأبار: الأولى موجودة بداخل إحدى البيوت دائرية الشكل يصل قطرها إلى متر واحد، والأخرى إحدى آبار المزارع مربعية الشكل يصل قطرها 4.5 متر ويظهر جليا الصف العجيب في الحجارة والتي يصل وزن الحجر الواحد منها أكثر من 40 كيلو جرام.

<!-- PDF page 50 -->

### احتفالات عيدي الفطر والأضحى

يزدان سوق نزوى في أيام العيدين بالاحتفالات الشعبية وعرصات بيع ألعاب الأطفال ومختلف أنواع المأكولات السريعة التي تصنع في المنازل والتي قد لا تجدها في باقي أيام السنة، ولأن نزوى مدرسة للتجار فإنك ستستمتع بالتعامل مع مئات التجار ممن هم دون الثامنة عشر حيث جل الباعة هم من العمانيين وقد يكون

<!-- PDF page 51 -->

عمر بعضهم العاشرة أو الثامنة ورغم ذلك تجد لديهم الجرأة والشجاعة والحماس والخبرة في التعامل، وهذه العادة قديمة في هذه المناسبة ويقصدها أغلب الأهالي مصطحبين معهم أبناءهم وأطفالهـم، يحفـظ الأطفـال وقت مناسبة العيد السعيد منذ نعومة أظافرهم ولا يساومون عليها شيئاً آخر، مع فرحتهم بمالهم الذي حصلوا عليه من عيدية العيد.

### متحف أبي المؤثر

يقع هذا المتحف فوق صباح أبي المؤثر مع جزء من سور العقر، يستطيع الزائر له تجربة المشي على سور العقر ومشاهدة الغرفة التي كانت تستخدم للحراسة مع الصعود على أحد الأبراج، كما سيتعرف أيضاً على معلومات تاريخية مهمة ومعرفة طرق الحراسة والحماية قديماً.

<!-- PDF page 52 -->

### ساعة المدة

هي ساعة تستخدم لقياس نصيب المزارعين من ماء الفلج، وبها عدة قياسات منها الأثر الذي يعادل (نصف ساعة)، ونصف أثر الذي يعادل (ربع ساعة)، وربع أثر الذي يعادل (سبع دقائق ونصف). وهي عبارة عن قطعة خشب من أحد الأشجار يتم تثبيتها في الأرض، وتوضع القياسات حول قطعة الخشب، وتسُتخدم هذه الساعة من طلوع الشمس صباحا حتى غروبها مساء وذلك من خلال الظل الذي ينعكس على الأرض من قطع الخشب. وفي الليل يقُاس نصيب المزارعين من ماء الفلج بأداة تسمى (السحلة) وهي عبارة عن إناء مصنوع من النحاس به ثقب صغير في الأسفل، حيث يحُضر إناء كبير مملوء بالماء وتوُضع (السحلة) وهي فارغة فوق الإناء المملوء بالماء، بحيث يدخل الماء إلى (السحلة) من خلال الثقب

الموجود في الأسفل وعند امتلاء (السحلة) يكون قد حصل المزارع على نصيبه من الفلج، وكذلك توجد عدة أحجام (للسحلة) منها الأثر ونصف الأثر وربع الأثر.

ويقوم بمتابع الساعة والقياسات شخص يسمى (عريف الفلج) فهو المسؤول عن توزيع ماء الفلج على المزارعين، وتقع هذه الساعة أمام مدرسة الجلجلان لتعليم القرآن الكريم الواقعة خلف مسجد الشواذنة. وهي خاصة بفلج ضوت ولكل فلج طريقته، ولم نجد لها صورة وإنما وجدنا في ولايات أخرى، فقد اندثرت بتوقف استخدامها وبقي مكانها فقط.

<!-- PDF page 53 -->

[صورة] صورة ليلية لسوق نزوى

### سوق نزوى

يرتبط سوق نزوى بحارة العقر والمسجد الجامع والقلعة الشهباء ارتباطاً وثيقاً، ومنذ القدم كان حصن نزوى ثم القلعة وهما المقر السياسي للدولة كفيلين بأن ينُشأ حولهما سوق كبير ورئيسي للمنطقة، ولا يعرف عمر هذا السوق سوى أنه من أهم الأسواق العمانية قديما وحديثا، ولعراقته والقوة الشرائية فيه ضربت به قديماً الكثير من الأمثلة الدالة على ذلك، وفاز في عام 1992م بأفضل تصميم هندسي معماري، ويميزه في الوقت الحاضر أن جل الباعة فيه من العمانيين، وهو سوق لا تكسد فيه البضائع رغم كثرتها وتعددها، ويسع الجميع العمل فيه صغيرهم قبل كبيرهم، ويعتبر صباح الجمعة هو الوقت المثالي لزيارة السوق لازدحامه اللافت وتعدد البضائع، ومن أهم الأسواق الصغيرة التابعة لسوق نزوى وأشهرها نشاطاً وحيوية في الوقت الراهن:

<!-- PDF page 54 -->

1 ـ السوق الشرقي (الصنصرة):

وهو سوق يوفر جميع البهارات والتوابل والعطريات و الأدوية العمانية التقليدية والزيوت المحلية، مع بعض المواد النادرة التي تستخدم في الطبخ والزارعة والعلاج، كما يحتوي على الكثير من المستلزمات التي أصبحت لا تباع إلا فيه لقلة السؤال عنها.

[صورة] صورة قديمة لسوق الصنصرة من الباب الغربي

<!-- PDF page 55 -->

2 ـ سوق الفضة والحرفيين:

منذ القدم اشتهرت نزوى بصياغة الذهب والفضة، وما تزال محافظة عليها إلى اليوم، وتتوزع محلات الفضة بالقرب من مدخل قلعة نزوى، وتوجد مجموعة منها بجانب سوق الأسلحة، وأهم ما توفره هذه المحلات هي الخناجر العمانية بمختلف أنواعها النزواني والسعيدي (الصافاني)، وكذلك مستلزمات صياغتها وإصلاحها، والصياغة النسائية التقليدية والحديثة بصناعات محلية ومستوردة وبأشكال مختلفة، كما توفر خدمة الصياغة والتصليح لكل طلبات الزبائن.

<!-- PDF page 56 -->

3 ـ سوق الذهب:

ويقع شمال القلعة وغرب الجامع على شكل شريطين يفصل بينهما الشارع، ويعد واحدا من أهم أسواق الذهب في السلطنة؛ حيث يخدم جميع المحافظات ويوفـر مختلف الصياغات التي تحتاجها المرأة سواء المحلية منها أو المستوردة.

4 ـ سوق الأسلحة:

ويقصد به الأسلحة التقليدية المسموح تداول شرائها في السلطنة، وهذا السوق يوفـر هذه الأسلحة بالإضافة إلى توفير احتياجاتها من الذخيـرة والاكسسوارات وخدمة

الصيانة والتنظيـف، وفي صبـاح كل جمعـة يقُام مـزاد علني لبعض هذه الأسلحة التي تأتي للسوق مـن الزبائن مباشرة.

5 ـ سوق الجمعة:

وهو سوق مفتوح للجميع، يمكن لك أن تعرض مـا تريــده مـن البضائع المسموح بها قانونياً وعرفياً، وأكثر ما يعرض فيـه السيارات والأثــاث والأواني المنزليـة والبخور والملابس وغيرهـا، ويبدأ منذ الساعات الأولى من صباح يوم الجمعة إلى الساعة الحادية عشرة صباحاً.

<!-- PDF page 57 -->

6 ـ سوق التمور والحلوى العمانية:

تشتهر ولاية نزوى بزراعة أجود أنواع النخيل وبصناعة الحلوى العمانية؛ لذلك يتميز سوقها بالكثير من معارض بيع الحلوى التي تقدم في الضيافة العمانية مع التمر والقهوة، وهي أيضا هدايا فاخرة إذ تعلب في أواني فاخرة يميل شكلها إلى الموروث العماني غالباً، كما توجد معارض بيع التمور الطازجة والمجففة مع مشتقاتها من الصناعات كالدبس والمدلوك والمعمول.

ويضم السوق أيضاً الكثير من البضائع التي يحتاجها البيت العماني كاللحوم والدواجن والأسماك والخضروات والفواكه والعطريات والملابس وغيرها، وبقي محافظا على خدمات تقليدية قديمة والتي اندثر بعضها من أغلب الأسواق، ونذكر مثالا عليها:

الصفاّرون والحدادون: وهم الذين يقومون بصناعة الأواني المنزلية النحاسية وإصلاحها، ويقومون بصناعة السكاكين والسيوف والسواطير وسنها.

الصاغة: هم الذين يقومون

بإصلاح الذهب والفضة

والخناجر.

مصلح الأحذية (الإسكافي):

هم الذين يقومون بتصليح

الأحذية وخياطتها بالإضافة إلى

الصناعات الجلدية كتفصيل

الغمد للسكين وبعض الإحتياجات الحيوانية والزراعية.

<!-- PDF page 58 -->

بإلاضافة إلى مختلف الخدمات التي أصبحت متوفرة في جميع مدن العالم كالخياطة والحلاقة وتفصيل الملابس وإصلاح الساعات والإلكترونيات وغيرها.

7 ـ مناداة الأغنام:

يضم سوق نزوى مختلف أصناف البضائـع، وجـزء كبير منها يباع بطريقة المزاد الجماعي في صباح يوم الجمعة من كل أسبوع، وفي الأيام الأخيرة التي تسبق عيدي الفطر والأضحى، ومن ذلك عرصة بيع الأغنام والأبقار التي تعرف محليا بالهبطة والمناداة، وتعتبر هذه العرصة هي الأشهر في السلطنة وأكثرها ازدحاماً، حيث

<!-- PDF page 59 -->

تجلب المواشي فيها من مختلف ولايات عمان بالإضافة إلى الباعة القادمين من القرى القريبة، فالأبقار تجلب بكثرة من محافظة ظفار كما تجلب كبيرة الحجم منها من محافظة شمال الباطنة، وتجلب الكثير من الأغنام من محافظات الشرقية والظاهرة والوسطى، ويبدأ المزاد من الساعة السابعة صباحا ببيع الأغنام ثم الأبقار لتستمر نحو 3 ساعات، ويتشارك فيها العشرات من الدلالين في وقت واحد، ليتشكل بذلك مشهد جميل يقصده الكثير من أهل الولاية وخارجها، وهي عادة قديمة في الكثير من المدن العمانية الرئيسية.

<!-- PDF page 60 -->

### مطعم العقر التراثي

لا تكتمل رحلة الزائر لحارة العقر دون زيارة هذا المطعم ليعود بك إلى الماضي العتيق، وكأنك نزلت ضيفاً في منزل عماني قديم، فتأكل المأكولات العمانية في مكانها الأصيل، ليكون غداؤك أو عشاؤك هو خاتمة جولتك السياحية.

<!-- PDF page 61 -->

شكراً من القلب إلى الأستاذ القدير محمد بن عبد الله السيفي على مراجعة هذه المادة وتصحيحها، وللمصور المبدع سامي بن سالم الهنائي لتكلفه عناء التصوير لعدة أيام، وللأخوه علي بن أحمد القسيمي وناصر بن محمد الفرقاني لتزويدي بالصور الحصرية القديمة، وإلى الدكتور الوليد بن زاهر السالمي الذي أعد لي مخطط سور العقر، والفاضل راشد بن عبد الله الفارسي مدير نزل نزوى التراثية وإلى خالي الأستاذ خالد بن عيسى السليماني للمراجعة النهائية للكتاب، ولكل من ساهم في إنجاح هذا العمل بحرف أو نصيحة.

<!-- PDF page 62 -->

بحمد الله وتوفيقه تم هذا العمل المتواضع والذي أريد به تعريف السائح عن تاريخ وآثار حارة العقر بمدينة العلم والعلماء وبيضة الإسلام نزوى ليكون مرشدا سياحيا له في تجواله بها وقد روعي في مادته أن يكون سهلا واضحا ومختصرا وجيزا كي تسهل قراءته للجميع، وشيقا حتى لا يمله القارئ وإلا فإن سرد تاريخ هذه الحارة يحتاج للكثير من المجلدات، علماً أن هذا الكتاب سيترجم إلى عدة لغات عالمية مع بعض التغيرات والإضافات في كل طباعة لتتناسب مع لغة وثقافة ذلك البلد لتحوي مقدمته ذكر أبرز العلاقات التاريخية بين البلدين، وسيكون في أول طباعة له بإذن الله في تسع لغات مختلفة.

<!-- PDF page 63 -->

المقدمة 5 تمهيد: حارة العقر 7 قلعة نزوى الشهباء 21 حصن نزوى 27 مسجد الشواذنة 29 مسجد مزارعة 33 جامع نزوى ومركز التعريف بالإسلام 37 نزل نزوى التراثية 41 سور العقر 45 البيت العماني في حارة العقر 54 حارة العقر في حكم دولة اليعاربة 56 الأبواب والأسقف 59 مدارس تعليم القران الكريم 65 المجالس 67 بيت الصاروج 69

<!-- PDF page 64 -->

شعار نزوى عاصمة الثقافة الإسلامية 71 تنور مزارعة 73 قبر الشيخ الأصم 75 مقبرة الفرس 77 مستشفى الطبيب تومس 79 قنوات تصريف المياه 81 السيارات السياحية 83 الأوقاف 85 مجرى الأودية 89 فلج ضوت 95 الآبار 97 احتفالات عيدي الفطر والأضحى 99 متحف أبي المؤثر 101 ساعة المدة 102 سوق نزوى 105 مطعم العقر التراثي 119 شكر وتقدير 121 الخاتمة 123 الفهرس 125
