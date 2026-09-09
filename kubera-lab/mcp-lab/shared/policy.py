from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Iterable
from urllib.parse import urlparse


class SideEffect(StrEnum):
    READ_ONLY = "READ_ONLY"
    PREPARE_ONLY = "PREPARE_ONLY"
    WRITE_REQUIRES_APPROVAL = "WRITE_REQUIRES_APPROVAL"
    PROHIBITED = "PROHIBITED"


@dataclass(frozen=True)
class ToolPolicy:
    server: str
    tool: str
    side_effect: SideEffect
    allowed_hosts: tuple[str, ...] = ()
    max_input_chars: int = 20_000


@dataclass(frozen=True)
class ApprovalReceipt:
    action_id: str
    tool: str
    approved: bool
    nonce: str


def canonical_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_identifier(value: str, *, field: str = "id", max_length: int = 120) -> str:
    candidate = value.strip()
    if not candidate:
        raise ValueError(f"{field} cannot be empty")
    if len(candidate) > max_length:
        raise ValueError(f"{field} is too long")
    if not re.fullmatch(r"[A-Za-z0-9._:/-]+", candidate):
        raise ValueError(f"{field} contains unsupported characters")
    return candidate


def require_allowed_url(url: str, allowed_hosts: Iterable[str]) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")
    host = (parsed.hostname or "").lower()
    allowed = {item.lower() for item in allowed_hosts}
    if host not in allowed:
        raise ValueError(f"Host is not allow-listed: {host or '<missing>'}")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in URLs are not allowed")
    return url


def enforce_tool_policy(
    policy: ToolPolicy,
    *,
    input_text: str = "",
    target_url: str | None = None,
    approval: ApprovalReceipt | None = None,
) -> None:
    if policy.side_effect == SideEffect.PROHIBITED:
        raise PermissionError("Tool is prohibited")
    if len(input_text) > policy.max_input_chars:
        raise ValueError("Tool input exceeds configured size budget")
    if target_url is not None:
        require_allowed_url(target_url, policy.allowed_hosts)
    if policy.side_effect == SideEffect.WRITE_REQUIRES_APPROVAL:
        if approval is None or not approval.approved:
            raise PermissionError("A valid human approval receipt is required")
        if approval.tool != policy.tool:
            raise PermissionError("Approval receipt does not match tool")


def evidence_envelope(*, source: str, source_url: str | None, payload: Any, retrieved_at: str) -> dict[str, Any]:
    return {
        "source": source,
        "source_url": source_url,
        "retrieved_at": retrieved_at,
        "evidence_hash": canonical_hash(payload),
    }
