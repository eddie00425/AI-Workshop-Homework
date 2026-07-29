import argparse
import json
import os
import re
from datetime import datetime, time
from typing import Any, Dict, Iterable, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


DEFAULT_TOKEN_ENV = "SLACK_BOT_TOKEN"
SLACK_API_BASE = "https://slack.com/api"


class SlackCollectorError(RuntimeError):
    """Raised when Slack evidence cannot be collected."""


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def _token(token: Optional[str] = None) -> str:
    resolved = _clean_text(token or os.getenv(DEFAULT_TOKEN_ENV))
    if not resolved:
        raise SlackCollectorError(f"Missing Slack bot token. Set {DEFAULT_TOKEN_ENV}.")
    if not resolved.startswith(("xoxb-", "xoxp-")):
        raise SlackCollectorError("Slack token should look like xoxb-... or xoxp-....")
    return resolved


def slack_api_get(method: str, params: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
    query = urlencode({key: value for key, value in params.items() if value is not None})
    request = Request(
        f"{SLACK_API_BASE}/{method}?{query}",
        headers={"Authorization": f"Bearer {_token(token)}"},
        method="GET",
    )

    try:
        with urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SlackCollectorError(f"Slack returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise SlackCollectorError(f"Could not connect to Slack: {error.reason}") from error

    if not data.get("ok"):
        raise SlackCollectorError(f"Slack API error from {method}: {data.get('error', 'unknown_error')}")

    return data


def _date_bounds(date: str, timezone_name: str) -> tuple[float, float]:
    tz = ZoneInfo(timezone_name)
    start = datetime.combine(datetime.fromisoformat(date).date(), time.min, tzinfo=tz)
    end = datetime.combine(datetime.fromisoformat(date).date(), time.max, tzinfo=tz)
    return start.timestamp(), end.timestamp()


def _message_timestamp(ts: str, timezone_name: str) -> str:
    tz = ZoneInfo(timezone_name)
    seconds = float(ts)
    return datetime.fromtimestamp(seconds, tz=tz).isoformat(timespec="seconds")


def _strip_slack_markup(text: str) -> str:
    text = re.sub(r"<@([A-Z0-9]+)>", r"@\1", text)
    text = re.sub(r"<#([A-Z0-9]+)\|([^>]+)>", r"#\2", text)
    text = re.sub(r"<([^|>]+)\|([^>]+)>", r"\2", text)
    text = re.sub(r"<([^>]+)>", r"\1", text)
    return text.strip()


def is_likely_work_related(text: str, user_id: str = "") -> bool:
    text = _strip_slack_markup(text)
    if not text:
        return False
    if re.fullmatch(r"[:+\-\s\w]+", text) and len(text) <= 20 and ":" in text:
        return False

    casual_patterns = (
        "午餐",
        "晚餐",
        "早餐",
        "吃飯",
        "飲料",
        "咖啡",
        "八卦",
        "閒聊",
        "週末",
        "下班",
        "哈哈",
        "笑死",
    )
    if any(pattern in text for pattern in casual_patterns):
        work_terms = ("完成", "問題", "卡", "修", "開發", "測試", "部署", "PR", "需求", "規格", "上線")
        return any(term in text for term in work_terms)

    work_patterns = (
        "完成",
        "處理",
        "修正",
        "修掉",
        "新增",
        "建立",
        "調整",
        "測試",
        "部署",
        "上線",
        "規格",
        "需求",
        "卡住",
        "問題",
        "錯誤",
        "bug",
        "PR",
        "review",
        "merge",
        "release",
        "待補",
        "明天",
        "今天",
        user_id,
    )
    return any(pattern in text for pattern in work_patterns)


def _channel_config(config: Dict[str, Any]) -> Iterable[Dict[str, str]]:
    for channel in config.get("slack", {}).get("channels", []):
        if isinstance(channel, str):
            yield {"id": channel, "name": channel}
        elif isinstance(channel, dict):
            yield {
                "id": _clean_text(channel.get("id")),
                "name": _clean_text(channel.get("name")) or _clean_text(channel.get("id")),
                "type": _clean_text(channel.get("type")),
            }


def fetch_channel_messages(
    channel_id: str,
    date: str,
    timezone_name: str,
    token: Optional[str] = None,
    limit: int = 15,
    max_pages: int = 1,
) -> List[Dict[str, Any]]:
    oldest, latest = _date_bounds(date, timezone_name)
    messages: List[Dict[str, Any]] = []
    cursor = None

    for _ in range(max_pages):
        response = slack_api_get(
            "conversations.history",
            {
                "channel": channel_id,
                "oldest": oldest,
                "latest": latest,
                "inclusive": "true",
                "limit": limit,
                "cursor": cursor,
            },
            token=token,
        )
        messages.extend(response.get("messages", []))
        cursor = response.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    return messages


def collect_slack_evidence(
    config: Dict[str, Any],
    date: str,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    timezone_name = config.get("timezone", "Asia/Taipei")
    slack_config = config.get("slack", {})
    self_user_id = _clean_text(slack_config.get("self_user_id"))
    limit = int(slack_config.get("history_limit", 15))
    max_pages = int(slack_config.get("max_pages_per_channel", 1))
    evidence = []

    for channel in _channel_config(config):
        channel_id = channel["id"]
        if not channel_id:
            continue

        messages = fetch_channel_messages(
            channel_id,
            date,
            timezone_name,
            token=token,
            limit=limit,
            max_pages=max_pages,
        )

        for message in messages:
            text = _strip_slack_markup(message.get("text", ""))
            user = _clean_text(message.get("user") or message.get("bot_id"))
            work_related = is_likely_work_related(text, self_user_id)
            evidence.append(
                {
                    "id": f"slack:{channel_id}:{message.get('ts')}",
                    "source_type": "slack",
                    "timestamp": _message_timestamp(message.get("ts", "0"), timezone_name),
                    "title": f"#{channel.get('name', channel_id)}",
                    "text": text,
                    "url": "",
                    "work_related": work_related,
                    "metadata": {
                        "channel_id": channel_id,
                        "channel_type": channel.get("type", ""),
                        "user": user,
                        "from_self": user == self_user_id,
                    },
                }
            )

    return evidence


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect Slack messages as daily report evidence.")
    parser.add_argument("date", help="Report date in YYYY-MM-DD.")
    parser.add_argument("--config", default="daily_report/config.local.json", help="Daily report config JSON.")
    parser.add_argument("--token", help=f"Slack token. Defaults to {DEFAULT_TOKEN_ENV}.")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        evidence = collect_slack_evidence(config, args.date, args.token)
    except SlackCollectorError as error:
        parser.exit(1, f"Error: {error}\n")

    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

