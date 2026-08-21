/** First sentence-ish of an entry, with markdown syntax stripped, for cards and meta tags. */
export function excerpt(markdown: string, max = 170): string {
  const firstPara =
    markdown
      .split(/\n{2,}/)
      .map((p) => p.trim())
      .find((p) => p && !p.startsWith('#') && !p.startsWith('---') && !p.startsWith('|')) ?? '';

  const plain = firstPara
    // The book's inline image markers, and the caption that follows each one.
    .replace(/`?\[(?:صورة|image)\]`?\s*/g, '')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/[*_`>#]/g, '')
    .replace(/\s+/g, ' ')
    .trim();

  if (plain.length <= max) return plain;
  const cut = plain.slice(0, max);
  const lastSpace = cut.lastIndexOf(' ');
  return `${cut.slice(0, lastSpace > max * 0.6 ? lastSpace : max).trim()}…`;
}
