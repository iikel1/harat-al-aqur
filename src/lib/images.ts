import type { ImageMetadata } from 'astro';

/**
 * The book's photographs, as build-time image assets.
 *
 * `src/lib/photos.ts` answers *which* photograph belongs to an entry, from the
 * catalogue JSON. This file answers *how to serve it*: the same files, imported
 * so that Astro's image pipeline can resize them and emit WebP.
 *
 * They used to be copied verbatim into `public/photos/` and served at full size
 * whatever slot they landed in - a 1418px JPEG behind a 256px card thumbnail.
 * The discover page alone was 3.3 MB of images. Going through the pipeline gives
 * each slot a `srcset` sized for it, in WebP with a JPEG fallback, under a
 * content-hashed `/_astro/` name that can be cached forever.
 *
 * The glob is eager because the join is by filename: the catalogue names
 * `p05-1.jpeg`, and only an import gives us the width, height and hashed URL.
 * Eager here costs nothing at runtime - this is a static build, and an image
 * that no page references is never transformed and never written out.
 */
const modules = import.meta.glob<ImageMetadata>('../../assets/photos/*.jpeg', {
  eager: true,
  import: 'default'
});

const byFile = new Map<string, ImageMetadata>();
for (const [path, meta] of Object.entries(modules)) {
  byFile.set(path.slice(path.lastIndexOf('/') + 1), meta);
}

/** The image asset for a catalogue filename, e.g. `p05-1.jpeg`. */
export function imageFor(file: string): ImageMetadata {
  const meta = byFile.get(file);
  // A missing file means the catalogue and assets/photos/ have drifted apart.
  // Fail the build rather than emit a broken <img> into 74 pages.
  if (!meta) throw new Error(`No image asset for "${file}" - is it in assets/photos/?`);
  return meta;
}

/**
 * The widths worth emitting for one slot, clamped to what the source can give.
 *
 * Two clamps, and both matter. The resolution ceiling in CLAUDE.md is the first:
 * only 11 of the 113 photographs reach 1.0 MP and the widest is 1658px, so
 * asking for a 1440px variant of an 800px original would upscale it - more bytes
 * for a blurrier image. Anything at or above the source width is replaced by the
 * source width itself.
 *
 * The second is the slot. A card thumbnail is never painted wider than about
 * 1088px even on a 2x phone, so emitting the full 1418px file for it is a
 * variant nothing will ever choose - it just sits in dist/. So the source width
 * is only added when the caller actually asked for something that big.
 *
 * Callers should therefore pass a ramp that reaches roughly 2x the widest the
 * slot is ever painted, and let this cut it down.
 */
export function widthsFor(meta: ImageMetadata, wanted: number[]): number[] {
  const ceiling = Math.max(...wanted);
  const fits = wanted.filter((w) => w < meta.width);
  if (ceiling >= meta.width) fits.push(meta.width);
  return [...new Set(fits)].sort((a, b) => a - b);
}
