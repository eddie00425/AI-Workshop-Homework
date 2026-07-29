import json
import os
import unittest
from unittest.mock import MagicMock, patch

from daily_report.slack_collector import (
    DEFAULT_TOKEN_ENV,
    SlackCollectorError,
    collect_slack_evidence,
    fetch_channel_messages,
    is_likely_work_related,
    slack_api_get,
)


class SlackCollectorTests(unittest.TestCase):
    def test_is_likely_work_related_filters_casual_text(self):
        self.assertFalse(is_likely_work_related("午餐吃什麼"))
        self.assertTrue(is_likely_work_related("完成 daily report collector 測試"))

    def test_slack_api_get_requires_token(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SlackCollectorError):
                slack_api_get("auth.test", {})

    def test_fetch_channel_messages_calls_conversations_history(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {
                "ok": True,
                "messages": [{"ts": "1785319200.000000", "text": "完成測試", "user": "U_TEST_USER"}],
                "response_metadata": {"next_cursor": ""},
            }
        ).encode("utf-8")

        with patch.dict(os.environ, {DEFAULT_TOKEN_ENV: "xoxb-"}):
            with patch("daily_report.slack_collector.urlopen", return_value=response) as urlopen:
                messages = fetch_channel_messages("C_TEST_CHANNEL", "2026-07-29", "Asia/Taipei")

        self.assertEqual(messages[0]["text"], "完成測試")
        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertIn("conversations.history", request.full_url)
        self.assertIn("channel=C_TEST_CHANNEL", request.full_url)

    def test_collect_slack_evidence_marks_self_messages(self):
        config = {
            "timezone": "Asia/Taipei",
            "slack": {
                "self_user_id": "U_TEST_USER",
                "channels": [{"name": "測試頻道", "id": "C_TEST_CHANNEL", "type": "private"}],
            },
        }

        with patch(
            "daily_report.slack_collector.fetch_channel_messages",
            return_value=[{"ts": "1785319200.000000", "text": "完成 Slack collector", "user": "U_TEST_USER"}],
        ):
            evidence = collect_slack_evidence(config, "2026-07-29", token="xoxb-")

        self.assertEqual(evidence[0]["id"], "slack:C_TEST_CHANNEL:1785319200.000000")
        self.assertTrue(evidence[0]["work_related"])
        self.assertTrue(evidence[0]["metadata"]["from_self"])


if __name__ == "__main__":
    unittest.main()
