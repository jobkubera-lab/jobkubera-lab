from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = {
    "id", "title", "start", "end", "area", "borough", "venue", "address",
    "category", "price_type", "price_text", "organiser", "source_url",
    "source_type", "checked_at", "status",
}
VALID_AREAS = {"London", "Merton"}
VALID_PRICE_TYPES = {"FREE", "PAID", "UNKNOWN"}
VALID_STATUSES = {"CURRENT", "CANCELLED"}
VALID_CATEGORIES = {"community", "culture", "sport", "wellbeing", "learning", "volunteering"}


def parse_iso(value: str, field: str, event_id: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{event_id}: {field} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{event_id}: {field} must include a timezone offset")
    return parsed


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def fingerprint(item: dict) -> str:
    start = parse_iso(item["start"], "start", item["id"])
    return "|".join((normalize(item["title"]), start.isoformat(), normalize(item["venue"])))


def validate_item(item: dict) -> None:
    missing = REQUIRED - set(item)
    if missing:
        raise ValueError(f"{item.get('id', '<unknown>')}: missing {sorted(missing)}")
    event_id = item["id"]
    if item["area"] not in VALID_AREAS:
        raise ValueError(f"{event_id}: unsupported area")
    if item["price_type"] not in VALID_PRICE_TYPES:
        raise ValueError(f"{event_id}: unsupported price_type")
    if item["status"] not in VALID_STATUSES:
        raise ValueError(f"{event_id}: unsupported status")
    if item["category"] not in VALID_CATEGORIES:
        raise ValueError(f"{event_id}: unsupported category")
    parsed_url = urlparse(item["source_url"])
    if parsed_url.scheme != "https" or not parsed_url.netloc:
        raise ValueError(f"{event_id}: source_url must be HTTPS")
    start = parse_iso(item["start"], "start", event_id)
    end = parse_iso(item["end"], "end", event_id)
    if end <= start:
        raise ValueError(f"{event_id}: end must be after start")
    try:
        datetime.strptime(item["checked_at"], "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{event_id}: checked_at must be YYYY-MM-DD") from exc
    for coord in ("lat", "lon"):
        if coord in item and not isinstance(item[coord], (int, float)):
            raise ValueError(f"{event_id}: {coord} must be numeric")


def validate(path: Path) -> int:
    items = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(items, list) or not items:
        raise ValueError("events must be a non-empty list")
    ids: set[str] = set()
    fingerprints: set[str] = set()
    for item in items:
        validate_item(item)
        if item["id"] in ids:
            raise ValueError(f"duplicate id: {item['id']}")
        ids.add(item["id"])
        fp = fingerprint(item)
        if fp in fingerprints:
            raise ValueError(f"duplicate event fingerprint: {item['id']}")
        fingerprints.add(fp)
    return len(items)


if __name__ == "__main__":
    count = validate(Path(__file__).with_name("events.json"))
    print(f"OK: {count} Community Compass events validated")
