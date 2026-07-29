# Slack 權限未核准前可以先做什麼

在還沒拿到 Slack bot token 前，可以先用手動 evidence 流程把資料整理起來。這會讓日報格式、敏感詞遮罩、HTML/Markdown 輸出先跑起來，等 Slack 權限下來後只要把資料來源換成 `slack_collector.py`。

## 你現在可以準備

1. Slack app 權限
   - 確認已申請安裝 Slack app 到目標 workspace。
   - 確認 scopes 包含 `channels:read`、`channels:history`、`groups:read`、`groups:history`、`users:read`。
   - 若要發報告到 Slack，保留 `chat:write`。
   - 權限核准後，把 app 邀請進 private channel：`/invite @Shiloh`。
2. 手動匯入 Slack
   - 每天下班前複製目標 Slack 頻道內和工作有關的訊息。
   - 閒聊、生活雜事可以不貼；若貼了請標 `work_related: false`。
3. 手動匯入 Notion
   - 記錄今天移到完成、進行中、剛啟動、卡住的卡片。
4. 手動匯入 AI sessions
   - 摘要今天 Claude Code / Codex session 裡完成的規格、程式碼、決策、錯誤修復與待辦。

## JSONL 格式

每一行是一筆 evidence：

```json
{"source_type":"slack","timestamp":"2026-07-29T17:45:00+08:00","title":"#目標頻道","text":"完成 daily report agent 的 Slack collector 測試。","work_related":true}
```

必填欄位：

- `source_type`：`slack`、`notion`、`codex`、`claude_code`、`manual`
- `timestamp`：ISO 時間字串，不確定就填日期加時間或 `待補`
- `title`：來源標題，例如 Slack 頻道名稱、Notion 卡片名稱、AI session 名稱
- `text`：原始內容或摘要
- `work_related`：工作內容填 `true`，閒聊填 `false`

選填欄位：

- `id`：不填會自動產生
- `url`：來源連結
- `metadata`：其他備註

## 建立 payload skeleton

```bash
python3 -m daily_report.build_payload 2026-07-29 daily_report/manual_inputs/2026-07-29.jsonl
```

這會輸出：

```text
daily_report/payloads/2026/07/2026-07-29.payload.json
```

這份 payload 會先用「待補」建立每段內容。之後可以把 `evidence` 交給 `agent_prompt.md`，讓 LLM 產生正式 `report` JSON，再用 `report_generator.py` 產出正式報告。
