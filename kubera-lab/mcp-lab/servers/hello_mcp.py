from __future__ import annotations

from datetime import datetime, timezone

from mcp.server import MCPServer

mcp = MCPServer("kubera-hello-mcp")


@mcp.tool()
def hello(name: str = "world") -> dict[str, str]:
    """Return a deterministic greeting for MCP smoke testing."""
    safe_name = name.strip()[:80] or "world"
    return {"message": f"Hello, {safe_name}.", "server": "kubera-hello-mcp"}


@mcp.tool()
def utc_time() -> dict[str, str]:
    """Return current UTC time from the server runtime."""
    return {"utc": datetime.now(timezone.utc).isoformat()}


@mcp.resource("kubera://hello/about")
def about() -> str:
    return "KUBERA Hello MCP is a read-only learning and smoke-test server."


if __name__ == "__main__":
    mcp.run(transport="stdio")
