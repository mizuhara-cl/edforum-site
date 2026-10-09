// Cloudflare Pages 用のビルド（独自ドメインのルートに置く版）。
// astro.config.mjs は GitHub Pages の仮サイト（/edforum-site）のまま残し、ここで上書きして dist-cf/ に出す。
import { build } from 'astro';

await build({
  site: 'https://eatingdisorderforum.net',
  base: '/',
  outDir: './dist-cf',
});
