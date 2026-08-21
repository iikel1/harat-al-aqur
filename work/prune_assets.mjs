// Astro emits the ORIGINAL file for every image it imports, alongside the
// resized variants it actually puts in the srcset. Nothing links to those
// originals - the whole point of the pipeline is that no page hands out a
// 1418px JPEG - so all 113 of them, 10.4 MB, were riding along in dist/ where
// only the deploy paid for them.
//
// This deletes any image in dist/_astro/ whose filename appears nowhere in the
// built output. It reads every text file in dist/ (html, css, js, xml, txt), so
// a variant named only from a script or a stylesheet still counts as referenced.
// It only ever considers image extensions: JS chunks and CSS are left alone.
//
// Run after `astro build`, before `check:links`.
import fs from 'node:fs';
import path from 'node:path';

const root = 'dist';
const assets = path.join(root, '_astro');
if (!fs.existsSync(assets)) {
  console.log('prune:assets - nothing to do (no dist/_astro)');
  process.exit(0);
}

const TEXT = /\.(html|css|js|mjs|json|xml|txt|webmanifest|svg)$/i;
const IMAGE = /\.(avif|webp|jpe?g|png|gif)$/i;

let haystack = '';
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (TEXT.test(e.name)) haystack += fs.readFileSync(p, 'utf8');
  }
})(root);

let freed = 0;
let gone = 0;
for (const name of fs.readdirSync(assets)) {
  if (!IMAGE.test(name)) continue;
  if (haystack.includes(name)) continue;
  const p = path.join(assets, name);
  freed += fs.statSync(p).size;
  fs.rmSync(p);
  gone++;
}

console.log(`prune:assets - ${gone} unreferenced images removed, ${(freed / 1024 / 1024).toFixed(1)} MB`);
