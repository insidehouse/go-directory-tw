# 台灣圍棋目錄 — 未來計劃

**日期**: 2026-03-13
**現狀**: 4 Phase 擴展完成，92 schools, 109 pages, Cloudflare Pages 部署中

---

## Phase 5: 驗證與索引（短期，1-2 天）

### 5.1 Google Search Console 提交
- 註冊 GSC，驗證 `go-directory-tw.pages.dev`
- 提交 sitemap (`/sitemap-index.xml`)
- 監控索引狀態、搜尋排名、點擊率

### 5.2 執行 verify-schools.py
- 跑 `python scripts/verify-schools.py` 驗證 92 所學校
- 標記 website 失效、Google Maps 異常的教室
- 更新 `last_verified` 時間戳

### 5.3 補齊缺失資料
- 18 所缺 google_rating/lat/lng 的學校（見 quality-report.txt）
- 手動 Google Maps 查詢，更新 schools.json
- 目標：google_rating >= 95%, lat/lng >= 95%

---

## Phase 6: 內容擴展（中期，依流量決定）

### 6.1 連鎖品牌頁 `/chains/[name]/`
- 名人、黑嘉嘉、中央棋院、長清、碁人等主要連鎖
- 品牌介紹 + 全部分校列表 + 價格比較
- SEO 目標：「名人兒童棋院評價」「黑嘉嘉圍棋分校」

### 6.2 城市比較頁 `/compare/`
- 「台北 vs 新竹圍棋教室比較」等長尾關鍵字
- 學費、教室數量、連鎖佔比等維度比較

### 6.3 Google Maps 嵌入
- School detail page 加互動地圖（87% 有 lat/lng）
- 使用 Google Maps Embed API（免費額度內）

### 6.4 部落格/文章 `/blog/`
- 「2026 台灣圍棋教室推薦 Top 10」
- 「圍棋升段攻略：從入門到業餘 1 段」
- 「各縣市圍棋教室學費比較」
- SEO 長尾內容，增加自然流量入口

---

## Phase 7: 功能強化（中長期）

### 7.1 使用者評論系統
- 家長分享棋院體驗心得
- UGC 內容增加頁面深度和更新頻率
- 技術：可用 Cloudflare D1 或外部服務

### 7.2 體驗課預約表單
- 串接棋院，提供 lead generation
- 表單 → email 通知棋院
- 商業化起點：每筆有效預約收費

### 7.3 搜尋功能強化
- 目前只有 client-side filter（city + age）
- 加入距離排序（使用者 GPS + school lat/lng）
- 加入關鍵字搜尋

---

## Phase 8: 商業化與規模化（長期）

### 8.1 自訂域名
- 從 `pages.dev` 換到 `go-directory.tw`
- 時機：月訪客 > 1,000 或開始商業化時

### 8.2 資料自動更新
- 定期 Outscraper API 刷新 rating/review
- CI 排程（GitHub Actions）每月更新
- 自動偵測歇業教室

### 8.3 棋院認領（Claim）
- 棋院主人可認領頁面，更新資訊
- 付費加值：置頂、特色標記、詳細介紹
- 參考：Google My Business 模式

### 8.4 多語言
- 英文版：Taiwan Go Schools Directory
- 目標：外國人在台灣找圍棋教室

---

## 決策點

| 指標 | 觸發動作 |
|------|----------|
| GSC 索引 > 50 頁 | 開始 Phase 6 內容擴展 |
| 月訪客 > 500 | 加 Google Maps 嵌入 |
| 月訪客 > 1,000 | 自訂域名 + 部落格 |
| 月訪客 > 3,000 | 評論系統 + 預約表單 |
| 有棋院主動聯繫 | 棋院認領功能 |
