import json
import tempfile
import unittest
from pathlib import Path

from daily_report.build_payload import (
    PayloadBuildError,
    build_payload,
    merge_evidence,
    read_jsonl,
    write_payload,
)


class BuildPayloadTests(unittest.TestCase):
    def test_read_jsonl_adds_stable_id(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "input.jsonl"
            path.write_text(
                '{"source_type":"manual","timestamp":"2026-07-29T18:00:00+08:00","title":"測試","text":"完成測試。","work_related":true}\n',
                encoding="utf-8",
            )

            entries = read_jsonl(str(path))

        self.assertEqual(len(entries), 1)
        self.assertTrue(entries[0]["id"].startswith("manual:manual:"))

    def test_merge_evidence_rejects_duplicate_ids(self):
        evidence = [{"id": "manual:1"}, {"id": "manual:1"}]

        with self.assertRaises(PayloadBuildError):
            merge_evidence(evidence)

    def test_build_payload_creates_skeleton_report(self):
        evidence = [{"id": "manual:1", "work_related": True}]

        payload = build_payload("2026-07-29", evidence)

        self.assertEqual(payload["report"]["summary"], "待補")
        self.assertEqual(payload["report"]["completed"][0]["items"][0]["evidence_ids"], ["manual:1"])

    def test_write_payload_uses_date_path(self):
        payload = build_payload("2026-07-29", [{"id": "manual:1", "work_related": True}])

        with tempfile.TemporaryDirectory() as temp_dir:
            target = write_payload(payload, temp_dir)
            saved = json.loads(target.read_text(encoding="utf-8"))

        self.assertEqual(target.name, "2026-07-29.payload.json")
        self.assertEqual(saved["date"], "2026-07-29")


if __name__ == "__main__":
    unittest.main()

