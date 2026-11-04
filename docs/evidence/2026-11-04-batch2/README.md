# 批次 2 驗收證據（2026-11-04，GMT+8）

| 檔案 | 內容 |
|---|---|
| verification-report.txt | 修正後的 `verify-schools.py` 對 91 筆棋院的實際檢查結果：64 筆通過、4 筆網站有問題、3 筆轉址到別的網域、20 筆沒有網站 |
| data-diff.md | 資料變動的程式比對結果（只有 `last_verified` 變動，共 64 筆）、腳本修正說明、7 筆需人工確認的清單和建議 |
| regression-test.txt | 加上 `--skip-web`、完全不做網路檢查時：舊版腳本把 91/91 筆標成已驗證，新版是 0/91 |
| check-output.txt | `npm ci && npm run check:cutover`：PASS，exit=0（119 頁，和 baseline 相同） |

另外確認：build 後的棋院頁面中，顯示「最後驗證：2026-11-04」的有 64 頁，顯示「2026-03-29」的有 27 頁，合計 91 頁。
