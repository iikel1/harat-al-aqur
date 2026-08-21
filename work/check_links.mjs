// Crawls dist/ after a build and confirms every internal link resolves to a
// page that exists and every asset reference points at a real file.
// Run with: npm run build && npm run check:links
import fs from 'node:fs';
import path from 'node:path';

const root = 'dist';
const files = [];
(function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.endsWith('.html')) files.push(p);
  }
})(root);

const routeOf = (f) =>
  '/' + path.relative(root, f).split(path.sep).join('/').replace(/index\.html$/, '').replace(/\/$/, '');

const exists = new Set(files.map(routeOf));
const bad = [];

for (const f of files) {
  const html = fs.readFileSync(f, 'utf8');
  for (const m of html.matchAll(/href="(\/[^"#?]*)"/g)) {
    const raw = m[1];
    // stylesheets, scripts and images are files on disk, not routes
    if (/\.[a-z0-9]{2,5}$/i.test(raw)) {
      if (!fs.existsSync(path.join(root, raw))) bad.push([routeOf(f), raw, 'missing file']);
      continue;
    }
    const u = raw.replace(/\/$/, '');
    if (!exists.has(u)) bad.push([routeOf(f), raw, 'no page']);
  }
  for (const m of html.matchAll(/src="(\/[^"#?]*)"/g)) {
    if (!fs.existsSync(path.join(root, m[1]))) bad.push([routeOf(f), m[1], 'missing asset']);
  }
  // Every image goes out as a srcset now, and a `src` that resolves says nothing
  // about the candidates beside it - which is exactly what a visitor downloads.
  for (const m of html.matchAll(/srcset="([^"]+)"/g)) {
    for (const candidate of m[1].split(',')) {
      const url = candidate.trim().split(/\s+/)[0];
      if (!url.startsWith('/')) continue;
      if (!fs.existsSync(path.join(root, url))) bad.push([routeOf(f), url, 'missing srcset asset']);
    }
  }
}

console.log('html pages:', files.length);
console.log('broken internal links/assets:', bad.length);
bad.slice(0, 12).forEach((b) => console.log('  ', b.join(' | ')));
