// Crawls dist/ after a build and confirms every internal link resolves to a
// page that exists and every asset reference points at a real file.
// Run with: npm run build && npm run check:links
import fs from 'node:fs';
import path from 'node:path';

const root = 'dist';

// The site deploys under a base path (/harat-al-aqur on GitHub Pages), so dist/
// is served AT that prefix - dist/ar/ is /harat-al-aqur/ar/ on the server. Every
// internal absolute URL therefore MUST start with the base; one that does not
// (a bare /ar/ or /fonts/) 404s on the deployed site even though the file exists
// in dist. Strip the base to resolve against disk, and flag anything absolute
// that lacks it. Set BASE to '' if the site ever moves to a domain root.
const BASE = '/harat-al-aqur';
const rebase = (u) => {
  if (u === BASE) return '/';
  if (u.startsWith(BASE + '/')) return u.slice(BASE.length);
  return null; // absolute but not under the base -> would 404 on the server
};
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
    const rel = rebase(raw);
    if (rel === null) { bad.push([routeOf(f), raw, 'missing base prefix']); continue; }
    // stylesheets, scripts and images are files on disk, not routes
    if (/\.[a-z0-9]{2,5}$/i.test(rel)) {
      if (!fs.existsSync(path.join(root, rel))) bad.push([routeOf(f), raw, 'missing file']);
      continue;
    }
    const u = rel.replace(/\/$/, '');
    if (!exists.has(u)) bad.push([routeOf(f), raw, 'no page']);
  }
  for (const m of html.matchAll(/src="(\/[^"#?]*)"/g)) {
    const rel = rebase(m[1]);
    if (rel === null) { bad.push([routeOf(f), m[1], 'missing base prefix']); continue; }
    if (!fs.existsSync(path.join(root, rel))) bad.push([routeOf(f), m[1], 'missing asset']);
  }
  // Every image goes out as a srcset now, and a `src` that resolves says nothing
  // about the candidates beside it - which is exactly what a visitor downloads.
  for (const m of html.matchAll(/srcset="([^"]+)"/g)) {
    for (const candidate of m[1].split(',')) {
      const url = candidate.trim().split(/\s+/)[0];
      if (!url.startsWith('/')) continue;
      const rel = rebase(url);
      if (rel === null) { bad.push([routeOf(f), url, 'missing base prefix']); continue; }
      if (!fs.existsSync(path.join(root, rel))) bad.push([routeOf(f), url, 'missing srcset asset']);
    }
  }
}

console.log('html pages:', files.length);
console.log('broken internal links/assets:', bad.length);
bad.slice(0, 12).forEach((b) => console.log('  ', b.join(' | ')));
