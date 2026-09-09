from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urlparse

from mcp.server import MCPServer

from shared.policy import evidence_envelope

mcp = MCPServer("kubera-local-mcp")


def _official_gov_url(url: str) -> str:
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https":
        raise ValueError("Official local-service URL must use HTTPS")
    if not (host == "gov.uk" or host.endswith(".gov.uk")):
        raise ValueError("Only gov.uk official-source URLs are accepted by this starter")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in URLs are not allowed")
    return url.strip()


@mcp.tool()
def validate_official_service_url(url: str) -> dict[str, object]:
    """Validate that a supplied local-service URL is on an HTTPS gov.uk host."""
    checked = _official_gov_url(url)
    return {"valid": True, "url": checked, "source_class": "official_gov_uk"}


@mcp.tool()
def create_local_service_evidence(url: str, service_name: str, supplied_fact: str) -> dict:
    """Create an evidence envelope for a fact already obtained from an official gov.uk source."""
    checked = _official_gov_url(url)
    if not service_name.strip() or len(service_name) > 200:
        raise ValueError("service_name must be 1..200 characters")
    if len(supplied_fact) > 50_000:
        raise ValueError("supplied_fact is too large")
    retrieved_at = datetime.now(timezone.utc).isoformat()
    payload = {"service_name": service_name.strip(), "fact": supplied_fact}
    return {
        "service_name": service_name.strip(),
        "fact": supplied_fact,
        "evidence": evidence_envelope(
            source="UK local government",
            source_url=checked,
            payload=payload,
            retrieved_at=retrieved_at,
        ),
    }


@mcp.resource("kubera://local/policy")
def local_policy() -> str:
    return (
        "Local MCP starter accepts only HTTPS gov.uk source URLs and supplied facts. "
        "It does not determine legal eligibility, submit council forms or claim council partnership."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
