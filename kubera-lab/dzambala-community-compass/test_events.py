from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from validate_events import fingerprint, validate


class EventValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sample = {
            "id": "event-1",
            "title": "Community Event",
            "start": "2026-09-05T10:00:00+01:00",
            "end": "2026-09-05T12:00:00+01:00",
            "area": "Merton",
            "borough": "Merton",
            "venue": "Town Hall",
            "address": "Example Street",
            "category": "community",
            "price_type": "FREE",
            "price_text": "Free",
            "organiser": "Example",
            "source_url": "https://example.org/event",
            "source_type": "official",
            "checked_at": "2026-08-30",
            "status": "CURRENT",
        }

    def write(self, items: list[dict]) -> Path:
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(items, handle)
        handle.close()
        return Path(handle.name)

    def test_seed_file_is_valid(self) -> None:
        self.assertGreater(validate(Path(__file__).with_name("events.json")), 0)

    def test_duplicate_ids_are_rejected(self) -> None:
        path = self.write([self.sample, dict(self.sample)])
        with self.assertRaisesRegex(ValueError, "duplicate id"):
            validate(path)

    def test_duplicate_fingerprint_is_rejected(self) -> None:
        second = dict(self.sample, id="event-2")
        path = self.write([self.sample, second])
        with self.assertRaisesRegex(ValueError, "duplicate event fingerprint"):
            validate(path)

    def test_timezone_is_required(self) -> None:
        broken = dict(self.sample, start="2026-09-05T10:00:00")
        path = self.write([broken])
        with self.assertRaisesRegex(ValueError, "timezone"):
            validate(path)

    def test_bad_source_url_is_rejected(self) -> None:
        broken = dict(self.sample, source_url="http://example.org/event")
        path = self.write([broken])
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            validate(path)

    def test_end_must_follow_start(self) -> None:
        broken = dict(self.sample, end=self.sample["start"])
        path = self.write([broken])
        with self.assertRaisesRegex(ValueError, "end must be after start"):
            validate(path)

    def test_fingerprint_normalises_text(self) -> None:
        a = self.sample
        b = dict(self.sample, id="event-2", title="Community---Event", venue="Town   Hall")
        self.assertEqual(fingerprint(a), fingerprint(b))


if __name__ == "__main__":
    unittest.main()
