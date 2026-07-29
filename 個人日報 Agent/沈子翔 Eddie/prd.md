# 工作日報 PRD

## 概述

把 [AI Gen Figma 專案](/Users/eddieshen/Documents/Gen%20Figma%20AI/AI-Gen-Figma/CHANGELOG.md)的 `CHANGELOG.md` 即時渲染成一份好讀的工作日報網頁。核心原則：**html 只是載體，md 是唯一資料來源**——不重新產生 html、不複製內容進本專案，CHANGELOG.md 改了,頁面開著就會自動反映。

## 系統組成

| 檔案 | 角色 |
|---|---|
| `report.html` | 報表本體（即時同步版）。前端 JS 分兩塊：共用的 parse/渲染邏輯（`window.__report`）+ 即時 bootstrap（抓取 → 解析 → 渲染 → 定時輪詢），不含任何寫死的日報內容 |
| `start-report.command` | 啟動器。雙擊執行，開本機伺服器 + 開瀏覽器 |
| `generate-static-report.py` | 靜態快照產生器。讀一次 CHANGELOG.md，烘出單一、可離線開啟的 `MMDD_daily_report_Eddie.html`（作業繳交用） |
| `regenerate.command` | 產生器的雙擊啟動器。跑 `generate-static-report.py` 並自動開啟產出的 html，免打字 |

## 運作機制

### 為何需要本機伺服器

`report.html` 用 `fetch()` 讀取 `CHANGELOG.md`。若直接雙擊 html（`file://` 協定開啟），瀏覽器 CORS 政策會擋掉本機檔案的 `fetch()`，即時同步會失敗（畫面顯示「讀取失敗」）。`start-report.command` 先在 `~/Documents` 開一個 Python 內建的靜態伺服器（`python3 -m http.server`），讓網址變成 `http://localhost:8934/...`，`fetch()` 才被允許。

伺服器根目錄選在 `~/Documents`，因為這是 `report.html` 所在資料夾與 `CHANGELOG.md` 所在資料夾的共同上層——伺服器不能讀取根目錄以外的路徑，兩個檔案得同在一棵樹下才能互相讀到。

### 啟動流程（`start-report.command`）

1. 檢查 port 8934 是否已被佔用（`lsof`）——已有伺服器在跑就跳過，不重複啟動
2. 沒有就在 `~/Documents` 背景啟動 `python3 -m http.server 8934`
3. 用 Python 組出正確編碼過的網址（含中文資料夾名），呼叫系統瀏覽器開啟 `report.html`

### 前端運作（`report.html`）

1. 頁面載入時 `fetch()` 讀取 `CHANGELOG.md`（路徑寫死：`/Gen Figma AI/AI-Gen-Figma/CHANGELOG.md`，相對於伺服器根目錄）
2. 解析 markdown 為結構化資料，規則：
   - `## YYYY-MM-DD` → 一個日期區塊
   - `### 標題` → 該日期底下的一個條目（entry）；若日期底下沒有 `###`（如最早的 2026-05-20），視為一個無標題條目
   - `- ` bullet → 條目內容，依縮排（每 2 空格一層）組成巢狀清單
   - 行內語法：`**粗體**` → `<strong>`、`` `code` `` → `<code>`、`[文字](連結)` → 只取文字、渲染成不可點的檔名標籤（chip），不解析連結目標
3. 依日期所屬月份自動分段、產生月份跳轉導覽
4. 每 4 秒重新 `fetch()` 一次；內容若有變化才重繪（避免打斷閱讀捲動位置），並閃一下提示已更新；每次都更新畫面右上角「已同步 HH:MM:SS」時間戳
5. `fetch` 失敗（伺服器沒開）時,同步狀態顯示「讀取失敗」提示

### 靜態快照版（`generate-static-report.py`）

為符合 `AI-Workshop-Homework` repo 「作業一律單一 `.html`」的規定而做——即時同步版依賴本機伺服器與 fetch，離開 Eddie 電腦打不開，不能拿來繳交。

機制：**不重寫 parse/渲染邏輯**，只換「資料怎麼進來」這一段。

1. `report.html` 的 `<script>` 拆成兩塊：共用邏輯（`escapeHtml` / `inlineFormat` / `parseChangelog` / `renderList` / `renderEntry` / `renderDays` / `applyDays`，掛在 `window.__report` 上供外部呼叫）+ 用註解標記包起來的即時 bootstrap（`/* BOOTSTRAP:LIVE:START */` … `/* BOOTSTRAP:LIVE:END */`，做 fetch + 輪詢那段）
2. `generate-static-report.py` 讀一次 `report.html` 當範本、讀一次 `CHANGELOG.md` 當資料，把範本裡整段 `BOOTSTRAP:LIVE` 區塊換成一段新的 bootstrap：資料不 fetch，改成把 CHANGELOG 全文用 `json.dumps` 逃脫後直接寫死成 JS 字串常數（另外處理掉 `</script` 避免提早關閉標籤），頁面載入時呼叫共用的 `applyDays()` 渲染一次，不設輪詢
3. 同時把「產生當下」的時間戳（`YYYY-MM-DD HH:MM:SS`）一併寫進去，畫面上 `sourceNote` 顯示「此頁為靜態快照，擷取於 …」、`syncStatus` 顯示「● 靜態快照（離線可讀）」，不會誤導成即時版
4. 輸出檔名 `MMDD_daily_report_Eddie.html`（`MMDD` 取產生當下日期），寫在同一資料夾

跑法：雙擊 `regenerate.command`（會自動開啟新產出的 html），或手動 `python3 generate-static-report.py`。CHANGELOG.md 之後若更新、想換一份新快照，重新跑一次即可（不會自動觸發，見下方限制）。

**為何不是 html 裡放一個「更新」按鈕**：瀏覽器基於安全設計，不允許任何網頁（無論靜態或伺服器版）從頁面內執行本機程式——這不是本專案的限制，是所有瀏覽器都擋死的界線。唯一能做到「網頁按鈕觸發 script」的方法是另外常駐一個本機伺服器、按鈕呼叫伺服器端點去執行——但那樣就得依賴伺服器持續運行，違背靜態快照「單一檔案、到處能開」的初衷，所以改用雙擊 `.command` 這個在瀏覽器安全限制下最接近「一鍵」的路徑。

## 已知限制 / 取捨

- **輪詢非真即時**：用 4 秒定時重讀模擬「即時」，不是檔案系統事件推播（瀏覽器沙盒沒有原生檔案監看能力）
- **連結不可點**：CHANGELOG 裡的 `[檔名](相對路徑)` 只取檔名文字顯示，不組真實可點連結——避免中文路徑 / 空格編碼不一致導致連結失效或連錯檔案。之後若要做成可點連結需另外處理路徑編碼
- **無自訂字型**：中文內容量大，內嵌 CJK 字型會讓檔案暴增到幾十 MB，改用系統字體（等寬體排數字/日期/代碼、系統中文字體排內文）
- **需要伺服器持續運行**：電腦重開機、或手動關掉 terminal/伺服器行程後，需要重新雙擊 `start-report.command`
- **only 支援本機**：目前只服務 Eddie 自己的 Mac，未考慮多人共用或雲端部署
- **靜態快照不會自動更新**：這是它跟即時版的必然取捨（單一靜態檔 vs 自動跟隨外部檔案，兩者不可兼得）——CHANGELOG.md 改了之後，快照內容不會變，要更新須重新執行 `generate-static-report.py` 產生新檔案，不會自動觸發

## 決策紀錄

- **2026-07-29**：曾考慮三種 md↔html 同步方案——(A) 本機伺服器 + fetch 輪詢、(B) File System Access API（僅 Chrome/Edge）、(C) 手動拖曳檔案。選 A：跨瀏覽器相容性最好，且能做到「開著不用管、自動更新」的體感，最貼近「即時」的需求

## 關鍵設定值（改動前查這裡）

| 項目 | 值 |
|---|---|
| 本機伺服器 port | `8934` |
| 伺服器根目錄 | `~/Documents` |
| CHANGELOG.md 絕對路徑 | `/Users/eddieshen/Documents/Gen Figma AI/AI-Gen-Figma/CHANGELOG.md` |
| 輪詢間隔 | 4000ms |

## 變更紀錄

- 2026-07-29：初版建立
- 2026-07-29：搬進 `AI-Workshop-Homework/個人日報 Agent/沈子翔 Eddie/`（本專案其實是該 repo 的工作坊作業）；`start-report.command` 的 `REL_PATH` 同步改新路徑
- 2026-07-29：完成靜態快照版——`report.html` 拆成共用邏輯 + 即時 bootstrap 兩段；新增 `generate-static-report.py`，跑一次烘出 `MMDD_daily_report_Eddie.html`（作業繳交用）。已驗證：離線（零 network request）、內容與即時版一致、擷取時間戳正確顯示
- 2026-07-29：新增 `regenerate.command`（雙擊跑產生器 + 自動開啟結果）。曾考慮「html 內建更新按鈕」，因瀏覽器安全限制（頁面不能執行本機程式）不可行，改採此雙擊方案
