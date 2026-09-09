from __future__ import annotations

from datetime import datetime, timezone

from mcp.server import MCPServer

mcp = MCPServer("kubera-business-mcp")


def _clean(value: str, *, field: str, limit: int = 300) -> str:
    text = value.strip()
    if not text:
        raise ValueError(f"{field} cannot be empty")
    if len(text) > limit:
        raise ValueError(f"{field} is too long")
    return text


@mcp.tool()
def prepare_booking_request(customer_name: str, service: str, preferred_time: str, notes: str = "") -> dict:
    """Prepare, but do not create, a customer booking request."""
    customer = _clean(customer_name, field="customer_name", limit=120)
    requested_service = _clean(service, field="service", limit=200)
    requested_time = _clean(preferred_time, field="preferred_time", limit=200)
    if len(notes) > 2000:
        raise ValueError("notes is too long")
    return {
        "status": "DRAFT_ONLY",
        "human_approval_required": True,
        "external_write_performed": False,
        "prepared_at": datetime.now(timezone.utc).isoformat(),
        "booking_request": {
            "customer_name": customer,
            "service": requested_service,
            "preferred_time": requested_time,
            "notes": notes.strip(),
        },
        "next_action": "A separate approved calendar/CRM write tool would be required to create this booking."
    }


@mcp.tool()
def prepare_customer_reply(customer_name: str, message: str, proposed_reply: str) -> dict:
    """Package a proposed customer reply for human review. It does not send anything."""
    customer = _clean(customer_name, field="customer_name", limit=120)
    if len(message) > 10_000 or len(proposed_reply) > 10_000:
        raise ValueError("message or reply is too long")
    return {
        "status": "DRAFT_ONLY",
        "human_approval_required": True,
        "external_write_performed": False,
        "customer_name": customer,
        "customer_message": message,
        "proposed_reply": proposed_reply,
    }


@mcp.resource("kubera://business/policy")
def business_policy() -> str:
    return (
        "Business MCP starter is PREPARE_ONLY. It cannot send WhatsApp/email messages, create calendar bookings, "
        "change CRM records or charge customers. Future writes require authenticated integrations and approval receipts."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
