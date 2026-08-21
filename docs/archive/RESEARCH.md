# حارة العقر / Harat Al-Aqr, Nizwa — source analysis & research notes

Compiled 20 Aug 2026. Two parts: (1) what the source material in this repo actually
contains, (2) what external sources add, corroborate, or contradict.

---

## 1. The source material

| File | What it is |
|---|---|
| `REFRENCE.pdf` | 65-page illustrated book, *حارة العقر* by سليمان بن محمد السليماني. Adobe InDesign CS5.5, created 11 Nov 2020. Publisher مكتبة خزائن الآثار (بركاء، عُمان), 1442 AH / 2021 CE, ISBN 978-9933-29-448-9. |
| `Ref.md` | **Broken.** A text dump of the PDF in *visual* glyph order — every line mirrored, ligatures mangled. Not usable as text. |
| `Ref.clean.md` | Rebuilt by `work/build_md.py` straight from the PDF glyph stream. ~35 k chars, 30 sections. |

### Why `Ref.md` is broken

The PDF stores Arabic in logical order but with a font whose `ToUnicode` table is
lossy. Whatever produced `Ref.md` read the glyph positions instead of the stream, so:

- every line came out reversed (`ةظوفحم قوقحلا عيمج` = `جميع الحقوق محفوظة`)
- lam-alef ligatures were flattened or transposed (`الإسلام` → `اإلسام`)
- U+00C9 `É` appears 1 334× as a justification-kashida artifact, inside words
- 2 988 consecutive U+FFFD on the last page

`work/build_md.py` fixes this geometrically rather than by guessing:

1. A glyph that maps to several characters emits them with **zero width** except one.
   Those runs are one ligature → reassembled in logical order.
2. A lam-alef ligature whose `ToUnicode` collapsed to a bare alef shows up as an alef
   with width > 0.45 em (normal alef ≈ 0.2 em). Its lam is restored.
3. Characters re-sorted right-to-left; Latin/digit runs flipped back to LTR (this is
   what puts `سنة 1650م` back where it belongs instead of at the line start).
4. Lines regrouped into columns (several pages are two-column) and into paragraphs.

Residual known imperfections, all noted in the file header: poetry diacritics on PDF
pages 13 and 32 are scrambled beyond geometric repair; Qur'anic verse on page 17 is set
in a private-use font and comes out as `ﮙ ﮚ ﮛ…`; photographs are not extracted, marked
`[صورة]`; four words are hand-corrected against the rendered page (see `CORRECTIONS`).

### Book structure (30 sections)

المقدمة · حارة العقر · قلعة نزوى الشهباء · حصن نزوى · مسجد الشواذنة · مسجد مزارعة ·
جامع نزوى ومركز التعريف بالإسلام · نزل نزوى التراثية · سور العقر · البيت العماني في حارة
العقر · حارة العقر في حكم دولة اليعاربة · الأبواب والأسقف · مدارس تعليم القرآن الكريم ·
المجالس · بيت الصاروج · شعار نزوى عاصمة الثقافة الإسلامية · تنور مزارعة · قبر الشيخ الأصم
· مقبرة الفرس · مستشفى الطبيب تومس · قنوات تصريف المياه · السيارات السياحية · الأوقاف ·
مجرى الأودية · فلج ضوت · الآبار · احتفالات عيدي الفطر والأضحى · متحف أبي المؤثر · ساعة
المدة · سوق نزوى · مطعم العقر التراثي

The author states in the conclusion that the book was written as a **tourist guide**
(`مرشدًا سياحيًا`), deliberately short, and was to be published in **nine languages** with
per-language additions covering historic ties between Oman and the target country.

---

## 2. Facts asserted by the book

### Dates

| Date | Event |
|---|---|
| pre-Islam | Al-Aqr already settled (author's reading of the site evidence) |
| 9 AH | مسجد الشواذنة built — "second mosque built in Oman" |
| 2nd c. AH (~1200 yrs) | حصن نزوى begun under Imam محمد بن عبد الله بن أبي عفان; جامع نزوى founded on Wadi Kalbuh |
| 3rd c. AH | مسجد مزارعة built; fort extended under Imam الصلت بن مالك الخروصي |
| 7th c. AH | الشيخ الأصم (أبو عبد الله عثمان بن عبد الله بن أحمد العزري) |
| 853 AH | flood destroys the older Al-Aqr wall |
| 936 AH | mihrab of مسجد الشواذنة carved and signed |
| 1650 CE | Imam سلطان بن سيف اليعربي expels the Portuguese; Nizwa Fort funded from the Diu campaign booty, 12 years to build |
| 2nd half 11th c. AH | present سور العقر founded by Imam سلطان بن سيف, 7 years to build |
| 1 Dhu al-Hijja 1150 AH | ~4 000 Persian troops enter Nizwa; ambushed inside the quarter → مقبرة الفرس |
| 1902 | dated photograph of Nizwa Fort |
| 1950s (implied) | British air-force rockets hit the fort, "only slight" damage |
| 1992 | Nizwa Souq wins a best-architectural-design award |
| 2003 | مسجد الشواذنة restored by وزارة التراث |
| 2015 | Nizwa is Capital of Islamic Culture; commemorative tower built at the souq front |
| 1 Dhu al-Qa'da 1439 / 23 Apr 2018 | نزل نزوى التراثية opened by the Wali of Nizwa, الشيخ حمد بن سالم بن سيف الأغبري |
| 2020 | مسجد مزارعة restored from its own waqf |

### Measurements

- **Wall (سور العقر):** ~2 km; 1.5–2 m thick; 5–6 m high; 15 towers, 150–200 m apart;
  tower bases 4–5 m diameter, mostly cylindrical, some square.
- **Gates (صباح):** four — أبي المؤثر (S), الشجبي (W), السوق (NE), الصبخة (E).
  **صباح السوق was demolished** during fort/souq restoration; only photos survive.
- **Towers named:** المذبحة، ميرزة (بستان قسام)، بلج، خريص بلج، العلياء، غوير، الكوارج،
  محمود، السوق، القلعة، بستان العقر الشرقي/الغربي (سكة القبر)، الصبخة، قطعة الطوي،
  حارة الزامة الشرقي/الغربي. Wall map drawn by د. الوليد بن زاهر السالمي.
- **Houses:** 300+, 60–200 m²; five sub-quarters, each with a مجلس/سبلة
  (سبلة الكوارج، سبلة النيري named).
- **Wells:** house wells < 1 m diameter; farm wells 3–4 m wide, up to 20 m deep.
- **Waqf:** ~70 distinct types of endowment in Al-Aqr alone.
- **ساعة المدة:** الأثر = ½ hour, نصف أثر = ¼ hour, ربع أثر = 7½ minutes; night shares
  measured with السحلة, a pierced copper vessel; administered by عريف الفلج. Stood in
  front of مدرسة الجلجلان behind مسجد الشواذنة, specific to فلج ضوت. **Now gone** — the
  author notes no photograph of it could be found.

### Named people worth indexing

Author سليمان بن محمد السليماني (from قرية العقر, and — see below — now manager of the
Al-Aqr waqf). Reviewer محمد بن عبد الله السيفي, author of *الحلل السندسية في الكتابات
المسجدية*. Photographer سامي بن سالم الهنائي. Archive photos: علي بن أحمد القسيمي,
ناصر بن محمد الفرقاني. Wall map: د. الوليد بن زاهر السالمي. Director of Nizwa Heritage
Inn: راشد بن عبد الله الفارسي. Final review: خالد بن عيسى السليماني.
Historic figures: Imams سلطان بن سيف اليعربي، الصلت بن مالك الخروصي، الوارث بن كعب
الخروصي (drowned in Wadi Kalbuh freeing prisoners)، محمد بن عبد الله الخليلي (cured of
blindness by the American Dr. Thomas)؛ الشيخ سيف بن محمد الفارسي (the رائية poem)؛
السيد طارق بن تيمور البوسعيدي, father of Sultan Haitham, once resident in بيت الصاروج.

---

## 3. What external sources add

### Current state of the quarter (this is the big gap — the book stops at 2021)

| Figure | Value | As of |
|---|---|---|
| Heritage houses restored | **89** | Dec 2025 |
| Youth business projects | **81+** (78 in an earlier count) | Dec 2025 |
| Direct jobs | **400+** (300+ earlier) | Dec 2025 |
| Visitors | **600 000** in Q1 alone | 2023 |
| Rehabilitation began | **2017** (wall works from Jan 2020) | — |
| Visitors after the wall opened | **3 000–5 000 per day** | 2024 |
| Al Dakhiliyah heritage/tourism sites | **415 081 visitors** | full-year 2024 |
| Nizwa Heritage Inn capacity | 3 houses in phase 1, بيت الصاروج converted to 10 rooms, **36 rooms total** | — |

- Developer: **شركة بوارق نزوى الدولية للاستثمار** operating **نزل نزوى التراثية**; also
  the first operator of electric tourist buggies in the Sultanate.
- The book's author, **سليمان بن محمد السليماني, is named in the press as مدير/وكيل أوقاف
  العقر بنزوى** — he is not merely a chronicler of the quarter but currently running its
  endowment. Useful if you need a primary contact or permissions.
- Officials to cite: الشيخ صالح بن ذياب الربيعي (Wali of Nizwa), الشيخ هلال بن سعيد الحجري
  (Governor of Al Dakhiliyah), أحلام بنت حمد القصابية (Director of Heritage & Tourism,
  Al Dakhiliyah), أحمد بن صالح الراشدي (Undersecretary, Ministry of Endowments),
  د. إسحاق بن هلال الشرياني (adviser to the Al-Aqr waqf).

### Wall restoration, phase by phase

Work began **January 2020** — the third major restoration in the wall's history — led by
بوارق نزوى الدولية with the wall's custodians. Current specification as restored:
**~2 000 m, 16 towers**, running from صباح الصبخة to برج حارة الزامة الغربي.

| Phase | Opened | Detail | Cost |
|---|---|---|---|
| 1 | Jan 2024 (wall & square, 8 Jan) | first restored stretch | **OMR 400 000** |
| 3 | Dec 2024 | 275 m, incl. a **75 m step-free accessible entrance** for wheelchairs and strollers | **OMR 370 000**, 4 months |
| 4 | 29 Dec 2025 | electric lift, tower restorations | — |

Total expected cost of the full wall restoration: **OMR 2.5–3 million**. Alongside it,
**Al Aqr Plaza** offers commercial and cultural services including **VR exhibits and 3D
models** of the historic quarter. A separate **paving project** — replacing asphalt with
flat stone, plus water, sewerage and fibre — costs ~**OMR 340 000**, funded by the
governorate, was 60 % complete in Sept 2025 and is **due to finish at the end of 2026**.

### 2026 specifically

- **3 Jan 2026** — second *مسير نزوى السياحي* (Nizwa tourist walk), **3 000+ participants**,
  under the patronage of the Minister of Economy سعيد بن محمد الصقري, organised by the
  Oman Chamber of Commerce (Al Dakhiliyah branch) with فريق الصمود للمغامرات of Nizwa
  Club. The route went through Harat Al-Aqr and along its wall, and took in **فلج ضوت**
  alongside Daris, Al-Ghantaq, Al-Khoubi and Al-Sa'ali — the same falaj the book
  documents.
- **12 Mar 2026 — MIPIM Awards, Cannes. Al-Aqr did *not* win.** It was shortlisted in the
  **Best Urban Regeneration** category (التجديد العمراني); that category went to
  **Nordhavn, Copenhagen**. Ten category winners plus a Special Jury Award (Sydney Fish
  Market); Paris took the most. Al Thuraya City (Muscat), the other Omani finalist, also
  did not win. Being one of 40 finalists from 19 countries is still quotable — winning is
  not.
- **17 Mar 2026** — Oman Observer feature on Omani historic quarters as tourist
  destinations; context only, no new Al-Aqr figures.
- **22–23 Apr 2026 — Shell Oman dedicates the 7th edition of *هدية شل للوطن* to Harat
  Al-Aqr.** Launched at **متحف عمان عبر الزمان** in Manah under the patronage of the
  Minister of Finance **سلطان بن سالم الحبسي**. Three pillars: restore the **remaining**
  stretch of wall plus heritage buildings and pathways; build an **integrated visitor
  centre**; connect the quarter to **solar power** (framed against Oman Vision 2040). A
  fourth strand funds entrepreneur/SME capacity building. Delivered with أوقاف عقر نزوى,
  the Governor's office and the Ministry of Heritage & Tourism. Named: **علي الجنيبي**
  (Country Chairman, Shell Oman), **د. إسحاق بن هلال الشرياني** (waqf adviser),
  **الأحنف الزبيدي** (Social Investment Manager, Shell Oman). **No budget disclosed.**
- **May–Aug 2026** — nothing found. The next expected milestones are the paving project
  completing at end-2026 and the Shell visitor centre.

### Corroborations

- Wall history (853 AH flood → refounded by Imam Sultan bin Saif → second half of the
  11th c. AH → 7 years to build), the four صباح gates, the 150–200 m tower spacing, the
  1.5–2 m thickness and 5–6 m height: Oman Daily reproduces these **exactly** as in the
  book. Treat the press coverage as downstream of the same source, not independent.
- فلج دارس is the largest falaj in Oman — canal length **7 990 m**, داوودي type, one of
  **five Omani aflaj inscribed on the UNESCO World Heritage List in 2006**. Nizwa has
  **17 aflaj** in total. This corroborates and dates the book's claim that Falaj Dawt's
  flow tracks Falaj Daris.
- Nizwa: largest city of Ad Dakhiliyah, ~140 km from Muscat, population ≈ 83 500,
  Capital of Islamic Culture 2015.

### Discrepancies — resolve these before publishing anything

1. **مسجد الشواذنة founding date.** Book: **9 AH**. Arabic Wikipedia and Oman Daily:
   **7 AH**. Al-Watan: **8 AH**. All agree on the 936 AH / 1529 CE mihrab and the 2003
   restoration. The book's "second mosque built in Oman" claim also needs a source.
2. **Age of the quarter.** Book implies pre-Islamic settlement. Press variously says
   1 200 years (Oman Observer / MIPIM material), 1 500 years, and 4 000 years
   (Al-Watan). No two agree.
3. **Wall length.** Book: "in the region of two kilometres". Oman Observer / Oman Daily:
   **1 950 m**. Recent Omani coverage: **2 000 m**.
4. **Towers and gates.** Book: 15 towers, 4 gates. Recent official coverage:
   **16 towers, 3 gates** — consistent with the book's own note that صباح السوق was
   demolished, but the tower count differs.
5. **Who began حصن نزوى.** Book: Imam محمد بن عبد الله بن أبي عفان, 2nd c. AH. Most
   reference works: Imam **الصلت بن مالك الخروصي**, 3rd c. AH / 9th CE. The book has him
   only as the extender. For the *wall*, Al-Sahwa dates al-Salt's original to **237 AH**
   and the Ya'rubi rebuild to **1050 AH**, which is compatible with the book's "second
   half of the 11th century AH".
6. **Fort construction dates.** Book: 12 years, after the 1650 expulsion. Arabic
   Wikipedia and others: begun **1656**, finished **1668**.
7. ~~Restoration cost.~~ **Resolved.** The "RO 4,000" in the Oman Observer English piece
   is a garble. Al-Sahwa (Jan 2024) gives **OMR 400 000 for phase 1** and **OMR 2.5–3 m
   for the whole wall**; Oman Daily's "over OMR 3 million" is the full-project figure, not
   a 700 m figure. Quote phase costs, not the total, unless you mean the total.

### Not yet verified

- مقبرة الفرس / the 1150 AH massacre — no independent source found in this pass.
- قبر الشيخ الأصم and the "deaf sheikh" anecdote — book only.
- The 1992 souq architecture award — no citation found; the awarding body is unnamed.
- مستشفى الطبيب تومس — the American mission doctor is almost certainly **Dr. Wells
  Thoms** of the Arabian Mission, but this needs confirming and the spelling fixing.
- ساعة المدة — the book says no photo exists; worth checking whether one has since
  surfaced from another wilayat, since the book says surviving examples exist elsewhere.

---

## Sources

- [حارة العقر التاريخية بولاية نزوى — جريدة عمان](https://www.omandaily.om/print-article?articleId=1150773)
- [حارة العقر بنزوى من حارة مهجورة إلى حارة تعج بالحياة — الوطن](https://alwatan.om/details/473663)
- [Nizwa: Bridging sustainable development and heritage — Oman Observer](https://www.omanobserver.om/article/1171723/oman/nizwa-bridging-sustainable-development-and-heritage)
- [Al Aqr, Al Thuraya projects shortlisted for the MIPIM Awards — Oman Observer](https://www.omanobserver.om/article/1183945/oman/al-aqr-al-thuraya-projects-shortlisted-for-the-prestigious-mipim-awards)
- [Restored Al Aqur wall now pride of Nizwa — Oman Observer](https://www.omanobserver.om/article/1148249/features/restored-al-aqur-wall-now-pride-of-nizwa)
- [افتتاح المرحلة الرابعة من مشروع سور العقر في نزوى — وجهات](https://wejhatt.com/?p=113362)
- [إطلاق مشروع تطوير حارة العقر بولاية نزوى — جريدة عمان](https://www.omandaily.om/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF%D9%8A%D8%A9/na/%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D9%85%D8%B4%D8%B1%D9%88%D8%B9-%D8%AA%D8%B7%D9%88%D9%8A%D8%B1-%D8%AD%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%B9%D9%82%D8%B1-%D8%A8%D9%88%D9%84%D8%A7%D9%8A%D8%A9-%D9%86%D8%B2%D9%88%D9%89)
- [بوارق نزوى: توقيع اتفاقيات لتطوير نزل نزوى التراثية — جريدة عمان](https://www.omandaily.om/print-article?articleId=15704)
- [مسجد الشواذنة — ويكيبيديا](https://ar.wikipedia.org/wiki/%D9%85%D8%B3%D8%AC%D8%AF_%D8%A7%D9%84%D8%B4%D9%88%D8%A7%D8%B0%D9%86%D8%A9)
- [قلعة نزوى — ويكيبيديا](https://ar.wikipedia.org/wiki/%D9%82%D9%84%D8%B9%D8%A9_%D9%86%D8%B2%D9%88%D9%89)
- [فلج دارس (نزوى) — ويكيبيديا](https://ar.wikipedia.org/wiki/%D9%81%D9%84%D8%AC_%D8%AF%D8%A7%D8%B1%D8%B3_(%D9%86%D8%B2%D9%88%D9%89))
- [Nizwa — Wikipedia](https://en.wikipedia.org/wiki/Nizwa)
- [Archnet: Al-Aqur](https://www.archnet.org/sites/22148) (403 on fetch — open in a browser)

2026 sources:

- [MIPIM Awards 2026 — Winners](https://www.mipimawards.com/mipimawards2026/en/page/winners-2026) (confirms Al-Aqr did not win)
- [11 sustainable projects named winners of 2026 Mipim Awards — Real Asset Insight](https://realassetinsight.com/2026/03/13/11-sustainable-projects-named-winners-of-2026-mipim-awards/)
- [Harat Al Aqur to get facelift with new initiative — Oman Observer, 22 Apr 2026](https://www.omanobserver.om/article/1188397/oman/harat-al-aqur-to-get-facelift-with-new-initiative)
- [إطلاق النسخة الـ7 من "هدية شل للوطن" لدعم تطوير حارة العقر — وجهات، 23 أبريل 2026](https://wejhatt.com/?p=117402)
- [مسير نزوى السياحي يستكشف المقوّمات السياحية بالولاية — جريدة عمان، 3 يناير 2026](https://www.omandaily.om/ampArticle/1193751)
- [Oman's historic neighbourhoods revived as vibrant tourist destinations — Oman Observer, 17 Mar 2026](https://www.omanobserver.om/article/1186334/oman/tourism/omans-historic-neighbourhoods-revived-as-vibrant-tourist-destinations)
- [سور العقر بنزوى يستعيد أمجاده — الصحوة](https://alsahwa.om/?p=206243) (phase costs, 16 towers, daily visitors, Al Aqr Plaza)
- [تواصل مشروع تبليط حارة العقر واستبدال الأسفلت بالحجارة المسطّحة — جريدة عمان](https://www.omandaily.om/%D8%B9%D9%85%D8%A7%D9%86-%D8%A7%D9%84%D9%8A%D9%88%D9%85/na/%D8%AA%D9%88%D8%A7%D8%B5%D9%84-%D9%85%D8%B4%D8%B1%D9%88%D8%B9-%D8%AA%D8%A8%D9%84%D9%8A%D8%B7-%D8%AD%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%B9%D9%82%D8%B1-%D8%A8%D9%86%D8%B2%D9%88%D9%89-%D9%88%D8%A7%D8%B3%D8%AA%D8%A8%D8%AF%D8%A7%D9%84-%D8%A7%D9%84%D8%A3%D8%B3%D9%81%D9%84%D8%AA-%D8%A8%D8%A7%D9%84%D8%AD%D8%AC%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D9%85%D8%B3%D8%B7%D8%AD%D8%A9)
- [المحروقي يجتمع مع اللجنة الرئيسية لتطوير حارة العقر — وجهات](https://wejhatt.com/?p=104252) (phase 3 detail)
- [@awqafnizwa on X](https://x.com/awqafnizwa) — the Al-Aqr endowment's own account; confirms the MIPIM category was التجديد العمراني
