from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = {"id", "name", "area", "category", "kind", "description", "source_url", "source_type", "last_checked", "trust"}
TRUST_KEYS = {"authority", "freshness", "direct_link", "local_relevance"}


def validate_item(item: dict) -> None:
    missing = REQUIRED - set(item)
    if missing:
        raise ValueError(f"{item.get('id', '<unknown>')}: missing {sorted(missing)}")
    if item["area"] not in {"London", "Merton"}:
        raise ValueError(f"{item['id']}: unsupported area")
    parsed = urlparse(item["source_url"])
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"{item['id']}: source_url must be HTTPS")
    if set(item["trust"]) != TRUST_KEYS:
        raise ValueError(f"{item['id']}: trust fields must be exactly {sorted(TRUST_KEYS)}")
    values = item["trust"].values()
    if any(not isinstance(v, int) or v < 0 for v in values):
        raise ValueError(f"{item['id']}: invalid trust values")
    if sum(values) > 100:
        raise ValueError(f"{item['id']}: trust score exceeds 100")


def validate(path: Path) -> int:
    items = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(items, list) or not items:
        raise ValueError("data must be a non-empty list")
    ids = set()
    for item in items:
        validate_item(item)
        if item["id"] in ids:
            raise ValueError(f"duplicate id: {item['id']}")
        ids.add(item["id"])
    return len(items)


if __name__ == "__main__":
    count = validate(Path(__file__).with_name("data.json"))
    print(f"OK: {count} Community Compass seed sources validated")
