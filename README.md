# حارة العقر · Harat Al Aqur

A static bilingual website about **Harat Al Aqur**, the walled historic quarter of Nizwa,
Oman — part encyclopedia, part visitor guide. Arabic is the primary language; English is a
secondary view reached by a toggle that maps page-to-page.

Built with [Astro](https://astro.build). 74 static pages, no server, no database.

The whole site is drawn from one book — *حارة العقر* by **سليمان بن محمد السليماني** — who
has given permission for its text, photographs and the English translation to be published
here. Permission to publish is not a transfer of copyright: the footer credits the author
and the book on every page, and must stay.

---

## Running it

```bash
npm install
npm run dev            # http://localhost:4321 — redirects to /ar
```

| Command | What it does |
|---|---|
| `npm run dev` | Dev server with HMR |
| `npm run build` | 74 pages into `dist/`, images resized, unused variants pruned |
| `npm run preview` | Serve the built `dist/` locally |
| `npm run check` | `astro check` — types and template diagnostics |
| `npm run check:links` | Crawl `dist/` for broken internal links and missing assets |

### Images

`assets/photos/` is the source of truth and is never served as-is. Every photograph on
the site goes through `src/components/Photo.astro`, which resizes it for the slot it
lands in and serves **WebP with a JPEG fallback** from `/_astro/`, under a content-hashed
name that can be cached forever. Nothing is copied into `public/`.

`npm run build` therefore ends with `work/prune_assets.mjs`, which deletes the full-size
originals Astro emits beside the variants and nothing links to — about 10 MB per build.

⚠️ **Do not run `npm run build` while `astro dev` is running.** They share `.astro/` and
`node_modules/.vite/`; the dev server ends up serving stale chunks. See `CLAUDE.md`.

### Routes

`/{ar,en}` · `/{lang}/discover` · `/{lang}/<slug>` (31 entries) · `/{lang}/map` ·
`/{lang}/route` · `/{lang}/visit` · `/{lang}/credits`, plus a bilingual `/404` and a
generated `/robots.txt` and `/sitemap-index.xml`.

Every route is a shared slug under a language segment, which is what lets the toggle in
`Masthead.astro` be a segment swap that always lands on the same page in the other language.

---

## Deploying

Static output, domain root. Both hosts are configured; pick one.

| | Cloudflare Pages | Netlify |
|---|---|---|
| Build command | `npm run build` | `npm run build` (in `netlify.toml`) |
| Output directory | `dist` | `dist` (in `netlify.toml`) |
| Node version | `.nvmrc` → 22 | `netlify.toml` → 22 |
| Headers / redirects | `public/_headers`, `public/_redirects` | `netlify.toml` |

`public/_headers` and `netlify.toml` say the same thing — long immutable caching for
`/_astro/*` (the hashed CSS, JS and image variants) and the woff2 subsets, and
`nosniff` / `Referrer-Policy` / `X-Frame-Options` / `Permissions-Policy` on everything.
**They are kept in step by hand**: change one, change the other.

Both also turn the bare `/` into a real 302 to `/ar`. Astro emits a meta-refresh
`index.html` for the same hop, which stays as the fallback.

You can also deploy without any git remote by uploading the built `dist/` directory
directly — both hosts accept a drag-and-drop of a folder.

### ⚠️ Set the domain before launch

`astro.config.mjs` sets `site` to **`https://alaqur.om`, which is a placeholder** — as of
21 August 2026 the real domain was not decided. That one value feeds every canonical URL,
every `hreflang`, `og:url`, `og:image` and the entire sitemap. Change it there and nothing
else needs touching; ship it wrong and 74 pages of canonicals point at a domain that is
not yours.

---

## What is in here

| Path | What it is |
|---|---|
| `src/` | **The site.** `pages/[lang]/` the routes, `lib/` the data joins, `components/` the shared parts, `styles/global.css` the design tokens |
| `content/` | The book as 31 sections per language, paired by slug, plus `data/` — the traced wall plan, the captions, the walking route, the places list |
| `assets/photos/` | 113 photographs extracted from the book, with `CATALOGUE.md` |
| `public/` | Static root: the generated icons, the self-hosted font subsets, the host header/redirect files |
| `book/` | The source book: `REFRENCE.pdf` and `Ref.clean.md`, the recovered Arabic text |
| `docs/` | `AL-AQR.md` — the full dossier: sources, the restoration timeline, the discrepancies. `docs/archive/` is superseded material kept for the record |
| `design/` | Design canvas working files (`.dc.html`) |
| `work/` | The extraction and build scripts — see below. `work/legacy/` is superseded |
| `CLAUDE.md` | The decisions log. **Read it before changing anything**: colour tokens, the 3D model's sourcing, what may and may not be invented |

### Regenerating

Python scripts, run from the repository root. None of them run at build time — the
content they produce is committed.

```bash
python work/build_md.py        # book/REFRENCE.pdf -> book/Ref.clean.md
python work/build_content.py   # -> content/{ar,en}/sections/
python work/extract_photos.py  # -> assets/photos/
python work/build_captions.py  # -> content/data/captions.json
python work/trace_wall_plan.py # -> content/data/wall-plan.json
python work/build_icons.py     # -> public/icon.svg, public/apple-touch-icon.png
python work/fetch_fonts.py     # Google Fonts -> public/fonts/ + src/styles/fonts.css
python work/check_contrast.py  # verifies global.css against WCAG AA
```

`check_contrast.py` is the one to remember: **run it after touching any colour token.** It
parses the stylesheet, checks both light and dark, and exits non-zero on a failure.

---

## Rules that hold in the content

These are not style preferences — they are why the site can be trusted. `CLAUDE.md` has
the full list.

- **The book's figures appear in the book's voice; current figures get a qualifier.** The
  book says the wall has fifteen towers; the restored wall has sixteen; the plan printed in
  the same book draws seventeen. Never put a modern number inside a sentence attributed to
  the author.
- **Where sources disagree, say so on the page.** There is a component for it. Do not
  silently pick a winner.
- **Never render ratings, prices or review counts.** They sit in `places.json` for
  reference only, and the file says so itself.
- **Do not invent practical facts** — walking times, distances, opening hours. The walking
  route deliberately ships with no times and no distances, because nobody measured them.
