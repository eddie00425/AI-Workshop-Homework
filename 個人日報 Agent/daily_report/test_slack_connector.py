import json
import os
import unittest
from unittest.mock import MagicMock, patch

from daily_report.slack_connector import (
    DEFAULT_WEBHOOK_ENV,
    SlackConnectorError,
    build_slack_payload,
    send_daily_report_to_slack,
)


class SlackConnectorTests(unittest.TestCase):
    def test_build_slack_payload_formats_report(self):
        payload = build_slack_payload("今天完成重點整理。", "Daily Report")

        self.assertEqual(payload, {"text": "*Daily Report*\n今天完成重點整理。"})

    def test_build_slack_payload_requires_report_text(self):
        with self.assertRaises(ValueError):
            build_slack_payload("  ")

    def test_send_daily_report_uses_env_webhook(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"ok"

        with patch.dict(os.environ, {DEFAULT_WEBHOOK_ENV: "https://hooks.slack.com/services/T/B/X"}):
            with patch("daily_report.slack_connector.urlopen", return_value=response) as urlopen:
                result = send_daily_report_to_slack("今日進度完成。")

        self.assertEqual(result, "ok")
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://hooks.slack.com/services/T/B/X")
        self.assertEqual(request.get_method(), "POST")
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["text"], "*Daily Report*\n今日進度完成。")

    def test_send_daily_report_rejects_missing_webhook(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SlackConnectorError):
                send_daily_report_to_slack("今日進度完成。")

    def test_send_daily_report_rejects_non_slack_webhook(self):
        with self.assertRaises(SlackConnectorError):
            send_daily_report_to_slack("今日進度完成。", "https://example.com/webhook")


if __name__ == "__main__":
    unittest.main()

