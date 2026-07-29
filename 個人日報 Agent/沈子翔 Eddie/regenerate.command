#!/bin/bash
# 雙擊本檔案：重新讀一次 CHANGELOG.md，烘出新的靜態快照 html，並自動開啟

cd "$(dirname "$0")" || exit 1

OUTPUT_LOG=$(python3 generate-static-report.py)
echo "$OUTPUT_LOG"

OUTPUT_PATH=$(echo "$OUTPUT_LOG" | sed -n 's/^已產生靜態快照：//p')

if [ -n "$OUTPUT_PATH" ]; then
  open "$OUTPUT_PATH"
fi

echo ""
echo "完成，按任意鍵關閉視窗…"
read -n 1 -s -r
