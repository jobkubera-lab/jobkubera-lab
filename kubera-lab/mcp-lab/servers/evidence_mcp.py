from __future__ import annotations

from datetime import datetime, timezone

from mcp.server import MCPServer

from shared.policy import evidence_envelope, validate_identifier

mcp = MCPServer("kubera-evidence-mcp")


@mcp.tool()
def create_evidence_record(source: str, payload: str, source_url: str | None = None) -> dict:
    """Create a privacy-minimal, hash-based evidence envelope from supplied content."""
    source_id = validate_identifier(source, field="source", max_length=100)
    if len(payload) > 100_000:
        raise ValueError("payload exceeds 100000 characters")
    retrieved_at = datetime.now(timezone.utc).isoformat()
    return evidence_envelope(
        source=source_id,
        source_url=source_url,
        payload=payload,
        retrieved_at=retrieved_at,
    )


@mcp.tool()
def verify_evidence_hash(payload: str, expected_hash: str) -> dict[str, object]:
    """Check whether supplied content matches an existing SHA-256 evidence hash."""
    record = evidence_envelope(
        source="verification",
        source_url=None,
        payload=payload,
        retrieved_at=datetime.now(timezone.utc).isoformat(),
    )
    actual = record["evidence_hash"]
    return {"matches": actual == expected_hash.lower(), "actual_hash": actual}


@mcp.resource("kubera://evidence/policy")
def evidence_policy() -> str:
    return (
        "Evidence MCP hashes supplied content and creates provenance envelopes. "
        "It does not grant arbitrary filesystem access and does not treat model prose as authoritative evidence."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
