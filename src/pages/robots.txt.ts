import type { APIRoute } from 'astro';

// Generated rather than dropped in public/ so the Sitemap line follows `site`
// in astro.config.mjs. That domain is still provisional — see the note there.
export const GET: APIRoute = ({ site }) => {
  const body = [
    'User-agent: *',
    'Allow: /',
    '',
    `Sitemap: ${new URL('sitemap-index.xml', site)}`,
    ''
  ].join('\n');

  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  });
};
