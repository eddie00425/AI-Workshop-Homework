#!/bin/bash
# 雙擊本檔案：啟動本機伺服器(若尚未啟動)並開啟工作日報頁面

PORT=8934
ROOT="$HOME/Documents"
REL_PATH="AI-Workshop-Homework/個人日報 Agent/沈子翔 Eddie/report.html"

if ! lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  ( cd "$ROOT" && nohup python3 -m http.server "$PORT" >/tmp/daily-report-server.log 2>&1 & )
  sleep 1
fi

python3 - "$REL_PATH" "$PORT" <<'PYEOF'
import sys
import urllib.parse
import webbrowser

rel, port = sys.argv[1], sys.argv[2]
encoded = '/'.join(urllib.parse.quote(part) for part in rel.split('/'))
webbrowser.open(f"http://localhost:{port}/{encoded}")
PYEOF
