# 工作日報 PRD

## 概述

把 `CHANGELOG.md` 烘成一份好讀的工作日報靜態網頁，作為 `AI-Workshop-Homework` 的作業繳交物。核心原則：**繳交物是單一靜態 html，`CHANGELOG.md` 是資料來源**——內容於產生當下寫死進去，之後要更新內容就重跑一次產生器。

資料來源是本資料夾內的 `CHANGELOG.md`，這是從 [AI Gen Figma 專案](/Users/eddieshen/Documents/Gen%20Figma%20AI/AI-Gen-Figma/CHANGELOG.md)複製出來的一份**獨立副本**，供這份作業使用；不會回頭修改、也不會自動同步原始檔（見「決策紀錄」）。

本專案原本還有一個「即時同步版」（開瀏覽器、開本機伺服器、每 4 秒自動 fetch 重繪）給 Eddie 自己debug/預覽用，驗證完靜態機制可行後已停用其個人化啟動流程（`start-report.command` 已刪除）——**現在只留靜態繳交這條路徑**。`report.html` 仍保留，但角色改變：它不再是「打開來看」的頁面，純粹是 `generate-static-report.py` 的**內部範本**（共用的 parse/渲染邏輯 + CSS 都在裡面，刪了範本產生器會壞掉，見下方機制說明）。

## 系統組成

| 檔案 | 角色 |
|---|---|
| `CHANGELOG.md` | 資料來源。從 AI Gen Figma 專案複製出來的獨立副本，產生器只讀這份，不讀外部原始檔 |
| `report.html` | **內部範本，非給人打開的頁面**。前端 JS 分兩塊：共用的 parse/渲染邏輯（`window.__report`）+ 一段用註解標記包起來、將被產生器整段替換掉的 bootstrap 佔位區 |
| `generate-static-report.py` | 靜態快照產生器。讀一次 CHANGELOG.md + report.html 範本，烘出單一、可離線開啟的 `MMDD_daily_report_Eddie.html`（作業繳交本體） |
| `regenerate.command` | 產生器的雙擊啟動器。跑 `generate-static-report.py` 並自動開啟產出的 html，免打字 |

## 運作機制

### `report.html`：只當範本，機制沿用「共用邏輯 + 可替換 bootstrap」的設計

`report.html` 的 `<script>` 拆成兩塊：

1. 共用邏輯（`escapeHtml` / `inlineFormat` / `parseChangelog` / `renderList` / `renderEntry` / `renderDays` / `applyDays`，掛在 `window.__report` 上）——parse markdown、渲染 html 的實際邏輯全在這裡
2. 用註解標記包起來的 bootstrap 佔位區（`/* BOOTSTRAP:LIVE:START */` … `/* BOOTSTRAP:LIVE:END */`）——`generate-static-report.py` 會把這整段換成靜態版的 bootstrap

parse 規則：
   - `## YYYY-MM-DD` → 一個日期區塊
   - `### 標題` → 該日期底下的一個條目（entry）；若日期底下沒有 `###`（如最早的 2026-05-20），視為一個無標題條目
   - `- ` bullet → 條目內容，依縮排（每 2 空格一層）組成巢狀清單
   - 行內語法：`**粗體**` → `<strong>`、`` `code` `` → `<code>`、`[文字](連結)` → 只取文字、渲染成不可點的檔名標籤（chip），不解析連結目標

**這份檔案本身不是給人打開的頁面**——它裡面那段 bootstrap 佔位區雖然技術上寫的是「fetch + 輪詢」邏輯（因為開發階段是拿它來即時預覽、驗證 parse 邏輯正確），但正式流程裡沒有任何腳本會把它單獨啟動來看；它唯一的用途是被 `generate-static-report.py` 讀取、替換、產出真正繳交的靜態檔。**不要刪這個檔案**——共用邏輯與 CSS 都只在這裡一份，刪了 `generate-static-report.py` 找不到範本會直接壞掉。

### 靜態快照版（`generate-static-report.py`）—— 實際繳交物的產生方式

為符合 `AI-Workshop-Homework` repo 「作業一律單一 `.html`」的規定而做。

機制：**不重寫 parse/渲染邏輯**，只換「資料怎麼進來」這一段。

1. 讀一次 `report.html` 當範本、讀一次 `CHANGELOG.md` 當資料
2. 把範本裡整段 `BOOTSTRAP:LIVE` 區塊換成一段新的 bootstrap：資料不 fetch，改成把 CHANGELOG 全文用 `json.dumps` 逃脫後直接寫死成 JS 字串常數（另外處理掉 `</script` 避免提早關閉標籤），頁面載入時呼叫共用的 `applyDays()` 渲染一次，不設輪詢
3. 同時把「產生當下」的時間戳（`YYYY-MM-DD HH:MM:SS`）一併寫進去，畫面上 `sourceNote` 顯示「此頁為靜態快照，擷取於 …」、`syncStatus` 顯示「● 靜態快照（離線可讀）」
4. 輸出檔名 `MMDD_daily_report_Eddie.html`（`MMDD` 取產生當下日期），寫在同一資料夾

跑法：雙擊 `regenerate.command`（會自動開啟新產出的 html），或手動 `python3 generate-static-report.py`。CHANGELOG.md 之後若更新、想換一份新快照，重新跑一次即可（不會自動觸發，見下方限制）。

**為何不是 html 裡放一個「更新」按鈕**：瀏覽器基於安全設計，不允許任何網頁（無論靜態或伺服器版）從頁面內執行本機程式——這不是本專案的限制，是所有瀏覽器都擋死的界線。唯一能做到「網頁按鈕觸發 script」的方法是另外常駐一個本機伺服器、按鈕呼叫伺服器端點去執行——但那樣就得依賴伺服器持續運行，違背靜態快照「單一檔案、到處能開」的初衷，所以改用雙擊 `.command` 這個在瀏覽器安全限制下最接近「一鍵」的路徑。

## 已知限制 / 取捨

- **連結不可點**：CHANGELOG 裡的 `[檔名](相對路徑)` 只取檔名文字顯示，不組真實可點連結——避免中文路徑 / 空格編碼不一致導致連結失效或連錯檔案。之後若要做成可點連結需另外處理路徑編碼
- **無自訂字型**：中文內容量大，內嵌 CJK 字型會讓檔案暴增到幾十 MB，改用系統字體（等寬體排數字/日期/代碼、系統中文字體排內文）
- **靜態快照不會自動更新**：CHANGELOG.md 改了之後，已產生的快照內容不會變，要更新須重新執行 `generate-static-report.py`（或雙擊 `regenerate.command`）產生新檔案，不會自動觸發——這是「單一靜態檔可到處開」與「自動跟隨資料變動」兩者不可兼得的必然取捨
- **資料來源副本不會自動跟原始檔同步**：本資料夾的 `CHANGELOG.md` 是手動複製出來的獨立副本，AI Gen Figma 專案那份原始檔之後再更新，這份副本不會跟著變，要更新須重新 `cp` 覆蓋一次（目前無自動化，屬刻意設計——見決策紀錄）

## 決策紀錄

- **2026-07-29**：開發階段曾考慮三種 md↔html 同步方案——(A) 本機伺服器 + fetch 輪詢、(B) File System Access API（僅 Chrome/Edge）、(C) 手動拖曳檔案。選 A 做即時預覽版：跨瀏覽器相容性最好，且能做到「開著不用管、自動更新」的體感，方便驗證 parse 邏輯正確
- **2026-07-29**：資料來源從「讀 AI Gen Figma 專案的外部原始檔」改成「讀本資料夾內的獨立副本」。原因：① Eddie 需要新增測試內容驗證整個機制，但不能動外部那份「實打實」的正式紀錄；② 副本與工具同資料夾後，路徑都能大幅簡化，不用再靠「共同上層資料夾」這種繞路設計；③ 讓這份作業徹底自我包含，不依賴 repo 外部、其他專案的私有路徑。代價：副本不會自動跟著原始 CHANGELOG.md 更新，需要手動 `cp` 覆蓋（見下方限制）
- **2026-07-29**：驗證完整個機制可行後，確認**只有靜態繳交路徑是真正需要的**，即時預覽版對 Eddie 來說只是驗證用的過渡工具。刪除 `start-report.command`（個人化啟動流程），`report.html` 保留但重新定位為「`generate-static-report.py` 的內部範本」，不再是會被單獨打開的頁面

## 關鍵設定值（改動前查這裡）

| 項目 | 值 |
|---|---|
| CHANGELOG.md | 本資料夾內的獨立副本，非外部原始檔（見概述） |
| 靜態快照輸出檔名 | `MMDD_daily_report_Eddie.html`（`MMDD` = 產生當下日期） |

## 變更紀錄

- 2026-07-29：初版建立
- 2026-07-29：搬進 `AI-Workshop-Homework/個人日報 Agent/沈子翔 Eddie/`（本專案其實是該 repo 的工作坊作業）；`start-report.command` 的 `REL_PATH` 同步改新路徑
- 2026-07-29：完成靜態快照版——`report.html` 拆成共用邏輯 + 即時 bootstrap 兩段；新增 `generate-static-report.py`，跑一次烘出 `MMDD_daily_report_Eddie.html`（作業繳交用）。已驗證：離線（零 network request）、內容與即時版一致、擷取時間戳正確顯示
- 2026-07-29：新增 `regenerate.command`（雙擊跑產生器 + 自動開啟結果）。曾考慮「html 內建更新按鈕」，因瀏覽器安全限制（頁面不能執行本機程式）不可行，改採此雙擊方案
- 2026-07-29：把 `CHANGELOG.md` 複製一份進本資料夾，資料來源改為這份獨立副本（不再讀外部原始檔）；`report.html` / `start-report.command` / `generate-static-report.py` 的路徑同步簡化為同資料夾相對路徑。已實測驗證：在副本新增一筆測試條目，即時版 4 秒內自動反映（30 個工作日、更新閃爍提示），重跑產生器也正確烘進新內容（network 僅 html 本體一筆，證實非動態讀取）
- 2026-07-29：驗證通過、移除測試條目後，確認只需要靜態繳交路徑——刪除 `start-report.command`；`report.html` 重新定位為產生器專用的內部範本（不再是給人打開的頁面）；重新產生乾淨的 `0729_daily_report_Eddie.html`（29 個工作日，無測試內容）
