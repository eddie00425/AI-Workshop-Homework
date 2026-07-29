import tempfile
import unittest
from pathlib import Path

from daily_report.report_generator import (
    DailyReportError,
    render_html,
    render_markdown,
    validate_report_payload,
    write_outputs,
)


def sample_payload():
    return {
        "date": "2026-07-29",
        "timezone": "Asia/Taipei",
        "evidence": [
            {
                "id": "notion:card:agent",
                "source_type": "notion",
                "timestamp": "2026-07-29T18:00:00+08:00",
                "title": "每日進度報告 Agent",
                "text": "卡片已移到完成。",
                "url": "https://www.notion.so/example",
                "work_related": True,
            },
            {
                "id": "slack:plan",
                "source_type": "slack",
                "timestamp": "2026-07-29T18:10:00+08:00",
                "title": "#daily-report",
                "text": "明天補 Slack 設定。",
                "url": "",
                "work_related": True,
            },
        ],
        "report": {
            "date": "2026-07-29",
            "summary": "今天完成 daily report agent 骨架。",
            "completed": [
                {
                    "workstream": "Daily Report Agent",
                    "items": [
                        {
                            "text": "完成 daily report agent 骨架，並建立固定輸出格式。",
                            "evidence_ids": ["notion:card:agent"],
                        }
                    ],
                }
            ],
            "blockers": [
                {
                    "text": "無重大問題",
                    "evidence_ids": [],
                }
            ],
            "tomorrow": [
                {
                    "text": "補齊 Slack channel 設定後開始收集訊息。",
                    "evidence_ids": ["slack:plan"],
                }
            ],
            "analysis_additions": [
                {
                    "title": "來源信心等級",
                    "text": "建議增加來源信心等級，方便回溯判斷。",
                    "evidence_ids": ["notion:card:agent"],
                }
            ],
        },
    }


class DailyReportGeneratorTests(unittest.TestCase):
    def test_validate_accepts_complete_payload(self):
        validate_report_payload(sample_payload())

    def test_validate_rejects_unknown_evidence_id(self):
        payload = sample_payload()
        payload["report"]["completed"][0]["items"][0]["evidence_ids"] = ["missing"]

        with self.assertRaises(DailyReportError):
            validate_report_payload(payload)

    def test_render_markdown_contains_required_sections(self):
        markdown = render_markdown(sample_payload())

        self.assertIn("# 每日進度報告｜2026-07-29", markdown)
        self.assertIn("## 今天完成的事", markdown)
        self.assertIn("## 遇到的問題與卡點", markdown)
        self.assertIn("## 明天的計劃", markdown)
        self.assertIn("## 可以新增的內容", markdown)
        self.assertIn("## 來源索引", markdown)

    def test_render_redacts_sensitive_terms(self):
        payload = sample_payload()
        payload["report"]["summary"] = "今天完成 ACME 專案整理。"

        markdown = render_markdown(payload, ["ACME"])
        html = render_html(payload, ["ACME"])

        self.assertIn("［已遮罩］", markdown)
        self.assertIn("［已遮罩］", html)
        self.assertNotIn("ACME", markdown)
        self.assertNotIn("ACME", html)

    def test_write_outputs_creates_markdown_and_html(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            markdown_path, html_path = write_outputs(sample_payload(), temp_dir)

            self.assertEqual(markdown_path, Path(temp_dir) / "2026" / "07" / "2026-07-29.md")
            self.assertEqual(html_path, Path(temp_dir) / "2026" / "07" / "2026-07-29.html")
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())


if __name__ == "__main__":
    unittest.main()

