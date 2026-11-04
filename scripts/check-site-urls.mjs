#!/usr/bin/env node
// 驗證 build 結果（dist/）裡的網址都指向 astro.config.mjs 的 `site`。
// 用法：node scripts/check-site-urls.mjs [--baseline <頁面清單檔>]
// 任一規則失敗 → exit 1。無外部依賴。

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const dist = join(root, 'dist');
const FORBIDDEN = [/pages\.dev/, /go-directory\.tw/];

const args = process.argv.slice(2);
const baselineIdx = args.indexOf('--baseline');
const baselineFile = baselineIdx >= 0 ? args[baselineIdx + 1] : null;

const config = (await import(pathToFileURL(join(root, 'astro.config.mjs')).href)).default;
if (!config.site) {
  console.error('FAIL astro.config.mjs 沒有設定 site');
  process.exit(1);
}
const SITE = new URL(config.site);
const SITE_ORIGIN = SITE.origin;

if (!existsSync(dist)) {
  console.error('FAIL 找不到 dist/，請先執行 npm run build');
  process.exit(1);
}

const failures = [];
const fail = (rule, msg) => failures.push(`[${rule}] ${msg}`);

function walk(dir) {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
}

const files = walk(dist);
const rel = (p) => relative(dist, p).split(sep).join('/');
const htmlFiles = files.filter((f) => f.endsWith('.html'));

// 由 dist 內檔案位置推出對外路徑：a/b/index.html → /a/b/、404.html → /404.html
function pathOf(file) {
  const r = rel(file);
  if (r === 'index.html') return '/';
  if (r.endsWith('/index.html')) return `/${r.slice(0, -'index.html'.length)}`;
  return `/${r}`;
}
const pagePaths = new Set(htmlFiles.map(pathOf));
const pageExists = (urlStr) => {
  const u = new URL(urlStr);
  return pagePaths.has(decodeURI(u.pathname));
};

// 規則 1：所有輸出檔都不含舊網域
for (const f of files) {
  if (!/\.(html|xml|txt|json|js|css|webmanifest)$/.test(f)) continue;
  const text = readFileSync(f, 'utf8');
  for (const re of FORBIDDEN) {
    if (re.test(text)) fail('no-old-domain', `${rel(f)} 含有 ${re.source.replace(/\\/g, '')}`);
  }
}

// 規則 2：每個 HTML 恰好一個 canonical，指向 SITE 且路徑與檔案位置一致
// 規則 5：JSON-LD 中指向本站的網址必須對應到實際頁面；WebSite.url 必須等於站點根網址
for (const f of htmlFiles) {
  const html = readFileSync(f, 'utf8');
  const canon = [...html.matchAll(/<link[^>]+rel="canonical"[^>]*>/g)].map(
    (m) => (m[0].match(/href="([^"]*)"/) || [])[1],
  );
  const expected = new URL(pathOf(f), SITE_ORIGIN).href;
  if (canon.length !== 1) {
    fail('canonical', `${rel(f)} 有 ${canon.length} 個 canonical`);
  } else if (canon[0] !== expected) {
    fail('canonical', `${rel(f)} canonical=${canon[0]}，預期 ${expected}`);
  }

  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    let data;
    try {
      data = JSON.parse(m[1]);
    } catch (e) {
      fail('json-ld', `${rel(f)} JSON-LD 無法解析：${e.message}`);
      continue;
    }
    const visit = (node) => {
      if (Array.isArray(node)) return node.forEach(visit);
      if (!node || typeof node !== 'object') return;
      if (node['@type'] === 'WebSite' && node.url !== new URL('/', SITE_ORIGIN).href) {
        fail('json-ld', `${rel(f)} WebSite.url=${node.url}，預期 ${new URL('/', SITE_ORIGIN).href}`);
      }
      for (const v of Object.values(node)) {
        if (typeof v === 'string' && /^https?:\/\//.test(v)) {
          const u = new URL(v.replace(/\{[^}]*\}/g, 'x'));
          if (u.origin === SITE_ORIGIN && !pageExists(u.href)) {
            fail('json-ld', `${rel(f)} JSON-LD 指向不存在的頁面 ${v}`);
          }
        } else {
          visit(v);
        }
      }
    };
    visit(data);
  }
}

// 規則 3：sitemap 每個 <loc> 都在 SITE 底下；頁面類 loc 必須對應實際頁面；涵蓋所有頁面
const sitemapFiles = files.filter((f) => /\/sitemap-[^/]*\.xml$/.test(f));
if (sitemapFiles.length === 0) fail('sitemap', '找不到 sitemap-*.xml');
const sitemapPages = new Set();
for (const f of sitemapFiles) {
  const xml = readFileSync(f, 'utf8');
  for (const [, loc] of xml.matchAll(/<loc>([^<]*)<\/loc>/g)) {
    if (!loc.startsWith(`${SITE_ORIGIN}/`)) {
      fail('sitemap', `${rel(f)} 的 <loc> 不在本站：${loc}`);
      continue;
    }
    if (loc.endsWith('.xml')) continue; // sitemap-index 指向子 sitemap
    if (!pageExists(loc)) fail('sitemap', `${rel(f)} 列出不存在的頁面 ${loc}`);
    sitemapPages.add(decodeURI(new URL(loc).pathname));
  }
}
const notInSitemap = [...pagePaths].filter((p) => !sitemapPages.has(p) && !/^\/404(\.html|\/)$/.test(p));
if (notInSitemap.length > 0) {
  fail('sitemap', `${notInSitemap.length} 個頁面不在 sitemap：${notInSitemap.slice(0, 5).join(', ')}`);
}

// 規則 4：robots.txt 的 Sitemap 指向本站 sitemap-index.xml
const robotsPath = join(dist, 'robots.txt');
const expectedSitemap = new URL('/sitemap-index.xml', SITE_ORIGIN).href;
if (!existsSync(robotsPath)) {
  fail('robots', '找不到 dist/robots.txt');
} else {
  const lines = readFileSync(robotsPath, 'utf8').split('\n').filter((l) => /^sitemap:/i.test(l));
  if (lines.length !== 1 || lines[0].replace(/^sitemap:\s*/i, '').trim() !== expectedSitemap) {
    fail('robots', `Sitemap 行為 ${JSON.stringify(lines)}，預期 ${expectedSitemap}`);
  }
  if (!existsSync(join(dist, 'sitemap-index.xml'))) fail('robots', 'robots 指向的 sitemap-index.xml 不存在');
}

// 規則 6（選用）：頁面清單與 baseline 完全相同
if (baselineFile) {
  const base = readFileSync(join(root, baselineFile), 'utf8')
    .split('\n')
    .map((l) => l.trim().replace(/^\.\//, ''))
    .filter(Boolean);
  const now = htmlFiles.map(rel).sort();
  const missing = base.filter((p) => !now.includes(p));
  const added = now.filter((p) => !base.includes(p));
  if (missing.length || added.length) {
    fail('baseline', `頁面清單不同：少了 ${missing.length}（${missing.slice(0, 3).join(', ')}），多了 ${added.length}（${added.slice(0, 3).join(', ')}）`);
  }
}

console.log(`site: ${SITE_ORIGIN}`);
console.log(`HTML 頁數: ${htmlFiles.length}；sitemap 頁數: ${sitemapPages.size}；檢查檔案數: ${files.length}`);
if (baselineFile) console.log(`baseline: ${baselineFile}`);
if (failures.length) {
  console.error(`\nFAIL ${failures.length} 項：`);
  for (const f of failures.slice(0, 50)) console.error(`  ${f}`);
  if (failures.length > 50) console.error(`  …另有 ${failures.length - 50} 項`);
  process.exit(1);
}
console.log('PASS 全部規則通過');
