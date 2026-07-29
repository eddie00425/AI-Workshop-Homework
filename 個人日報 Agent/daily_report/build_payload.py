import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_TIMEZONE = "Asia/Taipei"


class PayloadBuildError(RuntimeError):
    """Raised when manual evidence cannot be converted into a payload."""


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def _stable_id(entry: Dict[str, Any], line_number: int) -> str:
    source_type = _clean_text(entry.get("source_type")) or "manual"
    source = "|".join(
        [
            source_type,
            _clean_text(entry.get("timestamp")),
            _clean_text(entry.get("title")),
            _clean_text(entry.get("text")),
            str(line_number),
        ]
    )
    digest = hashlib.sha1(source.encode("utf-8")).hexdigest()[:10]
    return f"{source_type}:manual:{digest}"


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    entries = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as error:
                raise PayloadBuildError(f"Invalid JSONL at line {line_number}: {error}") from error
            if not isinstance(entry, dict):
                raise PayloadBuildError(f"JSONL line {line_number} must be an object.")
            entry.setdefault("id", _stable_id(entry, line_number))
            entry.setdefault("url", "")
            entry.setdefault("work_related", True)
            entries.append(entry)
    return entries


def merge_evidence(*groups: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged = []
    seen = set()
    for group in groups:
        for entry in group:
            evidence_id = _clean_text(entry.get("id"))
            if not evidence_id:
                raise PayloadBuildError("Evidence id cannot be empty.")
            if evidence_id in seen:
                raise PayloadBuildError(f"Duplicate evidence id: {evidence_id}")
            seen.add(evidence_id)
            merged.append(entry)
    return merged


def build_skeleton_report(date: str, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
    work_evidence = [entry for entry in evidence if entry.get("work_related")]
    first_id = work_evidence[0]["id"] if work_evidence else None
    evidence_ids = [first_id] if first_id else []

    return {
        "date": date,
        "summary": "待補",
        "completed": [
            {
                "workstream": "待補",
                "items": [
                    {
                        "text": "待補",
                        "evidence_ids": evidence_ids,
                    }
                ],
            }
        ],
        "blockers": [
            {
                "text": "待補",
                "evidence_ids": evidence_ids,
            }
        ],
        "tomorrow": [
            {
                "text": "待補",
                "evidence_ids": evidence_ids,
            }
        ],
        "analysis_additions": [
            {
                "title": "待補",
                "text": "待補",
                "evidence_ids": evidence_ids,
            }
        ],
    }


def build_payload(
    date: str,
    evidence: List[Dict[str, Any]],
    timezone: str = DEFAULT_TIMEZONE,
    report: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if not evidence:
        raise PayloadBuildError("At least one evidence entry is required.")
    return {
        "date": date,
        "timezone": timezone,
        "evidence": evidence,
        "report": report or build_skeleton_report(date, evidence),
    }


def write_payload(payload: Dict[str, Any], output_dir: str) -> Path:
    date = payload["date"]
    target_dir = Path(output_dir) / date[:4] / date[5:7]
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{date}.payload.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a daily report payload from manual JSONL evidence.")
    parser.add_argument("date", help="Report date in YYYY-MM-DD.")
    parser.add_argument("jsonl", nargs="+", help="One or more manual evidence JSONL files.")
    parser.add_argument("--timezone", default=DEFAULT_TIMEZONE)
    parser.add_argument("--output-dir", default="daily_report/payloads")
    args = parser.parse_args()

    try:
        groups = [read_jsonl(path) for path in args.jsonl]
        payload = build_payload(args.date, merge_evidence(*groups), args.timezone)
        target = write_payload(payload, args.output_dir)
    except PayloadBuildError as error:
        parser.exit(1, f"Error: {error}\n")

    print(f"Payload: {target}")


if __name__ == "__main__":
    main()

