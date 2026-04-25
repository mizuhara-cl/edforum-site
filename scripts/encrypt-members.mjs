#!/usr/bin/env node
/**
 * Encrypt /members/ pages with staticrypt after Astro build.
 *
 * Usage:
 *   STATICRYPT_PASSWORD=xxxx node scripts/encrypt-members.mjs
 */

import { execSync } from 'node:child_process';
import { readdirSync, statSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';

const DIST = resolve(process.cwd(), 'dist');
const MEMBERS = join(DIST, 'members');
const PWD = process.env.STATICRYPT_PASSWORD;

if (!PWD) {
  console.error('[encrypt-members] STATICRYPT_PASSWORD env var is required.');
  process.exit(1);
}

function listHtml(dir) {
  const out = [];
  if (!statSync(dir, { throwIfNoEntry: false })) return out;
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) out.push(...listHtml(full));
    else if (name.endsWith('.html')) out.push(full);
  }
  return out;
}

const files = listHtml(MEMBERS);
if (files.length === 0) {
  console.log('[encrypt-members] No HTML files under dist/members/. Skipping.');
  process.exit(0);
}

console.log(`[encrypt-members] Encrypting ${files.length} file(s) under dist/members/`);

const TITLE = '摂食障害懇話会 会員エリア';
const INSTRUCTIONS = '共有IDとパスワードを入力してください';

for (const f of files) {
  const outDir = dirname(f);
  const args = [
    'staticrypt',
    JSON.stringify(f),
    '--password', JSON.stringify(PWD),
    '--short',
    '-d', JSON.stringify(outDir),
    '--template-title', JSON.stringify(TITLE),
    '--template-instructions', JSON.stringify(INSTRUCTIONS),
    '--template-button', '"ログイン"',
    '--template-placeholder', '"パスワード"',
    '--template-remember', '"このブラウザに保存する"',
    '--template-error', '"パスワードが違います"',
    '--template-color-primary', '"#1F3A5F"',
    '--template-color-secondary', '"#F7F5F0"',
    '--remember', '7',
  ].join(' ');
  try {
    execSync(`npx --yes ${args}`, { stdio: 'inherit', shell: true });
  } catch (e) {
    console.error('[encrypt-members] Failed on', f);
    process.exit(1);
  }
}

console.log('[encrypt-members] Done.');
