# Daily Report Agent

這個資料夾包含每日進度報告 Agent 的規格、提示詞、輸出產生器與 Slack 發送 connector。

## 核心檔案

- `AGENT_SPEC.md`：完整執行規格與資料來源策略。
- `agent_prompt.md`：給 LLM agent 使用的報告整理提示詞。
- `config.example.json`：Slack、Notion、AI session 與敏感詞設定範例。
- `config.local.json`：目前本機的 Slack/Notion 設定，不含 token，且不進 Git。
- `MANUAL_INPUTS.md`：Slack 權限未核准前的手動匯入流程。
- `evidence_schema.json`：輸入 evidence bundle 與 report JSON 的資料契約。
- `build_payload.py`：把手動 JSONL evidence 組成 payload skeleton。
- `slack_collector.py`：把 Slack 訊息收集成 evidence。
- `report_generator.py`：把 report JSON 轉成 Markdown 與 HTML。
- `slack_connector.py`：把 Markdown 報告送到 Slack。

## 建議每日流程

1. 從 Slack、Notion MCP、AI session 收集資料。
2. 將資料整理成 evidence bundle。
3. 交給 `agent_prompt.md` 產生 `report` JSON。
4. 用 `report_generator.py` 輸出 Markdown 與 HTML。
5. 視需要用 `slack_connector.py` 發到 Slack。

## 產生報告

使用範例 payload：

```bash
python3 -m daily_report.report_generator daily_report/sample_payload.json
```

輸出位置預設為：

```text
daily_report/reports/YYYY/MM/YYYY-MM-DD.md
daily_report/reports/YYYY/MM/YYYY-MM-DD.html
```

使用設定檔中的敏感詞與輸出路徑：

```bash
python3 -m daily_report.report_generator daily_report/sample_payload.json --config daily_report/config.example.json
```

## 收集 Slack Evidence

先把 Slack token 放進環境變數，不要寫進檔案：

```bash
export SLACK_BOT_TOKEN="xoxb-..."
```

收集指定日期 Slack 訊息：

```bash
python3 -m daily_report.slack_collector 2026-07-29 --config daily_report/config.local.json
```

真實 Slack workspace、channel id 與本人 user id 只放在 ignored 的 `config.local.json`，不要寫進 README 或 commit。

```text
workspace_url: https://your-workspace.slack.com
channel_name: 待補
channel_ids: 待補
self_user_id: 待補
```

## Slack 權限未核准時

先把可用資料放進 JSONL：

```bash
daily_report/manual_inputs/2026-07-29.jsonl
```

建立 payload skeleton：

```bash
python3 -m daily_report.build_payload 2026-07-29 daily_report/manual_inputs/2026-07-29.jsonl
```

產生暫存報告：

```bash
python3 -m daily_report.report_generator daily_report/payloads/2026/07/2026-07-29.payload.json
```

## Slack 設定

1. 在 Slack app 裡啟用 Incoming Webhooks。
2. 新增 webhook 並選擇要發送的 channel。
3. 把 webhook URL 設成環境變數：

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

## 使用方式

從檔案送出：

```bash
python3 -m daily_report.slack_connector ./daily-report.md
```

從 stdin 送出：

```bash
cat ./daily-report.md | python3 -m daily_report.slack_connector
```

先檢查 payload，不送到 Slack：

```bash
python3 -m daily_report.slack_connector ./daily-report.md --dry-run
```
