from __future__ import annotations

import json
import statistics
from typing import Any

from mcp.server import MCPServer

mcp = MCPServer("kubera-collector-mcp")


def _parse_listings(listings_json: str) -> list[dict[str, Any]]:
    if len(listings_json) > 250_000:
        raise ValueError("listings_json is too large")
    value = json.loads(listings_json)
    if not isinstance(value, list):
        raise ValueError("listings_json must be a JSON array")
    cleaned: list[dict[str, Any]] = []
    for row in value:
        if not isinstance(row, dict):
            continue
        title = str(row.get("title") or "").strip()[:300]
        url = str(row.get("url") or "").strip()[:2000]
        try:
            price = float(row.get("price"))
        except (TypeError, ValueError):
            continue
        if price < 0:
            continue
        cleaned.append({"title": title, "price": price, "url": url})
    return cleaned


@mcp.tool()
def compare_supplied_listings(listings_json: str, currency: str = "GBP") -> dict:
    """Compare prices from listings supplied by the caller. This starter does not scrape marketplaces."""
    listings = _parse_listings(listings_json)
    if not listings:
        return {"count": 0, "currency": currency.upper()[:8], "ranked": []}
    ranked = sorted(listings, key=lambda row: row["price"])
    prices = [row["price"] for row in ranked]
    return {
        "count": len(ranked),
        "currency": currency.upper()[:8],
        "lowest": ranked[0],
        "highest": ranked[-1],
        "median_price": statistics.median(prices),
        "ranked": ranked[:50],
        "source_note": "Comparison uses caller-supplied listings only; no live marketplace retrieval was performed."
    }


@mcp.tool()
def filter_budget(listings_json: str, max_price: float) -> dict:
    """Return supplied listings at or below a price ceiling."""
    if max_price < 0:
        raise ValueError("max_price must be non-negative")
    matches = [row for row in _parse_listings(listings_json) if row["price"] <= max_price]
    matches.sort(key=lambda row: row["price"])
    return {"count": len(matches), "max_price": max_price, "matches": matches[:50]}


@mcp.resource("kubera://collector/policy")
def collector_policy() -> str:
    return (
        "Collector MCP starter compares caller-supplied market evidence. It does not authenticate to marketplaces, "
        "place orders, contact sellers or present an estimate as a certified valuation."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
