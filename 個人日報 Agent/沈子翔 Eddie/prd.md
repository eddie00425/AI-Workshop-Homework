# 工作日報 PRD

## 概述

把 [AI Gen Figma 專案](/Users/eddieshen/Documents/Gen%20Figma%20AI/AI-Gen-Figma/CHANGELOG.md)的 `CHANGELOG.md` 即時渲染成一份好讀的工作日報網頁。核心原則：**html 只是載體，md 是唯一資料來源**——不重新產生 html、不複製內容進本專案，CHANGELOG.md 改了,頁面開著就會自動反映。

## 系統組成

| 檔案 | 角色 |
|---|---|
| `report.html` | 報表本體。純前端 JS：抓取 → 解析 → 渲染 → 定時輪詢，不含任何寫死的日報內容 |
| `start-report.command` | 啟動器。雙擊執行，開本機伺服器 + 開瀏覽器 |

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

## 已知限制 / 取捨

- **輪詢非真即時**：用 4 秒定時重讀模擬「即時」，不是檔案系統事件推播（瀏覽器沙盒沒有原生檔案監看能力）
- **連結不可點**：CHANGELOG 裡的 `[檔名](相對路徑)` 只取檔名文字顯示，不組真實可點連結——避免中文路徑 / 空格編碼不一致導致連結失效或連錯檔案。之後若要做成可點連結需另外處理路徑編碼
- **無自訂字型**：中文內容量大，內嵌 CJK 字型會讓檔案暴增到幾十 MB，改用系統字體（等寬體排數字/日期/代碼、系統中文字體排內文）
- **需要伺服器持續運行**：電腦重開機、或手動關掉 terminal/伺服器行程後，需要重新雙擊 `start-report.command`
- **only 支援本機**：目前只服務 Eddie 自己的 Mac，未考慮多人共用或雲端部署

## 決策紀錄

- **2026-07-29**：曾考慮三種 md↔html 同步方案——(A) 本機伺服器 + fetch 輪詢、(B) File System Access API（僅 Chrome/Edge）、(C) 手動拖曳檔案。選 A：跨瀏覽器相容性最好，且能做到「開著不用管、自動更新」的體感，最貼近「即時」的需求

## 關鍵設定值（改動前查這裡）

| 項目 | 值 |
|---|---|
| 本機伺服器 port | `8934` |
| 伺服器根目錄 | `~/Documents` |
| CHANGELOG.md 絕對路徑 | `/Users/eddieshen/Documents/Gen Figma AI/AI-Gen-Figma/CHANGELOG.md` |
| 輪詢間隔 | 4000ms |

## 待辦

- **靜態快照版（作業繳交用）**：`AI-Workshop-Homework` repo 規定作業一律是單一 `.html`（見 repo 根目錄 README.md），這份即時同步版不符合（多檔案、需本機伺服器、離開 Eddie 電腦打不開）。待做：另外產出一份「內容於產生當下寫死」的單一 html，沿用同一套視覺設計，命名為 `MMDD_daily_report_Eddie.html`，放在同一資料夾內一併繳交。此即時同步版本身保留、不受影響

## 變更紀錄

- 2026-07-29：初版建立
- 2026-07-29：搬進 `AI-Workshop-Homework/個人日報 Agent/沈子翔 Eddie/`（本專案其實是該 repo 的工作坊作業）；`start-report.command` 的 `REL_PATH` 同步改新路徑
