# 每日進度報告 Agent 規格

## 目標

每日下班前把 Slack、Notion 工作看板與 AI 對話紀錄整理成一份可追溯、可回查、繁體中文的每日進度報告。

## 執行流程

1. 收集當天資料
   - Slack：抓取指定頻道與本人發出的訊息。
   - Notion MCP：讀取工作看板頁面與卡片狀態。
   - AI sessions：讀取 Claude Code、Codex 等對話紀錄摘要或逐字內容。
   - Slack 權限尚未核准時：先用 `manual_inputs/*.jsonl` 手動貼入工作相關訊息。
2. 正規化成 evidence bundle
   - 每筆來源都要有唯一 `id`。
   - 每筆來源保留 `source_type`、`timestamp`、`title`、`text`、`url`。
   - 閒聊、八卦、生活雜事標成 `work_related: false`，不得進入報告主體。
3. Agent 分析
   - 只使用 `work_related: true` 的 evidence。
   - 將完成事項、問題卡點、明日計畫、可新增內容整理成 report JSON。
   - 每一個完成事項、卡點與計畫都必須附上 `evidence_ids`。
4. 驗證與輸出
   - 使用 `report_generator.py` 驗證 evidence id 是否存在。
   - 用設定檔中的敏感詞進行遮罩。
   - 同時輸出 Markdown 與 HTML。
5. 保存與發布
   - Markdown 存到 `daily_report/reports/YYYY/MM/YYYY-MM-DD.md`。
   - HTML 存到 `daily_report/reports/YYYY/MM/YYYY-MM-DD.html`。
   - 如需發 Slack，將 Markdown 交給 `slack_connector.py`。

## 資料來源策略

### Slack

- 需要補齊設定：頻道名稱、本人 Slack user id。
- 真實 workspace、頻道名稱、channel id 與本人 user id 只放在 ignored 的 `config.local.json`。
- 抓取範圍：每日 00:00 到執行時間，時區 `Asia/Taipei`。
- 過濾規則：
  - 保留：任務進度、決策、交付、問題、需求變更、協作承諾。
  - 排除：閒聊、八卦、生活雜事、純表情、沒有工作意義的回覆。
- 未授權期間：使用 `MANUAL_INPUTS.md` 的 JSONL 格式先建立 evidence。

### Notion MCP

- 工作看板頁面 URL 只放在 ignored 的 `config.local.json`。
- 主要判斷：
  - 移到完成：列入「今天完成的事」。
  - 未開始移到進行中：列入「明天的計劃」或「今日啟動」。
  - 仍在進行中：列入「明天的計劃」。
  - 狀態不明：標「待補」。

### AI 對話紀錄

- 需要補齊設定：Claude Code 與 Codex session log 的實際路徑或匯出方式。
- 只摘要與工作產出相關的對話。
- 若 session 中有程式碼、規格、決策或錯誤修復，應作為 evidence。

## 輸出規則

- 一律繁體中文、台灣用語。
- 完成事項每條只寫一句話。
- 不美化、不誇大、不新增來源不存在的工作。
- 看不懂或缺資料就寫「待補」。
- 「遇到的問題與卡點」不可省略；若沒有明確卡點，寫「無重大問題」。
- 客戶名稱、內部專案代號與設定檔中的敏感詞一律遮罩成 `［已遮罩］`。

## 驗收標準

- Markdown 與 HTML 都存在。
- 每段都有內容。
- 每個主要項目都能追到 evidence id。
- 報告沒有未出現在輸入中的工作。
- HTML 樣式每次一致，且不依賴 JavaScript。
