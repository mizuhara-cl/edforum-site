# 摂食障害懇話会 サイト（仮ローンチ版）

関西の摂食障害治療者が集う症例検討会・勉強会「**摂食障害懇話会**」（Eating Disorder Forum）の公式サイトの仮リニューアル版。

## 概要

- **位置づけ**: 世話人会への提案用プロトタイプ
- **本番URL**: 仮 → https://mizuhara-cl.github.io/edforum-site/
- **既存サイト**: https://eatingdisorderforum.net/ （2011年構築・Shift_JIS）
- **将来**: ドメイン `eatingdisorderforum.net` をCloudflare移管予定

## 技術スタック

- Astro 4.x（静的サイト生成）
- GitHub Pages（自動デプロイ）
- staticrypt（会員エリアのパスワード保護）
- Pagefind（全文検索・将来）

## 開発

```bash
npm install
npm run dev          # http://localhost:4321
npm run build        # dist/ に出力
npm run build:protected  # ビルド後、/members/配下をstaticryptで暗号化
```

## デプロイ

`main` ブランチへ push すると、GitHub Actions が自動でビルド & GitHub Pages にデプロイ。
`.github/workflows/deploy.yml` 参照。

## 会員エリア（staticrypt）

`/members/` 配下のページは、ビルド時に共有パスワードで暗号化される。  
パスワードは GitHub Secrets `MEMBERS_PASSWORD` で管理。
