import catalogue from '../../assets/photos/catalogue.json';
import sections from '../../content/sections.json';

// 113 images extracted from the PDF. The catalogue keys them by the book's own
// Arabic section heading, which matches content/sections.json exactly, so the
// join is by title -> slug. Five sections carry no photograph at all
// (foreword, the-omani-house, under-the-yaariba, abu-al-muthir-museum,
// saat-al-mudda) - callers must handle an empty list.
export type Photo = {
  file: string;
  pdf_page: number;
  section: string;
  width: number;
  height: number;
  megapixels: number;
  kind: string;
  full_bleed: boolean;
};

const all = catalogue as Photo[];
const slugOfArTitle = new Map(sections.map((s) => [s.ar, s.slug] as const));

const bySlug = new Map<string, Photo[]>();
for (const p of all) {
  const slug = slugOfArTitle.get(p.section);
  if (!slug) continue;
  (bySlug.get(slug) ?? bySlug.set(slug, []).get(slug)!).push(p);
}
// Largest first: the lead image of an entry should be the best one available.
for (const list of bySlug.values()) list.sort((a, b) => b.megapixels - a.megapixels);

export const photosFor = (slug: string): Photo[] => bySlug.get(slug) ?? [];
export const leadPhoto = (slug: string): Photo | undefined => photosFor(slug)[0];

/**
 * An entry's photographs grouped by the book page they were printed on.
 *
 * The grouping is not cosmetic: the book prints several photographs to a page
 * under one shared caption, so the page is the unit a caption actually applies
 * to. Pass `exclude` to leave out an image already shown as the lead.
 */
export type PhotoGroup = { page: number; photos: Photo[] };

export function photoGroupsFor(slug: string, exclude?: string): PhotoGroup[] {
  const byPage = new Map<number, Photo[]>();
  for (const p of photosFor(slug)) {
    if (p.file === exclude) continue;
    const list = byPage.get(p.pdf_page);
    if (list) list.push(p);
    else byPage.set(p.pdf_page, [p]);
  }
  return [...byPage.entries()]
    .map(([page, photos]) => ({ page, photos: photos.sort((a, b) => a.file.localeCompare(b.file)) }))
    .sort((a, b) => a.page - b.page);
}

// There is deliberately no photoUrl() any more. The photographs are not copied
// into public/ and are not served at their source size: every one of them goes
// through src/lib/images.ts and the <Photo> component, which is what gives each
// slot a WebP at the width it actually paints. See src/lib/images.ts.

/**
 * The only images at or above 1.0 MP, from assets/photos/CATALOGUE.md.
 * The widest is 1658px - fine for a scrimmed banner, not for a full-bleed
 * retina hero. New photography is still needed; see CLAUDE.md.
 */
export const HERO_SHORTLIST = [
  'p20-1.jpeg', 'p05-1.jpeg', 'p44-1.jpeg', 'p31-1.jpeg', 'p55-1.jpeg',
  'p58-1.jpeg', 'p07-1.jpeg', 'p16-1.jpeg', 'p54-1.jpeg', 'p26-1.jpeg', 'p24-1.jpeg'
] as const;

export const photoByFile = (file: string) => all.find((p) => p.file === file);
