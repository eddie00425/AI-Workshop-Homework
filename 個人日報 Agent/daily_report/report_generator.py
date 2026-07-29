import argparse
import html
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple


REDACTION_TEXT = "［已遮罩］"
REPORT_SECTIONS = ("completed", "blockers", "tomorrow", "analysis_additions")


class DailyReportError(RuntimeError):
    """Raised when the daily report payload cannot be rendered safely."""


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def _redact_text(text: str, terms: Sequence[str]) -> str:
    redacted = text
    for term in terms:
        term = _clean_text(term)
        if term and term != "待補":
            redacted = redacted.replace(term, REDACTION_TEXT)
    redacted = re.sub(r"https://hooks\.slack(?:-gov)?\.com/services/\S+", REDACTION_TEXT, redacted)
    redacted = re.sub(r"\b(xox[baprs]-[A-Za-z0-9-]+)\b", REDACTION_TEXT, redacted)
    return redacted


def _redact_payload(value: Any, terms: Sequence[str]) -> Any:
    if isinstance(value, str):
        return _redact_text(value, terms)
    if isinstance(value, list):
        return [_redact_payload(item, terms) for item in value]
    if isinstance(value, dict):
        return {key: _redact_payload(item, terms) for key, item in value.items()}
    return value


def _evidence_catalog(payload: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    catalog = {}
    for entry in payload.get("evidence", []):
        evidence_id = _clean_text(entry.get("id"))
        if evidence_id:
            catalog[evidence_id] = entry
    return catalog


def _iter_report_items(report: Dict[str, Any]) -> Iterable[Tuple[str, Dict[str, Any]]]:
    for group in report.get("completed", []):
        for item in group.get("items", []):
            yield "completed", item

    for section in ("blockers", "tomorrow"):
        for item in report.get(section, []):
            yield section, item

    for item in report.get("analysis_additions", []):
        yield "analysis_additions", item


def _is_no_major_issue(item: Dict[str, Any]) -> bool:
    return _clean_text(item.get("text")) == "無重大問題"


def validate_report_payload(payload: Dict[str, Any]) -> None:
    report = payload.get("report")
    if not isinstance(report, dict):
        raise DailyReportError("Missing report object.")

    if not _clean_text(report.get("date")):
        raise DailyReportError("Missing report.date.")
    if not _clean_text(report.get("summary")):
        raise DailyReportError("Missing report.summary.")

    for section in REPORT_SECTIONS:
        if not report.get(section):
            raise DailyReportError(f"Missing report.{section}.")

    for group in report.get("completed", []):
        if not _clean_text(group.get("workstream")):
            raise DailyReportError("Completed workstream cannot be empty.")
        if not group.get("items"):
            raise DailyReportError(f"Completed workstream has no items: {group.get('workstream')}")

    evidence = _evidence_catalog(payload)
    if not evidence:
        raise DailyReportError("Missing evidence entries.")

    for section, item in _iter_report_items(report):
        text = _clean_text(item.get("text"))
        if not text:
            raise DailyReportError(f"Empty item text in {section}.")

        evidence_ids = item.get("evidence_ids", [])
        if not evidence_ids and not (section == "blockers" and _is_no_major_issue(item)):
            raise DailyReportError(f"Missing evidence_ids for item: {text}")

        missing = [evidence_id for evidence_id in evidence_ids if evidence_id not in evidence]
        if missing:
            raise DailyReportError(f"Unknown evidence id for item '{text}': {', '.join(missing)}")


def _evidence_label(evidence_id: str, catalog: Dict[str, Dict[str, Any]]) -> str:
    entry = catalog[evidence_id]
    source_type = _clean_text(entry.get("source_type")) or "source"
    title = _clean_text(entry.get("title")) or evidence_id
    timestamp = _clean_text(entry.get("timestamp"))
    if timestamp:
        return f"{source_type}｜{timestamp}｜{title}"
    return f"{source_type}｜{title}"


def _markdown_evidence(evidence_ids: Sequence[str], catalog: Dict[str, Dict[str, Any]]) -> str:
    if not evidence_ids:
        return "證據：無明確卡點來源"
    labels = [f"`{evidence_id}` {_evidence_label(evidence_id, catalog)}" for evidence_id in evidence_ids]
    return "證據：" + "；".join(labels)


def render_markdown(payload: Dict[str, Any], redaction_terms: Sequence[str] = ()) -> str:
    payload = _redact_payload(payload, redaction_terms)
    validate_report_payload(payload)

    report = payload["report"]
    catalog = _evidence_catalog(payload)
    lines: List[str] = [
        f"# 每日進度報告｜{report['date']}",
        "",
        f"> {report['summary']}",
        "",
        "## 今天完成的事",
        "",
    ]

    for group in report["completed"]:
        lines.extend([f"### {group['workstream']}", ""])
        for item in group["items"]:
            lines.append(f"- {item['text']}")
            lines.append(f"  - {_markdown_evidence(item.get('evidence_ids', []), catalog)}")
        lines.append("")

    lines.extend(["## 遇到的問題與卡點", ""])
    for item in report["blockers"]:
        lines.append(f"- {item['text']}")
        lines.append(f"  - {_markdown_evidence(item.get('evidence_ids', []), catalog)}")
    lines.append("")

    lines.extend(["## 明天的計劃", ""])
    for item in report["tomorrow"]:
        lines.append(f"- {item['text']}")
        lines.append(f"  - {_markdown_evidence(item.get('evidence_ids', []), catalog)}")
    lines.append("")

    lines.extend(["## 可以新增的內容", ""])
    for item in report["analysis_additions"]:
        lines.append(f"- **{item['title']}**：{item['text']}")
        lines.append(f"  - {_markdown_evidence(item.get('evidence_ids', []), catalog)}")
    lines.append("")

    lines.extend(["## 來源索引", ""])
    for evidence_id, entry in sorted(catalog.items()):
        title = _clean_text(entry.get("title")) or evidence_id
        source_type = _clean_text(entry.get("source_type")) or "source"
        timestamp = _clean_text(entry.get("timestamp")) or "待補"
        url = _clean_text(entry.get("url"))
        line = f"- `{evidence_id}` {source_type}｜{timestamp}｜{title}"
        if url:
            line += f"｜{url}"
        lines.append(line)

    return "\n".join(lines).rstrip() + "\n"


def _evidence_chips(evidence_ids: Sequence[str], catalog: Dict[str, Dict[str, Any]]) -> str:
    if not evidence_ids:
        return '<span class="chip muted">無明確卡點來源</span>'

    chips = []
    for evidence_id in evidence_ids:
        label = html.escape(evidence_id)
        title = html.escape(_evidence_label(evidence_id, catalog))
        chips.append(f'<span class="chip" title="{title}">{label}</span>')
    return "".join(chips)


def _render_item(item: Dict[str, Any], catalog: Dict[str, Dict[str, Any]]) -> str:
    text = html.escape(item["text"])
    chips = _evidence_chips(item.get("evidence_ids", []), catalog)
    return f"""
      <li>
        <p>{text}</p>
        <div class="evidence">{chips}</div>
      </li>
    """


def render_html(payload: Dict[str, Any], redaction_terms: Sequence[str] = ()) -> str:
    payload = _redact_payload(payload, redaction_terms)
    validate_report_payload(payload)

    report = payload["report"]
    catalog = _evidence_catalog(payload)

    completed_html = []
    for group in report["completed"]:
        items = "\n".join(_render_item(item, catalog) for item in group["items"])
        completed_html.append(
            f"""
            <section class="workstream">
              <h3>{html.escape(group["workstream"])}</h3>
              <ul>{items}</ul>
            </section>
            """
        )

    blockers = "\n".join(_render_item(item, catalog) for item in report["blockers"])
    tomorrow = "\n".join(_render_item(item, catalog) for item in report["tomorrow"])
    additions = "\n".join(
        f"""
        <li>
          <p><strong>{html.escape(item["title"])}</strong>：{html.escape(item["text"])}</p>
          <div class="evidence">{_evidence_chips(item.get("evidence_ids", []), catalog)}</div>
        </li>
        """
        for item in report["analysis_additions"]
    )

    source_rows = []
    for evidence_id, entry in sorted(catalog.items()):
        url = _clean_text(entry.get("url"))
        title = html.escape(_clean_text(entry.get("title")) or evidence_id)
        if url:
            title_html = f'<a href="{html.escape(url)}">{title}</a>'
        else:
            title_html = title
        source_rows.append(
            f"""
            <tr>
              <td><code>{html.escape(evidence_id)}</code></td>
              <td>{html.escape(_clean_text(entry.get("source_type")) or "source")}</td>
              <td>{html.escape(_clean_text(entry.get("timestamp")) or "待補")}</td>
              <td>{title_html}</td>
            </tr>
            """
        )

    date = html.escape(report["date"])
    summary = html.escape(report["summary"])
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>每日進度報告｜{date}</title>
  <style>
    :root {{
      --paper: #f7f5ef;
      --surface: #fffdf7;
      --ink: #20241f;
      --muted: #626a60;
      --line: #d9d4c8;
      --complete: #2f6f4e;
      --issue: #9a5b1f;
      --plan: #315f8f;
      --evidence: #4e5661;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", "Microsoft JhengHei", sans-serif;
      line-height: 1.65;
    }}

    main {{
      width: min(980px, calc(100% - 32px));
      margin: 0 auto;
      padding: 40px 0 56px;
    }}

    header {{
      border-bottom: 2px solid var(--ink);
      padding-bottom: 18px;
      margin-bottom: 28px;
    }}

    .date {{
      margin: 0 0 8px;
      color: var(--muted);
      font-size: 15px;
      font-weight: 700;
    }}

    h1 {{
      margin: 0;
      font-size: clamp(34px, 6vw, 58px);
      line-height: 1.05;
      letter-spacing: 0;
    }}

    .summary {{
      max-width: 74ch;
      margin: 18px 0 0;
      font-size: 18px;
      font-weight: 650;
    }}

    .section {{
      display: grid;
      grid-template-columns: 180px minmax(0, 1fr);
      gap: 28px;
      border-top: 1px solid var(--line);
      padding: 26px 0;
    }}

    .section h2 {{
      margin: 0;
      font-size: 18px;
      line-height: 1.25;
    }}

    .section.completed h2 {{ color: var(--complete); }}
    .section.blockers h2 {{ color: var(--issue); }}
    .section.tomorrow h2 {{ color: var(--plan); }}

    .workstream {{
      padding: 0 0 18px;
      margin: 0 0 18px;
      border-bottom: 1px dashed var(--line);
    }}

    .workstream:last-child {{
      margin-bottom: 0;
      border-bottom: 0;
    }}

    h3 {{
      margin: 0 0 10px;
      font-size: 17px;
    }}

    ul {{
      list-style: none;
      margin: 0;
      padding: 0;
    }}

    li {{
      background: var(--surface);
      border-radius: 8px;
      box-shadow: 0 5px 18px rgba(32, 36, 31, 0.08);
      margin: 0 0 10px;
      padding: 13px 14px 12px;
    }}

    li p {{
      margin: 0;
      max-width: 75ch;
    }}

    .evidence {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }}

    .chip {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      border-radius: 6px;
      background: #eef0eb;
      color: var(--evidence);
      padding: 2px 7px;
      font-size: 12px;
      font-weight: 700;
      overflow-wrap: anywhere;
    }}

    .chip.muted {{
      font-weight: 600;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--surface);
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 5px 18px rgba(32, 36, 31, 0.08);
    }}

    th, td {{
      border-bottom: 1px solid var(--line);
      padding: 10px;
      text-align: left;
      vertical-align: top;
      font-size: 14px;
    }}

    th {{
      color: var(--muted);
      font-weight: 750;
    }}

    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12px;
    }}

    a {{
      color: var(--plan);
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }}

    @media (max-width: 760px) {{
      main {{
        width: min(100% - 24px, 680px);
        padding-top: 28px;
      }}

      .section {{
        grid-template-columns: 1fr;
        gap: 12px;
      }}

      h1 {{
        font-size: 36px;
      }}

      table {{
        display: block;
        overflow-x: auto;
      }}
    }}

    @media print {{
      body {{ background: white; }}
      main {{ width: 100%; padding: 0; }}
      li, table {{ box-shadow: none; border: 1px solid var(--line); }}
      a {{ color: inherit; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <p class="date">{date}</p>
      <h1>每日進度報告</h1>
      <p class="summary">{summary}</p>
    </header>

    <section class="section completed">
      <h2>今天完成的事</h2>
      <div>
        {''.join(completed_html)}
      </div>
    </section>

    <section class="section blockers">
      <h2>遇到的問題與卡點</h2>
      <ul>{blockers}</ul>
    </section>

    <section class="section tomorrow">
      <h2>明天的計劃</h2>
      <ul>{tomorrow}</ul>
    </section>

    <section class="section">
      <h2>可以新增的內容</h2>
      <ul>{additions}</ul>
    </section>

    <section class="section">
      <h2>來源索引</h2>
      <table>
        <thead>
          <tr>
            <th>Evidence ID</th>
            <th>來源</th>
            <th>時間</th>
            <th>標題</th>
          </tr>
        </thead>
        <tbody>{''.join(source_rows)}</tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


def render_outputs(payload: Dict[str, Any], redaction_terms: Sequence[str] = ()) -> Tuple[str, str]:
    return render_markdown(payload, redaction_terms), render_html(payload, redaction_terms)


def write_outputs(
    payload: Dict[str, Any],
    output_dir: str,
    redaction_terms: Sequence[str] = (),
) -> Tuple[Path, Path]:
    markdown, html_text = render_outputs(payload, redaction_terms)
    date = payload["report"]["date"]
    target_dir = Path(output_dir) / date[:4] / date[5:7]
    target_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = target_dir / f"{date}.md"
    html_path = target_dir / f"{date}.html"
    markdown_path.write_text(markdown, encoding="utf-8")
    html_path.write_text(html_text, encoding="utf-8")
    return markdown_path, html_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Render daily report Markdown and HTML.")
    parser.add_argument("input", help="Daily report payload JSON.")
    parser.add_argument("--config", help="Optional config JSON with redaction terms and output path.")
    parser.add_argument("--output-dir", default="daily_report/reports", help="Directory for generated reports.")
    args = parser.parse_args()

    payload = load_json(args.input)
    redaction_terms: List[str] = []
    output_dir = args.output_dir

    if args.config:
        config = load_json(args.config)
        redaction_terms = config.get("redaction", {}).get("terms", [])
        output_dir = config.get("output", {}).get("reports_dir", output_dir)

    try:
        markdown_path, html_path = write_outputs(payload, output_dir, redaction_terms)
    except DailyReportError as error:
        parser.exit(1, f"Error: {error}\n")

    print(f"Markdown: {markdown_path}")
    print(f"HTML: {html_path}")


if __name__ == "__main__":
    main()

