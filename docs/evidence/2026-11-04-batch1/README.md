# 批次 1 驗收證據（2026-11-04，GMT+8）

| 檔案 | 內容 |
|---|---|
| baseline-pages.txt | 改動前 `npm run build` 產生的 119 個 HTML 頁面清單 |
| negative-test-old-build.txt | 用新的檢查腳本掃改動前的 dist：364 項失敗、exit=1（證明腳本確實抓得到舊網域） |
| check-output.txt | 改動後 `npm run check:cutover` 的完整輸出：119 頁、sitemap 119 頁、PASS、exit=0 |

重跑方式：`npm ci && npm run check:cutover`
