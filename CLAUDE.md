# ALAQUR — حارة العقر website

Building a **static bilingual website** about Harat Al Aqur, the walled historic quarter
of Nizwa, Oman. Part encyclopedia (from a 2021 book), part visitor guide.

All research, content extraction and translation are **done**. What remains is the build.

---

## Decisions already locked

| | |
|---|---|
| **Stack** | Astro — static output, real `/ar/` + `/en/` routing, shared components |
| **Languages** | **Arabic is primary**, English secondary via a toggle. `lang` + `dir` set per page, never swapped by JS |
| **Routing** | `/ar/<slug>` and `/en/<slug>` share a slug, so the toggle maps page-to-page instead of dumping the visitor at the homepage |
| **Scope** | Heritage archive **plus** practical visitor guide |
| **Photography** | Book images for cards and inline figures; hero images need new photography (see the resolution ceiling below) |
| **Translation** | Complete, by Claude, in `content/en/` |
| **Romanization** | **Al Aqur** / **Harat Al Aqur** throughout. Omani terms italic on first use with a gloss: *sabah* (gate), *sablah* (meeting room), *falaj* (irrigation channel), *sarooj* (Omani hydraulic mortar), *khanjar* |
| **Hosting** | Assume a domain root (Cloudflare Pages / Netlify). Confirm before assuming base paths |

## Decisions settled during the build

1. **Visual direction: أ — الطين والظل / Clay & Shadow.** Tokens live in
   `src/styles/global.css`; they were lifted from `design/Main.dc.html`. Change a value
   there, never in a page.
   **The ink ramp is set by contrast, not by eye.** `--ink-faint` used to fail WCAG AA
   (3.1–3.4:1) everywhere it was printed, and it carries labels at .68–.85rem, which is
   body size for contrast purposes — the 3:1 large-text allowance never applies. The ramp
   is now `--ink` 0.260, `--ink-muted` 0.460, `--ink-faint` 0.525, and `--clay` moved to
   0.535 so links clear AA on the sunk panels too. **Run `python work/check_contrast.py`
   after touching any colour token**; it parses the stylesheet itself, checks both themes,
   and exits non-zero on a failure. It only knows the pairings listed in its `PAIRS` — if
   you print a token on a new surface, add the pair.
   **`--rule` and `--rule-light` are decorative hairlines and are deliberately below 3:1.**
   That is allowed: nothing depends on seeing them. Interactive controls take
   `--rule-strong`, which does owe 3:1 under WCAG 1.4.11. Do not border a control with
   `--rule`.
   **Two tokens sit either side of the theme.** `--ink-invert` is light in BOTH themes and
   means "text on an always-dark surface" (the hero scrim). `--on-clay` is text on a clay
   fill and FLIPS, because clay itself lightens in dark mode. Using the wrong one only
   breaks in one theme, which is how it goes unnoticed.
   **Dark mode is a re-lighting, not a second design.** Only colour tokens are redefined
   under `prefers-color-scheme: dark`; every measurement is shared. Hover goes *brighter*
   on dark, so `--clay-deep` keeps meaning "more emphatic" rather than literally darker.
   Anything hardcoded rather than tokenised will not follow — the 3D map's floating labels
   were near-white text on a near-white chip until they were switched to `--surface`.
2. **The wall map is built and the plan is traced**, in both flat and 3D form.
   `/{lang}/map` draws the real circuit, clickable, from `content/data/wall-plan.json`.
   **Dr Al Salmi's plan is `assets/photos/p23-1.jpeg`** (753×871, PDF page 23) — it had been
   sitting in the wall entry's gallery classified as an ordinary photograph. It is a raster,
   not vector, so `work/trace_wall_plan.py` recovers the geometry by colour: the circuit by
   closing the dashed stretches and taking what is enclosed, towers as mid-orange discs,
   gates as dark-red bars, with anything not touching the circuit discarded so the fort's
   round tower is not mistaken for a wall tower.
   **The plan draws 17 towers and 4 gates.** That count is stable across every threshold
   tested.
   **All 21 marks are named, from the plan's own legend.** Printed around the plan on the
   SAME PDF page (23) is a bilingual key, signed تصميم: الوليد بن زاهر السالمي. It names 14
   towers outright, 3 more that each share a gate ("صباح وبرج …"), and 1 gate alone —
   **17 towers and 4 gates, exactly what the drawing shows.** `legend_labels()` in
   `work/trace_wall_plan.py` reads each label's position off the PDF page, maps it into the
   plan image's frame, and assigns it to the nearest mark, closest pair first. Labels sit
   ~10–100 plan units from their mark while neighbouring towers are ~180 apart, which is
   what makes distance matching safe. Combined "gate and tower" labels are split into their
   two halves via `SPLIT_LABEL` rather than by string surgery.
   **This settles the tower count against the book's own text.** The prose says fifteen and
   the wall entry names fourteen; the plan and its legend say seventeen. The map page states
   all the figures and picks none.
   `TOWER_MATCHES` / `GATE_MATCHES` in `src/lib/wall.ts` are the six placements worked out
   from the book's prose *before* the legend was found. **All six agree with the legend**, so
   they are kept as corroboration — and as the rule for adding any future row: if you cannot
   write the evidence sentence, do not add it.
   **برج الكوارج and برج محمود are named in the book but not in its wall entry** — they
   appear only in this legend (which `build_content.py` files under the Nizwa Heritage Inn
   entry). Do not assume the wall entry's list is complete.
3. **Marks are snapped onto the circuit.** The discs and bars are detected at their own
   centres while the circuit comes from a dilated, filled, simplified contour, so the two
   missed each other by **4–7 m** at model scale. Towers floated beside the wall and — worse
   — no gateway was ever cut, because the cut radius was 2 m. `snap_to_wall()` in
   `work/trace_wall_plan.py` projects each mark onto the line; `raw` and `snapped_by` are
   kept in the JSON so the move stays auditable. The book says the towers are attached to
   the wall and the gates are its only openings, so this asserts the source rather than
   fudging.
4. **The 3D model is `src/components/WallMap3D.astro`.** It extrudes the traced circuit at
   the book's own measurements — 5.5 m high, 1.75 m thick, tower bases 4.5 m across — with
   the metres-per-plan-unit scale derived from the book's "about two kilometres" of wall
   rather than guessed. **The one figure the book does not give is tower height**; they
   stand 2 m above the wall, and the page names that as the model's choice, not the book's.
   three.js loads only when the visitor asks for it (717 KB, ~180 KB gzipped, its own
   chunk); the map page itself ships 6 KB.
   **It opens on Sabah Al Sabkha**, close in, because at true scale the whole circuit reads
   as a thin ribbon — a 5.5 m wall around a half-kilometre quarter. "Whole circuit" pulls
   back to a framing computed from the model's bounding box. Do not hand-pick either camera,
   and **keep the eye below 5.5 m** in the gate view: above the wall top you look straight
   over it and the gateway vanishes.
   **Labels** are HTML over the canvas, not textures — the Arabic names need real shaping and
   an RTL run. Every mark now has a name from the legend, but floating all 21 at once is
   clutter, so only the four gates and the fort carry a tag; a tower gives its name in the
   readout when clicked. That is the `label` flag on each mark in the model payload.
5. **What is inside the wall, and what it is worth.** The plan draws the fort's great round
   tower as a true footprint — the only building it does, the rest being little pictures — so
   that one is placed from it. **The plan is not to scale for buildings:** its circle measures
   about 64 m across where Nizwa Fort's tower is usually given as roughly 45 m, so read the
   position, not the size.
   **Crenellations** run along the wall head, round every tower and round the fort drum.
   Omani fortification is crenellated throughout — the plan draws it and photographs show
   it — but no source gives merlon sizes, so those are cut to look right at this scale and
   are shape only, not measurement.
   **The fort drum's proportions come from photographs**, not from the plan: a drum a little
   under two-thirds as tall as it is wide, a crenellated head, a band of small openings and
   a flagpole. Its POSITION and its circle are the plan's.
   **The houses are the best-sourced invented thing in the model.** The book gives the
   count (**more than three hundred**), the footprint range (**60–200 m²**) and the fact
   that the quarter divides into **five sub-quarters, each with its own sablah** — so the
   model places 300 blocks of 60–200 m² in five clusters. Only *where* each one stands and
   *how tall* it is are the model's, and the panel says exactly that. This also fixes the
   old misreading: an empty interior contradicted the book's own three hundred houses.
   **The palms are not in any source.** The plan has essentially no green in it at all
   (0.01% of pixels) and draws no trees or farms; the book names orchards inside the wall
   (بستان العقر, and two towers named after it) but gives no positions. They are grouped into
   four groves rather than spread evenly, because an even sprinkle reads as "the quarter was
   a palm grove" and the book is explicit that it held **more than three hundred houses**.
   They now ring the outside of the wall as well as clustering inside, because every
   photograph shows the quarter sitting in date gardens — still indicative, still unsourced.
   Houses and palms each have their own switch, and both are labelled as indicative in the
   measurements panel. **Do not let either creep toward looking surveyed.**
   ⚠️ The outer palm belt is built first; keep the inner groves in their own array before
   concatenating, or the per-grove cap trips immediately and no palm lands inside the wall.
   ⚠️ **Everything placed inside the circuit must clear the wall by its own half-diagonal.**
   Houses were sited by testing their CENTRE against the polygon, but a house is up to ~14 m
   across, so **38 of the 300 grew through the 1.75 m wall** — one of them by a full 10 m —
   and through the walkway on top of it. `distToWall()` measures to the wall LINE (not to the
   nearest traced vertex, which is not the same thing on a long straight run); houses clear it
   by half-diagonal + half-thickness + a 2.2 m lane, palms by a frond radius. Verified: 0
   intersections, minimum gap 3.1 m.
   ⚠️ Raising that clearance costs placements. At the old budget of 1400 tries per sub-quarter
   only **292** houses landed, which would have quietly contradicted the book's own "more than
   three hundred". The budget is now 4000. **If you tighten the clearance again, re-check the
   count** — the 300 is sourced, the try-budget is not.

6. **Rights are granted.** On **21 August 2026** the user reported that the author,
   **سليمان بن محمد السليماني**, has given permission to publish the book's material on this
   site. The pre-launch banner that used to sit in `src/components/Footer.astro` has been
   removed on the strength of it. The standing credit stays exactly as it is — the footer
   still names the author and the book on every page and still says the text rights remain
   his; permission to publish is not a transfer of copyright.
   **The scope is confirmed** (user, 21 August 2026): the grant covers the **photographs** as
   well as the text, and the **English translation** as a derivative work. That is the whole
   of what the site republishes, so nothing is left outstanding on rights.
   This is recorded from the user's word, not from a document. If a written licence is ever
   signed, note its terms here — and keep the footer credit either way: permission to publish
   is not a transfer of copyright, and the author is still named on every page.

7. **The wall head is the restored wall, not the book's.** The merlons used to span nearly the
   whole 1.75 m thickness, leaving no deck. They now sit on the OUTER edge, with a plain low
   parapet on the inner edge, a walkway between, and lamps along the inner parapet — all of it
   from the user's photographs of the site. **The book describes a defensive wall and mentions
   neither a walk along it nor any lighting**, so both carry their own rows in the measurements
   panel ("the wall as restored today / from photographs, NOT the book"), both caveats say so,
   and the lamps have their own switch.
   **The lamps are modelled as FIXTURES, not as light.** Each is a small dark lantern — body,
   warm lens, lid — on every second merlon (~2.7 m). Two things were tried and dropped, so do
   not re-add them: a `PointLight` per lamp (700-odd real lights cost more than the rest of the
   model together), and a translucent "glow" halo — `scene.background` is the page's ivory and
   the scene is lit as bright daylight, so a soft orange blob cannot read as light there, it
   just smears colour over the wall. The dusk glow of the photographs needs a night scene,
   which this model is not. Every merlon was also tried and read as a solid band, not a row.
   **There is now a Night switch**, and that is the scene the glow was waiting for: it swaps the
   background and fog to a dusk blue, drops the hemisphere light to 0.55 and the sun to a dim
   cool 0.35, and turns ON an additively-blended glow sphere per lamp. Nothing geometric moves.
   Measured off the framebuffer: mean luminance 110.7 by day against 56.1 at night, sky pixel
   70,76,90, and the warmest pixel at night is 255,156,62 — which falls to 27,19,13 with the
   lamps switched off, so the warm light in the night scene is provably the lamps and nothing
   else. **The night sky is a gradient DOME, not a flat colour** — two flat passes
   (0x141a26, then 0x36415f) both read as dead. It is a 4000-radius BackSide sphere with a
   ShaderMaterial: deep blue overhead, lavender grey, and a warm peach band hugging the horizon,
   the colours taken off the dusk photographs. It must stay a dome and not become a screen-space
   gradient — the band has to be anchored to the WORLD horizon or it slides as you orbit and the
   illusion dies. `fog: false` on the dome, `renderOrder = -1`, `scene.background = null` while
   night is on, and the fog tone (`NIGHT_FOG`) is the horizon colour so distant geometry melts
   into the band instead of ending on a line. Hemisphere 0.85, sun 0.55.
   ⚠️ The gradient barely shows in the OPENING view — close in on Sabah Al Sabkha, the frame is
   nearly all gate and almost no sky. Judge it from "Whole circuit", where a vertical sample
   gives 9 distinct tones from 70,76,90 overhead down to the warm 100,56,54 at the horizon. Raising `groundColor` barely moved the darkest
   band (12→15) — that band is the GATEWAY, not shadow fill: hiding the palms or the houses
   changes it by ±1, because the model opens close in on Sabah Al Sabkha and the frame is mostly
   gate. If night ever needs lifting again, the jamb/lintel colours are the lever, not the lights. The label chips
   get a fixed dark treatment at night (`.labels.is-night`) rather than following the page theme,
   which would otherwise put a dark chip on a dark sky whenever the page is in dark mode.
   ⚠️ **Which side is "out" comes from the polygon's WINDING, never from a centre test.**
   Comparing each crenel against the bounding-box centre looks perfectly reasonable and is
   wrong wherever the circuit turns concave — on this very irregular wall it put the merlons
   on the INSIDE for **153 of 1484 crenels**. Signed area gives the winding once and the
   outward normal of a→b is `(sin θ, −cos θ) * WIND` everywhere. Verified 1484/1484 correct at
   every probe distance up to the wall's own thickness.

8. **The wall map pins a selection; it does not follow the mouse.** Hover and click used to be
   the same action — `mouseenter` selected and leaving the map cleared it — so a chosen mark
   never stayed chosen and "pointing at" was indistinguishable from "picked". They are now two
   states: `hovered` only previews the panel, `pinned` survives the mouse leaving and is what
   the chips, `aria-pressed` and Escape act on. A pinned mark carries a halo ring and everything
   else on the plan drops to 0.28 opacity — on a circuit carrying 21 marks that dimming is what
   makes the chosen one findable at all. Do not collapse these back into one handler.
   The **panel says which state it is in** — "Previewing" or "Pinned", with an Unpin button that
   only appears once something is pinned — and it repeats the mark's own glyph (filled square for
   a gate, circle for a tower, in the plan's own colours) so the readout is visibly about *that*
   mark. Without that row the panel looked identical whether you were merely pointing at a mark
   or had chosen it, which was the original complaint.

9. **The route ships with no walking times and no distances — deliberately.** Nobody measured
   them, and on 21 August 2026 the user decided none were needed. So this is a settled choice,
   **not an outstanding task**: `/{lang}/route` carries a box that says outright that no times
   or distances are given, and why, and `content/data/route.json` holds none.
   ⚠️ "No need to measure" meant the page is fine as it stands — it is **not** licence to
   estimate. The mockup in `design/Route.dc.html` still shows «نحو ساعتين» and per-stop
   minutes; that is placeholder content, **not a source**, and it must not be lifted into the
   site. If someone ever does walk the route with a stopwatch and a measuring wheel, real
   numbers can go in — nothing else.

10. **The tree is cleaned and the site is deploy-ready** (21 August 2026). The root had
    accumulated the extraction's scratch — nine `probe*.txt` dumps, `raw.txt`, `clean.txt`,
    `clean2.txt`, `p5crop.png`, a `__pycache__`, an empty `capture.txt` and two 3D-model
    screenshots. All deleted. The rest moved rather than went: the dossier to `docs/`, the
    superseded research and the broken `Ref.md` to `docs/archive/`, the book and its recovered
    text to **`book/`**, the two dead extractors to `work/legacy/`. **`book/`, not `source/`,
    because `src/` already exists** and the two would be read for each other.
    Every script that opened those files by relative path was updated — `build_md.py`,
    `build_content.py`, `extract_photos.py`, `trace_wall_plan.py` — so the regeneration chain
    still runs from the repository root exactly as before.
    Added for deployment: `README.md`, a bilingual `/404` (Arabic first, English below, since
    a missing URL does not say which language was wanted), a generated `/robots.txt` that
    takes its Sitemap line from `site` rather than hardcoding it, `@astrojs/sitemap` with the
    ar/en alternates wired in, and host config for **both** Cloudflare Pages
    (`public/_headers`, `public/_redirects`, `.nvmrc`) and Netlify (`netlify.toml`).
    ⚠️ **The two header files are duplicates kept in step by hand.** Change one, change the
    other, or the site caches differently depending on where it is hosted.
    ⚠️ **There is still no git repository** — the user chose to skip it. Nothing deleted here
    is recoverable, and there is no history behind any of the above.

11. **No image is served at its source size, and no font was loading at all** (21 August 2026).
    Two separate faults, found together while making the site faster.

    **The photographs went through `public/photos/` untouched.** `work/sync_photos.mjs`
    copied all 113 JPEGs across and every page linked the original file whatever size the
    slot was — a 1418px JPEG behind a 256px card thumbnail. `/ar/discover` alone was
    **3.27 MB** of images. They now go through `astro:assets`: `src/lib/images.ts` imports
    `assets/photos/*.jpeg` so Astro can transform them, and `src/components/Photo.astro`
    is the only thing on the site that renders one. Measured, at desktop widths:
    discover **3270 → 516 KB**, the home page **1021 → 271 KB**, the wall entry
    **761 → 148 KB**. `public/photos/` and the sync script are gone.
    **Every slot must pass its own `sizes`** — that string is what the browser picks from,
    so a wrong one wastes the whole ramp. They are written next to the CSS they describe;
    change the grid, change the `sizes`.
    **WebP with a JPEG fallback, no AVIF.** AVIF is a further ~20% but roughly ten times
    the encode time, and the host rebuilds from cold. 959 transforms take ~4 s as it stands.
    ⚠️ **Astro emits the untransformed original beside the variants**, and nothing links to
    it — 123 files, **10.4 MB** per build. `work/prune_assets.mjs` deletes any image in
    `dist/_astro/` whose name appears in no built html/css/js. It runs from `npm run build`,
    before `check:links`. If a variant is ever referenced only from a place it does not
    read, it will be pruned — add the file type to its scan rather than dropping the step.
    ⚠️ **`<Photo>` renders `<picture>`, so the flex/grid child is the wrapper, not the
    image.** Every parent that laid out an `<img>` directly now needs
    `:global(picture) { display: contents }` — and `:global()` at all, because the `<img>`
    belongs to the child component's template and never carries the parent's scope
    attribute. `img:first-child` also stops meaning what it did: with `display: contents`
    every image is the first child of its own `<picture>`. Use `picture:first-child img`.

    **The fonts had never once loaded.** `work/fetch_fonts.py` rewrote each `url()` and
    re-stated `format('woff2')` after a `format('woff2')` that was already there. Two
    format components make the whole `src` descriptor invalid, so all **23** faces were
    dropped and all 74 pages rendered in Times New Roman — while still preloading 124 KB of
    woff2 that nothing used. Verified in the browser before and after: `document.fonts`
    held 0 faces, and now holds 23 with 8 loaded on an Arabic page. The generator says why.
    The rules moved to `src/styles/fonts.css` and are `@import`-ed by `global.css` in the
    same change, which also removes the second blocking request per page.

    **Two layout-shift bugs fell out of the same pass.** In `Plate.astro` the images that
    keep their own proportions were given `aspect-ratio: auto`, which overrides the whole
    UA shorthand — including the `auto W/H` the browser derives from the width and height
    attributes — so they reserved **no height at all** until they loaded. `revert` does not
    help; that ratio is not a UA stylesheet rule. The 4/3 crop is now only ever *added*, via
    `:not()`, and never overridden back. And a grid item at `height: auto` is stretched, so
    an unloaded image took its full attribute height (871px in a 442px slot) until `height:
    auto` was made explicit on the image itself. Both verified in the browser.

## Decisions still open — ask the user, do not guess

**The domain.** `astro.config.mjs` sets `site` to `https://alaqur.om`, and as of
21 August 2026 that is a **placeholder, not a decision** — the user has not settled the real
domain. That single value feeds every canonical URL, every `hreflang`, `og:url`, `og:image`
and the whole sitemap, so it must be set before launch. It is the one thing standing between
the current tree and a correct deploy. Nothing else needs changing when it is.

The two items that used to stand here are settled above: rights (item 6, scope confirmed) and
the route's missing times and distances (item 9, a deliberate omission). Add to this section
rather than guessing if something new comes up.

## Design canvas

<https://claude.ai/code/artifact/dd2ff264-cbb6-491f-8d88-553d5a228237> — eight artboards:
three home-page directions (أ Clay & Shadow, ب The Manuscript, ج Map First) plus the wall
map, a wiki entry, Eat & Stay, the guided route, and the identity sheet
(الهوية, `design/Brand.dc.html`). Read it with WebFetch.

Working files in `design/`. To change it: edit the `.dc.html` files, re-seed with the
`design` skill's helper, republish **passing the URL above as `url`** — publishing without
it creates a second artifact instead of updating this one.

---

## Rules that must hold in the build

- **The book's figures appear in the book's voice; current figures get a qualifier.** The
  book says the wall has *fifteen* towers; the restored wall has *sixteen*. Never put a
  modern number inside a sentence attributed to the author. Say "١٦ برجاً بعد الترميم".
- **Where sources disagree, say so on the page.** There are seven such conflicts, listed
  in `docs/AL-AQR.md` §5 — plus one found during the build: the book's *text* says fifteen
  towers, while the plan printed in the same book draws **seventeen**. The map page states
  all four figures rather than choosing. The Shawadhna mosque has three different founding dates in three
  sources. Do not silently pick a winner — the entry template has a box for this.
- **Never render ratings, prices or review counts.** They are in `places.json` for
  reference only; the file says so itself. Render name, type, hours, phone and the maps
  link, with a visible "last checked" date. A wrong price is worse than no price.
- **Do not invent practical facts** — walking times, distances, opening hours. If it was
  not measured or sourced, mark it as an estimate or leave it out.
- **Sourcing caution.** The book, the Omani press coverage and the endowment's own
  channels are largely **one voice, not three**. Oman Daily reproduces the book's figures
  verbatim. Agreement between them is not independent corroboration.

## Files

| Path | What it is |
|---|---|
| `docs/AL-AQR.md` | **Start here.** The full dossier: source analysis, what the book says, the 2016–2026 restoration timeline, what the quarter contains today, the seven discrepancies, sources, and the complete Arabic text as an appendix |
| `content/ar/sections/` · `content/en/sections/` | **The site content.** 31 sections per language, paired by slug and `order`, with frontmatter. Page markers stripped, paragraphs intact |
| `content/sections.json` | Slug ↔ Arabic title ↔ English title index |
| `content/ar/back-matter/` | The book's closing pages — the author's acknowledgements and his afterword. Arabic only; the English translation is in `src/lib/credits.ts` |
| `content/data/wall-plan.json` | The wall circuit, its 17 towers and 4 gates, traced from Dr Al Salmi's plan by `work/trace_wall_plan.py`. Positions are in a 1000×1000 drawing — **no latitude or longitude, not a survey** |
| `content/data/captions.json` | The book's photo captions paired to its photographs, built by `work/build_captions.py`. Carries a `scope` per page — `photo` means the caption is certainly that image's, `group` means it labels the page's set |
| `content/data/route.json` | The guided walk: nine stops, each one an existing entry, in a walking order. **Authored, not generated** — no script writes it. Carries no times and no distances, deliberately |
| `content/data/places.json` | 42 places (heritage, stay, eat, shop) — each with a Google Maps link, 18 with Plus Codes. Carries its own `display_policy` |
| `content/en/book.md` | The translation as one document, with translator's notes |
| `book/Ref.clean.md` | The recovered Arabic text as one document, with PDF page markers |
| `assets/photos/` | 113 photos extracted from the PDF + `CATALOGUE.md` (page, section, size, caption) and `catalogue.json` |
| `design/` | Design canvas working files |
| `src/` | **The site.** Astro. `pages/[lang]/` holds the six routes, `lib/` the data joins, `components/` the shared parts, `styles/global.css` the direction-أ tokens |
| `work/` | Extraction scripts — see below |
| `book/REFRENCE.pdf` | The source book |
| `README.md` | The public-facing readme: how to run it, how to deploy it, what holds in the content |
| `src/components/Photo.astro` · `src/lib/images.ts` | Every image on the site. Resizes per slot, WebP + JPEG fallback |
| `netlify.toml` · `public/_headers` · `public/_redirects` · `.nvmrc` | Host config. The two header files say the same thing for two hosts and are kept in step **by hand** |
| `docs/archive/` | `RESEARCH.md`, `INVENTORY.md` and the broken `Ref.md`, all superseded by `docs/AL-AQR.md`. Nothing in the build reads them |
| `work/legacy/` | The first two extractors, superseded by `work/build_md.py`. Kept as the record of how its `CORRECTIONS` map was arrived at |

### ⚠️ `docs/archive/Ref.md` is broken — do not use it

It is a text dump of the PDF in *visual* glyph order: every line mirrored, ligatures
mangled, 1334 stray `É` characters inside words. It is kept only as evidence of the
problem. **Use `book/Ref.clean.md` or the `content/` sections.**

### Running the site

```bash
npm install
npm run dev      # http://localhost:4321 - redirects to /ar
npm run build    # 74 pages into dist/
npm run check    # astro check (types)
npm run check:links   # crawl dist/ for broken links and missing assets
```

Routes are `/{ar,en}`, `/{lang}/discover`, `/{lang}/<slug>` (31 entries), `/{lang}/map`,
`/{lang}/route`, `/{lang}/visit`, `/{lang}/credits`, plus a bilingual `/404` and a generated
`/robots.txt` and `/sitemap-index.xml`. Every route is a shared slug under a language segment, so the toggle in
`Masthead.astro` is a segment swap and always lands on the same page in the other language.

**Nothing is copied into `public/photos/` any more** — see item 11 below. The
photographs go through Astro's image pipeline and are served from `/_astro/` as WebP,
resized per slot. `npm run build` ends with `work/prune_assets.mjs`.

**`public/fonts/` is generated**, by `work/fetch_fonts.py`, and is committed rather
than fetched at build time. The three families used to load from `fonts.googleapis.com`
through a render-blocking `<link>` on all 74 pages. They are now self-hosted, Arabic and
Latin subsets only, and `Base.astro` preloads just the two faces the page's language
paints with — an Arabic page fetches 124 KB of font and no Latin at all, an English page
72 KB and no Arabic. Re-run the script only to pick up upstream font revisions.
The `@font-face` rules themselves are written to **`src/styles/fonts.css`** and
`@import`-ed by `global.css`, so they ride in the page's own hashed stylesheet instead of
costing a second blocking request. Both outputs are generated — do not hand-edit either.

### Regenerating

```bash
python work/build_md.py       # book/REFRENCE.pdf -> book/Ref.clean.md
python work/build_content.py  # book/Ref.clean.md + content/en/book.md -> content/{ar,en}/sections/
python work/extract_photos.py # book/REFRENCE.pdf -> assets/photos/
python work/build_captions.py # catalogue.json + reviewed EN -> content/data/captions.json
python work/trace_wall_plan.py # p23-1.jpeg -> content/data/wall-plan.json
python work/build_icons.py    # -> public/icon.svg + apple-touch-icon.png
python work/fetch_fonts.py    # Google Fonts -> public/fonts/ + src/styles/fonts.css
python work/check_contrast.py # verifies src/styles/global.css against WCAG AA
```

⚠️ **Do not run `npm run build` while `astro dev` is running.** They share
`.astro/` and `node_modules/.vite/`, and the dev server ends up serving `504 Outdated
Optimize Dep` for the three.js chunk, or reusing stale rendered markdown. Stop the dev
server first, or accept that you will have to restart it.

**If you cannot stop it** — someone else's session owns it — build against throwaway
caches instead of fighting for the shared ones. Write a config that spreads the real one
and overrides `cacheDir`, `outDir` and `vite.cacheDir`, build with
`npx astro build --config astro.verify.config.mjs`, then delete the config and its output.
Nothing the dev server owns is touched. Note the failure mode this avoids: the dev server
will happily serve **current HTML with one-revision-stale scoped CSS**, so a component
looks broken in ways the source does not explain.

⚠️ **Astro's content cache does not notice a change to a remark plugin.** If you edit
`src/lib/remark-book-captions.mjs` and the output looks unchanged, a stale
`.astro/data-store.json` is being reused — and a running `astro dev` will keep rewriting it
underneath a build. Stop the dev server, then
`rm -rf .astro dist node_modules/.astro node_modules/.vite` and rebuild. This has produced
convincingly wrong output twice.

`work/build_md.py` reconstructs Arabic from the PDF glyph stream — it un-reverses ligature
glyphs, restores lams that `ToUnicode` dropped, re-sorts right-to-left, and regroups
columns. Its `CORRECTIONS` map holds eight words that no geometric rule can resolve,
because the ligature and a plain final alef are identical in width. Do not "simplify" it.

## Known constraints

- **Photo resolution ceiling.** 113 images, but only **11 reach 1.0 MP** and the widest is
  1658 px. Fine for cards and inline figures; too small for full-bleed retina heroes.
  `assets/photos/CATALOGUE.md` ends with a hero shortlist.
- **Image markers survive into the content, and `build_content.py` only catches half of
  them.** The book's photo captions sit inside the running text as `[صورة]` (Arabic) and
  `` `[image]` `` (English). `is_caption()` in `work/build_content.py` tests
  `startswith("[image]")`, which never matches the English form because it begins with a
  backtick — so English captions are left mashed into their paragraphs, and in two places
  in the wall entry an Arabic caption splits a sentence in half. The site repairs this at
  render time in `src/lib/remark-book-captions.mjs`, which lifts every marker and its
  caption into its own block and rejoins the sentences the captions broke. **The
  underlying generator bug is still there** — fix `is_caption()` if the content is ever
  regenerated and you want the files themselves clean.
- **The book's back matter had been swallowed by the last entry.** The closing pages
  (شكر وتقدير, الخاتمة, الفهرس) carry no heading in the PDF glyph stream, so
  `split_headings()` filed them under مطعم العقر التراثي — which put the author's
  acknowledgements, and a raw page-number index, inside the restaurant entry.
  `work/build_content.py` now lifts them out by their opening words into
  `content/ar/back-matter/` and drops the printed index. **Fixed**, and the credits page
  is built from the result.
- **Captions are matched to a page, not always to a single photograph.** `work/build_captions.py`
  pairs the book's captions to its photographs: 16 pages carry captions, covering 40 of the
  113 images. Only **2** pages hold one photograph and one caption, so only those are bound
  to a single file (`scope: "photo"`). The other 14 print several photographs under a shared
  caption and the extraction records no position, so the caption labels the page's group
  (`scope: "group"`) and the page says so out loud. **Do not narrow a group caption to one
  file by guessing** — page 34 is the warning: its two sablah captions appear in opposite
  order in Arabic and English, because Arabic reads the spread right-to-left, so pairing by
  index labels each photograph with the other one's name.
- **73 photographs still carry no caption at all** — the book prints them without one.
- **Poetry.** Diacritics on two poems did not survive extraction. If either goes on the
  site, set it from the physical book.
- **Qur'anic verse** in the Mazara'a entry came out of the PDF as private-use glyphs
  (`ﮙ ﮚ ﮛ…`). **Fixed on 21 August 2026** — the user supplied the text and it is now
  re-keyed in `content/ar/sections/05-mazaraa-mosque.md`: التوبة ١٨. The glyph run had 24
  marks, which matches that verse's words, so the identification is corroborated and not a
  guess. Nothing was added to the book's sentence around it — no inline citation — because
  the `content/` files are the book's text, not an edition of it.
  The English entry renders it as **Saheeh International** (chosen by the user on
  21 August 2026), as a blockquote followed by a visible credit line. **That credit is not
  decoration** — Saheeh International is a copyrighted translation and the only third-party
  text on the site that is not the book's. If the translation is ever swapped, swap the
  credit with it.
- **Business listings are the mapped subset**, not a census: Google lists ~32 businesses,
  the quarter claims 81+ ventures. Stalls and home producers appear nowhere.
