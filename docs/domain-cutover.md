# 網域切換：go-directory-tw.pages.dev → weiqi.tw

狀態（2026-11-04 查證）：

- `weiqi.tw` 已在 Porkbun 註冊。nameserver 是 `*.ns.porkbun.com`，A 記錄目前指向 Porkbun 停車頁（`pixie.porkbun.com`）。
- 正式站 `https://go-directory-tw.pages.dev` 回 200。
- 舊的 `public/robots.txt` 把 sitemap 指向 `https://go-directory.tw/...`，但這個網域不存在（NXDOMAIN）。本 PR 已修正。

> ⚠️ **完成下面 1–3 步、確認 `https://weiqi.tw/` 能開之前，不要 merge 本 PR。**
> 本 PR 會把所有 canonical、sitemap、JSON-LD 改成 `https://weiqi.tw`。網域還沒接上就部署的話，搜尋引擎會被導向停車頁。

## 需要手動完成的步驟

1. **把 `weiqi.tw` 加進 Cloudflare，成為一個 zone，並改用 Cloudflare nameserver**
   - Pages 綁定 apex domain（不帶 `www`）時，該網域必須是同一個 Cloudflare 帳號底下的 zone，nameserver 也要指向 Cloudflare。
   - 做法：Cloudflare dashboard → Add a site → `weiqi.tw` → 選 Free plan → 照畫面把 Porkbun 的 nameserver 改成 Cloudflare 給的兩組。
   - 文件：<https://developers.cloudflare.com/pages/configuration/custom-domains/>
2. **在 Pages 專案加上 custom domain**
   - Workers & Pages → `go-directory-tw` → Custom domains → Set up a domain → `weiqi.tw`。Cloudflare 會自動建立 CNAME。
   - 想讓 `www.weiqi.tw` 也能開，就再加一次 `www.weiqi.tw`。
   - 注意：要先在 Pages 設定好 custom domain，再處理 DNS。手動先建 CNAME 會導致 522 錯誤（同一份文件有說明）。
3. **確認網域已生效**

   ```bash
   curl -sI https://weiqi.tw/ | head -1        # 預期 HTTP/2 200
   curl -s https://weiqi.tw/robots.txt          # 這時還是舊版，正常
   ```

4. **Merge 本 PR**。Cloudflare Pages 會自動部署。部署完成後：

   ```bash
   curl -s https://weiqi.tw/robots.txt          # 預期 Sitemap: https://weiqi.tw/sitemap-index.xml
   curl -s https://weiqi.tw/ | grep -o 'rel="canonical" href="[^"]*"'
   ```

5. **把 `*.pages.dev` 301 轉到 `weiqi.tw`**
   - 用 Cloudflare Bulk Redirects：source 填 `go-directory-tw.pages.dev`，target 填 `https://weiqi.tw`，status 301，勾選 preserve query string、subpath matching、preserve path suffix。
   - 文件：<https://developers.cloudflare.com/pages/how-to/redirect-to-custom-domain/>
   - **未確認**：官方文件也建議勾選「include subdomains」，但這可能連 preview deployment（`<hash>.go-directory-tw.pages.dev`）一起轉走。官方頁面沒有提到 preview，要先測試。
6. **Google Search Console**
   - 新增「網域」資源 `weiqi.tw`，用 DNS TXT 驗證（在 Cloudflare 加 TXT 記錄）。
   - 驗證後提交 `https://weiqi.tw/sitemap-index.xml`。
   - 舊的 `pages.dev` 資源可以用「網址變更」工具，前提是第 5 步的 301 已經生效。
   - `BaseLayout.astro` 裡的 `google-site-verification` meta 是舊資源用的，留著不影響任何東西。改用 DNS 驗證後可以考慮移除。

## 驗收方式（任何時候都能重跑）

```bash
npm ci
npm run check            # build + 檢查網址，exit 0 才算通過
npm run check:cutover    # 再加一項：頁面清單必須和切換前的 baseline 完全相同
```

`scripts/check-site-urls.mjs` 檢查的規則：

1. `dist/` 的所有輸出檔不含 `pages.dev`、`go-directory.tw`。
2. 每個 HTML 恰好一個 canonical，指向 `site`，而且路徑和檔案位置一致。
3. sitemap 的每個 `<loc>` 都在 `site` 底下，對應到實際存在的頁面，並涵蓋所有頁面。
4. `robots.txt` 只有一行 Sitemap，值等於 `${site}/sitemap-index.xml`。
5. JSON-LD 中指向本站的網址都對應到實際存在的頁面；`WebSite.url` 等於站點根網址。
6. （僅 `check:cutover`）HTML 頁面清單和 `docs/evidence/2026-11-04-batch1/baseline-pages.txt` 相同。

以後新增或移除頁面時，`check:cutover` 會失敗，這是預期行為，日常用 `npm run check` 即可。

## 以後再換網域

只需要改 `astro.config.mjs` 的 `site`，然後跑 `npm run check`。robots.txt（`src/pages/robots.txt.ts`）、canonical、OG、JSON-LD 都會從 `site` 自動產生。
