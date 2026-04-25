// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://mizuhara-cl.github.io',
  base: '/edforum-site',
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
});
