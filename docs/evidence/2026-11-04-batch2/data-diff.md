# 批次 2：棋院資料重新驗證（2026-11-04，GMT+8 17:28–17:31）

## 資料變動

用程式比對改動前後的 `src/data/schools.json`：

| 項目 | 結果 |
|---|---|
| 筆數 | 91 → 91（沒有刪除，也沒有新增） |
| 有變動的欄位 | 只有 `last_verified` |
| 有變動的筆數 | 64 筆，`2026-03-29` → `2026-11-04` |
| 更新依據 | 該校網站用 HEAD 檢查（失敗時改用 GET）回 2xx/3xx，且最後停在同一個網域 |

其他 27 筆保留原本的日期，原因分成三類：網站有問題（4 筆）、轉址到別的網域（3 筆）、沒有網站（20 筆）。

## 修正 `scripts/verify-schools.py` 的兩個問題

1. **Google Maps 檢查沒有實際意義**
   - 用一個捏造的 `place_id`（`ChIJTHIS_IS_FAKE_000000000`）測試，HEAD 和 GET 都回 200，和真的 place_id 結果一樣。
   - 所以這項檢查只能證明 google.com 連得上，不能證明這間棋院存在。
   - 改成只列入報告供參考，不再作為更新 `last_verified` 的依據。
2. **沒有做任何檢查也會更新日期**
   - 原本的邏輯是「沒有發現問題就更新」，所以沒有網站的學校，或加了 `--skip-web` 參數時，也會被標成已驗證。
   - 改成只有網站檢查真的通過才更新。
   - 這次如果用舊邏輯跑，20 筆沒有網站的學校會在完全沒驗證的情況下拿到新日期。

其他小改動：

- HEAD 失敗時改用 GET 重試，因為有些伺服器不接受 HEAD 請求。
- 轉址到別的網域時列為需人工確認（網域可能已過期被停放，或已經賣掉）。
- 新增 `--output` 參數，可以指定報告存到哪裡。
- 結尾印出的「更新筆數」原本算錯，已改正。

## 需要人工確認（7 筆）

| 棋院 | 城市 | 檢查結果 | 交叉確認 | 建議 |
|---|---|---|---|---|
| 上善若水圍棋教室 | 新北 | `gogohappy123.weebly.com` 回 404 | curl 也是 404 | 網站很可能已經關閉。到 Google Maps 或 FB 確認是否還在營業，再決定移除網址或標示為歇業 |
| 蘇老師櫻花圍棋教室 | 台中 | `sakurago.weebly.com` 回 404 | curl 也是 404 | 同上 |
| 心弈圍棋苑 | 嘉義 | HTTPS 連線被重置 | HTTP 回 302，伺服器還在。只有從雲端環境連 HTTPS 會失敗 | **可能是雲端環境的網路問題**。請用瀏覽器開開看，能開就不用改 |
| 心弈圍棋苑（嘉科分苑） | 嘉義 | 同上（同一個網站） | 同上 | 同上 |
| 黑嘉嘉圍棋（新竹巨城分校） | 新竹 | `heijiajia.com.tw` 轉址到 `heijiajia.com/zh-hant` | curl 確認，最後回 200 | 品牌官網換了網域，屬於正常情況。可以把 `website` 改成 `https://www.heijiajia.com/zh-hant`（這次沒改，留給你決定） |
| 黑嘉嘉圍棋（新竹竹北分校） | 新竹 | 同上 | 同上 | 同上 |
| 三重棋院（小小林圍棋） | 新北 | `lin.ee` 轉址到 `line.me` | — | 這是 LINE 官方帳號的短網址，屬於正常情況，不需要處理 |

## 無法自動驗證（20 筆，沒有網站）

清單在 `verification-report.txt` 的「Not Auto-Verifiable」段落。這 20 筆的 `last_verified` 維持 `2026-03-29`。要更新只能人工到 Google Maps 確認營業狀態。這次 Maps 檢查已證明沒有參考價值，所以沒有拿它來更新。

## 限制

- 網站回 200 只代表網站還在，不代表棋院還在營業，也不代表課程和價格是最新的。
- 這次沒有用 Google Places API。專案裡沒有 API key，而且依照範圍不新增付費服務。

## 重跑方式

```bash
python3 scripts/verify-schools.py --dry-run --output /tmp/report.txt   # 只產生報告，不改資料
python3 scripts/verify-schools.py --output docs/evidence/<日期>/verification-report.txt
npm run check:cutover                                                   # 確認頁面和網址不受影響
```
