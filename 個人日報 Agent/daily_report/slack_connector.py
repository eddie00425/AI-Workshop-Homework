import argparse
import json
import os
import sys
from typing import Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_WEBHOOK_ENV = "SLACK_WEBHOOK_URL"
DEFAULT_TITLE = "Daily Report"


class SlackConnectorError(RuntimeError):
    """Raised when a daily report cannot be posted to Slack."""


def build_slack_payload(report_text: str, title: str = DEFAULT_TITLE) -> Dict[str, str]:
    report_text = (report_text or "").strip()
    title = (title or DEFAULT_TITLE).strip()

    if not report_text:
        raise ValueError("report_text is required")

    return {"text": f"*{title}*\n{report_text}"}


def _resolve_webhook_url(webhook_url: Optional[str]) -> str:
    url = (webhook_url or os.getenv(DEFAULT_WEBHOOK_ENV) or "").strip()
    if not url:
        raise SlackConnectorError(f"Missing Slack webhook URL. Set {DEFAULT_WEBHOOK_ENV}.")

    allowed_prefixes = (
        "https://hooks.slack.com/services/",
        "https://hooks.slack-gov.com/services/",
    )
    if not url.startswith(allowed_prefixes):
        raise SlackConnectorError("Slack webhook URL must be a Slack incoming webhook URL.")

    return url


def send_daily_report_to_slack(
    report_text: str,
    webhook_url: Optional[str] = None,
    title: str = DEFAULT_TITLE,
    timeout: float = 10,
) -> str:
    url = _resolve_webhook_url(webhook_url)
    payload = build_slack_payload(report_text, title)
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8").strip()
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace").strip()
        raise SlackConnectorError(f"Slack returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise SlackConnectorError(f"Could not connect to Slack: {error.reason}") from error

    if body != "ok":
        raise SlackConnectorError(f"Unexpected Slack response: {body}")

    return body


def _read_report(path: str) -> str:
    if path == "-":
        return sys.stdin.read()

    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a daily report to Slack.")
    parser.add_argument("input", nargs="?", default="-", help="Daily report file path, or - for stdin.")
    parser.add_argument("--title", default=DEFAULT_TITLE, help="Slack message title.")
    parser.add_argument("--webhook-url", help=f"Slack webhook URL. Defaults to {DEFAULT_WEBHOOK_ENV}.")
    parser.add_argument("--dry-run", action="store_true", help="Print the Slack payload without sending it.")
    args = parser.parse_args()

    try:
        report_text = _read_report(args.input)
        payload = build_slack_payload(report_text, args.title)

        if args.dry_run:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return

        send_daily_report_to_slack(report_text, args.webhook_url, args.title)
        print("Daily report sent to Slack.")
    except (SlackConnectorError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
