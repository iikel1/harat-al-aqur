import data from '../../content/data/captions.json';
import type { Lang } from './i18n';

/**
 * The book's photo captions, paired to its photographs by work/build_captions.py.
 *
 * `scope` is the important field. 'photo' means the page held exactly one
 * photograph and one caption, so the caption belongs to that image and nothing
 * else. 'group' means the book printed several photographs to the page under one
 * or more shared captions, and the extraction does not record which photograph
 * sits beneath which caption — so the caption labels the whole page's set. The
 * templates must respect that difference; never present a group caption as
 * though it described a single image.
 */
export type CaptionPair = { ar: string; en: string };
export type PageCaptions = { scope: 'photo' | 'group'; photos: string[]; captions: CaptionPair[] };

const doc = data as {
  checked: string;
  source: string;
  policy: string;
  pages: Record<string, PageCaptions>;
};

export const CAPTIONS_CHECKED = doc.checked;

export const captionsForPage = (page: number): PageCaptions | undefined => doc.pages[String(page)];

export const captionText = (c: CaptionPair, lang: Lang) => (lang === 'ar' ? c.ar : c.en) || c.ar;

/** Only ever returns a caption that is certain to describe this one photograph. */
export function exactCaptionFor(file: string, page: number, lang: Lang): string | undefined {
  const entry = captionsForPage(page);
  if (!entry || entry.scope !== 'photo') return undefined;
  if (!entry.photos.includes(file)) return undefined;
  return captionText(entry.captions[0], lang);
}

/**
 * Every caption string the site shows alongside a photograph, in both languages.
 * remark-book-captions.mjs uses this to drop the matching block from the running
 * text, so a caption is not printed twice on the same page.
 */
export const ALL_CAPTION_STRINGS: string[] = Object.values(doc.pages).flatMap((p) =>
  p.captions.flatMap((c) => [c.ar, c.en].filter(Boolean))
);
