#!/usr/bin/env python3
"""
把 CHANGELOG.md 目前的內容烘進一份靜態單一 html（作業繳交用快照）。

跟 report.html（即時同步版）差別：這份輸出不 fetch、不輪詢，內容是產生當下
寫死進去的文字。CHANGELOG.md 之後再改，這份輸出不會跟著動——要更新快照，
重新跑一次這支腳本即可。

用法：
    python3 generate-static-report.py
"""

import json
import re
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHANGELOG_PATH = HERE / "CHANGELOG.md"  # 本資料夾內的複本，與 Gen Figma AI 專案原始檔分開
TEMPLATE_PATH = HERE / "report.html"

BOOTSTRAP_START = "/* BOOTSTRAP:LIVE:START"
BOOTSTRAP_END = "/* BOOTSTRAP:LIVE:END */"


def build_static_bootstrap(changelog_text: str, snapshot_time: str) -> str:
    # 安全內嵌：JSON 逃脫特殊字元，另外擋掉 "</script"，避免提早關閉 <script> 標籤
    data_literal = json.dumps(changelog_text)
    data_literal = re.sub(r"</(script)", r"<\\/\1", data_literal, flags=re.IGNORECASE)

    return f"""/* BOOTSTRAP:STATIC — 由 generate-static-report.py 產生，勿手改，改請重跑腳本 */
(function(){{
  const {{ applyDays }} = window.__report;
  const SNAPSHOT_TEXT = {data_literal};
  const SNAPSHOT_TIME = {json.dumps(snapshot_time)};

  const els = {{
    main: document.getElementById('reportMain'),
    nav: document.getElementById('monthNav'),
    range: document.getElementById('rangeText'),
    count: document.getElementById('dayCount')
  }};
  document.getElementById('sourceNote').innerHTML =
    `此頁為靜態快照，擷取於 <span class="mono">${{SNAPSHOT_TIME}}</span>`;
  document.getElementById('syncStatus').textContent = '● 靜態快照（離線可讀）';

  applyDays(SNAPSHOT_TEXT, els, false);
}})();
/* BOOTSTRAP:STATIC:END */"""


def main():
    changelog_text = CHANGELOG_PATH.read_text(encoding="utf-8")
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")

    start_idx = template_text.index(BOOTSTRAP_START)
    end_idx = template_text.index(BOOTSTRAP_END) + len(BOOTSTRAP_END)

    now = datetime.now()
    snapshot_time = now.strftime("%Y-%m-%d %H:%M:%S")
    static_block = build_static_bootstrap(changelog_text, snapshot_time)

    output_html = template_text[:start_idx] + static_block + template_text[end_idx:]
    # 靜態版 title 加註記，跟即時版分清楚
    output_html = output_html.replace(
        "<title>工作日報 · AI Gen Figma</title>",
        "<title>工作日報（靜態快照）· AI Gen Figma</title>",
        1,
    )

    output_name = f"{now:%m%d}_daily_report_Eddie.html"
    output_path = HERE / output_name
    output_path.write_text(output_html, encoding="utf-8")

    print(f"已產生靜態快照：{output_path}")
    print(f"擷取時間：{snapshot_time}")


if __name__ == "__main__":
    main()
