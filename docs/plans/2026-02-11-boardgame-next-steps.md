# Board Game Directory — 進度與下一步

## 已完成

### 1. Brainstorming（產品定位）
- 確認方向：決策樹問卷 + 目錄，先問卷後目錄
- 目標用戶：新手 + 有經驗玩家
- 資料策略：BGG + 台灣電商 + 手動補充
- Tech stack：Astro + Tailwind（沿用圍棋目錄）

### 2. Competitor Analysis（競品分析）
- 國際：Quantic Foundry, Gather Together, BGG, Recommend.Games 等 8 個工具
- 台灣：瘋桌遊, Gokids, 桌遊好地方, 栢龍玩具, WOB, mybest
- 結論：**繁體中文互動式推薦 = 零競爭**

### 3. Market Research（市場研究）
- 全球市場 USD 15-17B, CAGR 8-12%
- 台灣 300+ 桌遊店, 21.7M 網路用戶
- TAM/SAM/SOM 估算完成
- 變現策略：蝦皮/momo 聯盟行銷為主
- 報告：`docs/plans/2026-02-11-boardgame-market-research.md`

### 4. Implementation Plan（技術計畫，已批准）
- 完整檔案結構、資料模型、決策樹設計
- 從 go-directory-tw fork 的改造指南
- 計畫：`~/.claude/plans/parallel-orbiting-blanket.md`

---

## 未完成 — 下一步行動

### 5. Data Collection（資料收集）
**目標：** 建立 `games.json`（30 款）+ `tree.json`（決策樹）

- [ ] 從文章提取所有桌遊名稱、推薦理由、分類位置
- [ ] 用 BGG API 補充：評分、人數、時長、複雜度、封面圖
- [ ] 確認每款在台灣的可購買性（Gokids/Shopee 搜尋）
- [ ] 為每款填寫三維度指標：學習難度 / 入門助益 / 桌面麻煩度
- [ ] 建立 `tree.json` 決策樹結構（約 15-20 個節點）

**可用指令：** `/brainstorming` 繼續討論資料結構細節

### 6. Project Scaffolding（專案建立）
**目標：** 初始化專案、搬移可重用程式碼

- [ ] 決定專案位置（`d:\OneDrive\Claude\boardgame-directory-tw\`？）
- [ ] `pnpm create astro@latest` 初始化
- [ ] 從 go-directory-tw 複製：BaseLayout, Header, Footer, config files
- [ ] 調整品牌名稱、色系（暖色調）、導航連結
- [ ] 確認 `pnpm dev` 能跑

### 7. Implementation（實作，分 4 個 sprint）

**Sprint 1 — 目錄核心**
- [ ] `BoardGameCard.astro` 卡片組件
- [ ] `games/index.astro` 目錄頁 + 篩選（人數/時長/類型/難度）
- [ ] `games/[id].astro` 個別桌遊頁
- [ ] 首頁 `index.astro`（Hero + 卡片網格）

**Sprint 2 — 問卷核心**
- [ ] `match/index.astro` 問卷頁（client-side state machine）
- [ ] `match/result.astro` 結果頁（推薦 + 理由 + 三維度指標）
- [ ] URL query params 分享功能
- [ ] 問卷動畫與轉場

**Sprint 3 — SEO & Polish**
- [ ] Schema.org Product markup
- [ ] Open Graph meta tags
- [ ] Sitemap + robots.txt
- [ ] Responsive 測試（mobile/tablet/desktop）
- [ ] Lighthouse 90+ 全項

**Sprint 4 — Deploy & Launch**
- [ ] 部署到 Cloudflare Pages
- [ ] 設定 domain（如果有）
- [ ] PTT/Dcard 發文測試
- [ ] Facebook 桌遊社團分享

### 8. Post-Launch（上線後）
- [ ] 監控 Google Search Console 收錄狀況
- [ ] 申請蝦皮分潤計畫
- [ ] 擴充資料庫到 100+ 款
- [ ] 撰寫 SEO 文章（"2026 桌遊推薦" 等）

---

## 關鍵文件位置

| 文件 | 路徑 |
|------|------|
| 市場研究報告 | `docs/plans/2026-02-11-boardgame-market-research.md` |
| 技術實作計畫 | `~/.claude/plans/parallel-orbiting-blanket.md` |
| 參考文章（決策樹邏輯） | 對話中提供的桌遊選購文章 |
| 圍棋目錄（可重用架構） | `d:\OneDrive\Claude\go-directory-tw\` |

## 下次開始時的指令

```
幫我建立 boardgame-directory-tw 專案，按照
docs/plans/2026-02-11-boardgame-next-steps.md 的步驟 6 開始。
```

或如果要先做資料收集：

```
幫我建立 games.json 和 tree.json，
基於之前對話中的桌遊選購文章 + BGG 資料。
```
