from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from mcp.server import MCPServer

from shared.policy import evidence_envelope, validate_identifier

BASE = "https://api.beta.ons.gov.uk"
USER_AGENT = "KUBERA-ONS-MCP/0.1 (+https://github.com/jobkubera-lab/jobkubera-lab)"

mcp = MCPServer("kubera-ons-mcp")


def _safe_path(path: str) -> str:
    value = path.strip()
    if not value.startswith("/v1/"):
        raise ValueError("ONS path must start with /v1/")
    if ".." in value or "\\" in value:
        raise ValueError("Unsafe path")
    if len(value) > 2000:
        raise ValueError("Path is too long")
    return value


def _get(path: str) -> tuple[object, str]:
    safe = _safe_path(path)
    url = BASE + safe
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        payload = json.loads(response.read().decode(response.headers.get_content_charset() or "utf-8"))
    return payload, url


@mcp.tool()
def build_dataset_version_path(dataset: str, edition: str, version: int) -> dict[str, str]:
    """Build an allow-listed ONS API path for one dataset edition/version."""
    ds = validate_identifier(dataset, field="dataset")
    ed = validate_identifier(edition, field="edition")
    if version < 1:
        raise ValueError("version must be >= 1")
    path = f"/v1/datasets/{urllib.parse.quote(ds)}/editions/{urllib.parse.quote(ed)}/versions/{version}"
    return {"path": path, "url": BASE + path}


@mcp.tool()
def fetch_ons_json(path: str) -> dict:
    """Read JSON from the official ONS API. Only /v1/ paths on api.beta.ons.gov.uk are permitted."""
    payload, url = _get(path)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    return {
        "data": payload,
        "evidence": evidence_envelope(
            source="ONS",
            source_url=url,
            payload=payload,
            retrieved_at=retrieved_at,
        ),
    }


@mcp.resource("kubera://ons/policy")
def ons_policy() -> str:
    return (
        "ONS MCP is read-only and only retrieves /v1/ JSON from api.beta.ons.gov.uk. "
        "It does not browse arbitrary hosts and does not submit or modify ONS data."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
