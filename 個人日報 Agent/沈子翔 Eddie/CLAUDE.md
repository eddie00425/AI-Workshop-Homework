# 工作日報 Agent（沈子翔 Eddie）

## 這是什麼

一份**即時渲染**的工作日報網頁，資料來源是 [AI Gen Figma 專案](/Users/eddieshen/Documents/Gen%20Figma%20AI/AI-Gen-Figma/)的 `CHANGELOG.md`。本資料夾只放渲染用的 html／啟動腳本，不放任何日報內容本身——內容永遠即時讀自來源 md，不重寫、不複製。

本資料夾是 `AI-Workshop-Homework` repo 的「個人日報 Agent」作業繳交子資料夾。**注意**：repo 的 [README.md](../../README.md) 規定作業一律以單一 `.html` 檔案繳交（`MMDD_daily_report_Eddie.html`），即時同步版（多檔案、依賴本機伺服器）不符合此格式，是 Eddie 自己留用的工具；實際繳交的是 `generate-static-report.py` 產生的**靜態快照版單一 html**（決策脈絡見 prd.md）。

完整運作原理、架構、已知限制、決策脈絡見 [prd.md](prd.md)。

## 檔案結構

| 檔案 | 用途 |
|---|---|
| `report.html` | 報表頁面本體（即時同步版，fetch + parse + render + 輪詢，純前端 JS） |
| `start-report.command` | 即時同步版雙擊啟動：開本機伺服器 + 開瀏覽器 |
| `generate-static-report.py` | 靜態快照產生器：讀一次 CHANGELOG.md，烘出作業繳交用的 `MMDD_daily_report_Eddie.html` |
| `regenerate.command` | 產生器雙擊啟動：跑 `generate-static-report.py` 並自動開啟結果 |
| `MMDD_daily_report_Eddie.html` | 實際繳交的作業本體（靜態快照，內容凍結於產生當下） |
| `prd.md` | 這個工具的完整規格文件（架構、機制、限制、決策紀錄） |

## Rules

- **改動前先讀 `prd.md`**：機制、路徑、port 等設定值都記在裡面，別憑印象改
- **改完同步更新 `prd.md`**：新需求、行為變動、取捨都要落地寫進去（尤其「變更紀錄」段），不留只在對話裡、日後會遺忘的決定
- **html 是渲染殼，CHANGELOG.md 是唯一資料來源**：不要把日報內容寫死進 `report.html`，也不要把 CHANGELOG 內容複製進本資料夾
- **語言**：繁體中文優先，程式碼識別字維持原文
- **done**：使用者說「done」＝直接 `git add` + commit + push（不需先確認 commit message），push 後回報 commit 內容
