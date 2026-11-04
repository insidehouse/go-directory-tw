import type { APIRoute } from 'astro';

// robots.txt 由 astro.config.mjs 的 `site` 產生，避免 sitemap 網址和正式網域不一致
export const GET: APIRoute = ({ site }) => {
  if (!site) throw new Error('astro.config.mjs 缺少 site 設定');
  const sitemapUrl = new URL('/sitemap-index.xml', site).href;
  return new Response(`User-agent: *\nAllow: /\n\nSitemap: ${sitemapUrl}\n`, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
