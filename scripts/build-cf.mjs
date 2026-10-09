// Cloudflare Pages 用のビルド（独自ドメインのルートに置く版）。
// astro.config.mjs は GitHub Pages の仮サイト（/edforum-site）のまま残し、ここで上書きして dist-cf/ に出す。
import { build } from 'astro';
import { readFileSync, writeFileSync } from 'node:fs';

await build({
  site: 'https://eatingdisorderforum.net',
  base: '/',
  outDir: './dist-cf',
});

// 旧サイト（2011年版・*.html）のアドレスを新しいページへ 301 で送る。Cloudflare Pages が読む _redirects。
// 資料ページの slug は旧サイトのファイル名をそのまま使っている（diet1.html → /resources/diet1/）。
const legacyPages = {
  '/gaiyou.html': '/about/',
  '/yakuin.html': '/officers/',
  '/ayumi.html': '/archive/',
  '/yotei.html': '/archive/',
  '/toiawase.html': '/contact/',
};
const resources = JSON.parse(readFileSync('./src/data/resources.json', 'utf-8'));
for (const { slug } of resources) legacyPages[`/${slug}.html`] = `/resources/${slug}/`;

const lines = Object.entries(legacyPages).map(([from, to]) => `${from} ${to} 301`);
writeFileSync('./dist-cf/_redirects', lines.join('\n') + '\n');
console.log(`_redirects: ${lines.length} 件`);
