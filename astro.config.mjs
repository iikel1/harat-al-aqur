import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import remarkBookCaptions from './src/lib/remark-book-captions.mjs';

const SITE = 'https://iikel1.github.io';
const BASE = '/harat-al-aqur';

const tunnel = process.env.TUNNEL === '1';

export default defineConfig({
  site: SITE,
  base: BASE,

  output: 'static',
  trailingSlash: 'always',

  build: {
    format: 'directory',
  },

  integrations: [
    sitemap({
      i18n: {
        defaultLocale: 'ar',
        locales: {
          ar: 'ar-OM',
          en: 'en-GB',
        },
      },

      filter: (page) => new URL(page).pathname !== '/',
    }),
  ],

  vite: {
    server: {
      allowedHosts: ['.trycloudflare.com'],

      ...(tunnel
        ? {
            hmr: {
              protocol: 'wss',
              clientPort: 443,
            },
          }
        : {}),
    },
  },

  markdown: {
    smartypants: false,
    remarkPlugins: [remarkBookCaptions],
  },
});