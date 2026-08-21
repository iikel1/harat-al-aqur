/**
 * The book's photographs sit inside the running text in the PDF, and the
 * extraction keeps them as markers: `[صورة]` in Arabic, `` `[image]` `` in
 * English, each followed by that photograph's caption.
 *
 * Left alone they read as part of the sentence — and in two places in the wall
 * entry a caption lands mid-sentence and splits it. This plugin lifts every
 * marker and its caption out of the paragraph and gives it its own block,
 * styled as a caption, so the prose reads as prose.
 *
 * A caption that content/data/captions.json has already paired to a photograph is
 * dropped here instead, because the gallery prints it under the image itself and
 * showing it twice on one page reads as an error. Captions with no photograph
 * paired to them still get their own block, so nothing from the book is lost.
 */
import { ALL_CAPTION_STRINGS } from './captions.ts';

const normalise = (s) => s.replace(/\s+/g, ' ').trim();
const PAIRED = new Set(ALL_CAPTION_STRINGS.map(normalise));

const AR_MARKER = '[صورة]';
const EN_MARKER = '[image]';

const isEnMarker = (node) => node.type === 'inlineCode' && node.value.trim() === EN_MARKER;

/** Text a caption segment carries, for deciding whether it is worth keeping. */
function textOf(nodes) {
  return nodes
    .map((n) => (n.value ?? (n.children ? textOf(n.children) : '')))
    .join('')
    .trim();
}

/** Drop the separators the PDF layout leaves behind between adjacent captions. */
function tidy(nodes) {
  const out = nodes.slice();
  while (out.length) {
    const first = out[0];
    if (first.type === 'text') {
      const trimmed = first.value.replace(/^[\s·•\-–—]+/, '');
      if (!trimmed) { out.shift(); continue; }
      out[0] = { ...first, value: trimmed };
    }
    break;
  }
  while (out.length) {
    const last = out[out.length - 1];
    if (last.type === 'text') {
      const trimmed = last.value.replace(/[\s·•\-–—]+$/, '');
      if (!trimmed) { out.pop(); continue; }
      out[out.length - 1] = { ...last, value: trimmed };
    }
    break;
  }
  return out;
}

const caption = (children) => ({
  type: 'paragraph',
  children,
  data: { hProperties: { class: 'book-caption' } }
});

// Same set work/build_content.py uses to decide whether a break in the source
// ended a sentence or merely interrupted one.
const ENDS_SENTENCE = ['.', '؟', '!', '؛', ':', '»', '"'];
const endsSentence = (text) => ENDS_SENTENCE.some((p) => text.endsWith(p));

export default function remarkBookCaptions() {
  return (tree) => {
    const next = [];
    // A caption can land mid-sentence, splitting it across two paragraphs. When
    // that happens the first half waits here for the half that follows, and the
    // captions between them are held back until the sentence is whole again.
    let dangling = null;
    let held = [];

    const flushHeld = () => {
      next.push(...held);
      held = [];
      dangling = null;
    };

    for (const node of tree.children) {
      if (node.type !== 'paragraph' || !node.children?.length) {
        flushHeld();
        next.push(node);
        continue;
      }

      // Split the paragraph's children into segments at every marker.
      const segments = [[]];
      for (const child of node.children) {
        if (isEnMarker(child)) {
          segments.push([]);
          continue;
        }
        if (child.type === 'text' && child.value.includes(AR_MARKER)) {
          const parts = child.value.split(AR_MARKER);
          segments[segments.length - 1].push({ ...child, value: parts[0] });
          for (const part of parts.slice(1)) segments.push([{ ...child, value: part }]);
          continue;
        }
        segments[segments.length - 1].push(child);
      }

      if (segments.length === 1) {
        // A plain paragraph. If a half-sentence is waiting, this completes it.
        if (dangling) {
          dangling.children = [
            ...dangling.children,
            { type: 'text', value: ' ' },
            ...node.children
          ];
          flushHeld();
        } else {
          next.push(node);
        }
        continue;
      }

      const [body, ...captions] = segments;
      const captionNodes = captions
        .map((seg) => tidy(seg))
        .filter((seg) => textOf(seg))
        // Shown under its photograph in the gallery; printing it here as well
        // would put the same line on the page twice.
        .filter((seg) => !PAIRED.has(normalise(textOf(seg))))
        .map(caption);

      const bodyNodes = tidy(body);
      const bodyText = textOf(bodyNodes);

      // A caption-only paragraph carries no sentence of its own, so it must not
      // end a wait: a run of captions can sit between the two halves.
      if (!bodyText) {
        if (dangling) held.push(...captionNodes);
        else next.push(...captionNodes);
        continue;
      }

      flushHeld();

      const para = { ...node, children: bodyNodes };
      next.push(para);
      // The caption cut this sentence in half - hold its captions back until
      // the other half arrives, so the sentence is not left dangling.
      if (!endsSentence(bodyText)) {
        dangling = para;
        held = captionNodes;
        continue;
      }
      next.push(...captionNodes);
    }

    flushHeld();
    tree.children = next;
  };
}
