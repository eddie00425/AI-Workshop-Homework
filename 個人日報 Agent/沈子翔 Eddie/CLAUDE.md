# 工作日報 Agent（沈子翔 Eddie）

## 這是什麼

一份靜態渲染的工作日報網頁，資料來源是本資料夾內的 `CHANGELOG.md`——這是從 [AI Gen Figma 專案](/Users/eddieshen/Documents/Gen%20Figma%20AI/AI-Gen-Figma/)複製出來的**獨立副本**（為了讓這份作業自我包含、也讓 Eddie 能自由加測試內容驗證機制，不用去動外部那份正式紀錄；副本不會自動跟原始檔同步，見 prd.md）。

本資料夾是 `AI-Workshop-Homework` repo 的「個人日報 Agent」作業繳交子資料夾。repo 的 [README.md](../../README.md) 規定作業一律以單一 `.html` 檔案繳交（`MMDD_daily_report_Eddie.html`），實際繳交的就是 `generate-static-report.py` 產生的**靜態快照版單一 html**。開發階段曾有一個「即時同步版」（開瀏覽器即時預覽）方便驗證 parse 邏輯，驗證通過後其個人化啟動流程已刪除，只留靜態繳交這條路徑（決策脈絡見 prd.md）。

完整運作原理、架構、已知限制、決策脈絡見 [prd.md](prd.md)。

## 檔案結構

| 檔案 | 用途 |
|---|---|
| `CHANGELOG.md` | 資料來源：AI Gen Figma 專案原始檔的獨立副本，產生器只讀這份 |
| `report.html` | **內部範本，不是給人打開的頁面**。共用的 parse/渲染邏輯 + CSS 都在這裡，`generate-static-report.py` 靠它產出繳交物，別刪 |
| `generate-static-report.py` | 靜態快照產生器：讀一次 CHANGELOG.md + report.html 範本，烘出作業繳交用的 `MMDD_daily_report_Eddie.html` |
| `regenerate.command` | 產生器雙擊啟動：跑 `generate-static-report.py` 並自動開啟結果 |
| `MMDD_daily_report_Eddie.html` | 實際繳交的作業本體（靜態快照，內容凍結於產生當下） |
| `prd.md` | 這個工具的完整規格文件（架構、機制、限制、決策紀錄） |

## Rules

- **改動前先讀 `prd.md`**：機制、路徑、port 等設定值都記在裡面，別憑印象改
- **改完同步更新 `prd.md`**：新需求、行為變動、取捨都要落地寫進去（尤其「變更紀錄」段），不留只在對話裡、日後會遺忘的決定
- **`report.html` 是產生器的範本，不要刪、不要當成頁面直接改著用**：要更新日報內容，改 `CHANGELOG.md`（本資料夾內的副本）再重跑產生器，不要去動 AI Gen Figma 專案的原始檔
- **語言**：繁體中文優先，程式碼識別字維持原文
- **done**：使用者說「done」＝直接 `git add` + commit + push（不需先確認 commit message），push 後回報 commit 內容
