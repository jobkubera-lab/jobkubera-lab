from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
import sqlite3
from typing import Any

from .authorization_grant import AuthorizationGrant, AuthorizationSigner
from .constitution import Decision
from .evidence_ledger import EvidenceEntry, EvidenceLedger


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def hash_request(value: Any) -> str:
    return "sha256:" + sha256(_canonical_json(value).encode("utf-8")).hexdigest()


class Reversibility(str, Enum):
    REVERSIBLE = "REVERSIBLE"
    IRREVERSIBLE = "IRREVERSIBLE"


class GateOutcome(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


@dataclass(frozen=True)
class ActionIntent:
    action_id: str
    run_id: str
    actor: str
    operation: str
    target: str
    request_hash: str
    reversibility: Reversibility
    idempotency_key: str

    def __post_init__(self) -> None:
        for name in ("action_id", "run_id", "actor", "operation", "target", "request_hash", "idempotency_key"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must not be empty")
        if not self.request_hash.startswith("sha256:"):
            raise ValueError("request_hash must be a sha256: digest")

    @property
    def fingerprint(self) -> str:
        packet = {
            "operation": self.operation,
            "target": self.target,
            "request_hash": self.request_hash,
        }
        return hash_request(packet)

    @property
    def approval_scope(self) -> str:
        return f"execute:{self.operation}"


@dataclass(frozen=True)
class GateDecision:
    outcome: GateOutcome
    reason: str

    @property
    def allowed(self) -> bool:
        return self.outcome is GateOutcome.ALLOW

    @property
    def requires_approval(self) -> bool:
        return self.outcome is GateOutcome.REQUIRE_APPROVAL


class SourceEvidenceActionGate:
    """Fail-closed source -> evidence -> action gate for consequential work.

    Irreversible work requires a signed grant even if policy would otherwise
    allow it. The grant is checked against the exact action fingerprint.
    """

    def evaluate(
        self,
        intent: ActionIntent,
        *,
        source_verified: bool,
        evidence_verified: bool,
        policy_decision: Decision,
        grant: AuthorizationGrant | None = None,
        signer: AuthorizationSigner | None = None,
    ) -> GateDecision:
        if not source_verified:
            return GateDecision(GateOutcome.BLOCK, "source gate failed")
        if not evidence_verified:
            return GateDecision(GateOutcome.BLOCK, "evidence gate failed")
        if policy_decision is Decision.DENY:
            return GateDecision(GateOutcome.BLOCK, "owner policy denied action")

        approval_required = (
            policy_decision is Decision.REQUIRE_APPROVAL
            or intent.reversibility is Reversibility.IRREVERSIBLE
        )
        if not approval_required:
            return GateDecision(GateOutcome.ALLOW, "all gates passed")

        if grant is None or signer is None:
            return GateDecision(GateOutcome.REQUIRE_APPROVAL, "signed human approval required")

        if not signer.verify(
            grant,
            required_scope=intent.approval_scope,
            subject=intent.fingerprint,
        ):
            return GateDecision(GateOutcome.BLOCK, "approval grant invalid for exact action")

        return GateDecision(GateOutcome.ALLOW, "signed approval verified for exact action")


class IdempotencyOutcome(str, Enum):
    NEW = "NEW"
    REPLAY = "REPLAY"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class IdempotencyDecision:
    outcome: IdempotencyOutcome
    result_ref: str | None = None


class IdempotencyStore:
    """SQLite reservation store preventing duplicate side effects on retries."""

    def __init__(self, path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS idempotency (
                key TEXT PRIMARY KEY,
                request_hash TEXT NOT NULL,
                state TEXT NOT NULL,
                result_ref TEXT
            )
            """
        )
        self._conn.commit()

    def reserve(self, key: str, request_hash: str) -> IdempotencyDecision:
        if not key.strip() or not request_hash.strip():
            raise ValueError("idempotency key and request_hash must not be empty")
        try:
            self._conn.execute(
                "INSERT INTO idempotency (key, request_hash, state, result_ref) VALUES (?, ?, 'PENDING', NULL)",
                (key, request_hash),
            )
            self._conn.commit()
            return IdempotencyDecision(IdempotencyOutcome.NEW)
        except sqlite3.IntegrityError:
            row = self._conn.execute(
                "SELECT request_hash, state, result_ref FROM idempotency WHERE key = ?",
                (key,),
            ).fetchone()
            assert row is not None
            existing_hash, _state, result_ref = row
            if existing_hash != request_hash:
                return IdempotencyDecision(IdempotencyOutcome.CONFLICT)
            return IdempotencyDecision(IdempotencyOutcome.REPLAY, result_ref)

    def complete(self, key: str, *, result_ref: str) -> None:
        if not result_ref.strip():
            raise ValueError("result_ref must not be empty")
        cur = self._conn.execute(
            "UPDATE idempotency SET state = 'COMPLETE', result_ref = ? WHERE key = ?",
            (result_ref, key),
        )
        if cur.rowcount != 1:
            raise KeyError(f"unknown idempotency key: {key}")
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


class ActionStatus(str, Enum):
    QUEUED = "QUEUED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    EXECUTED = "EXECUTED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    REPLAYED = "REPLAYED"


class ActionLogger:
    """Structured action log stored in the existing hash-chained Evidence Ledger."""

    def __init__(self, ledger: EvidenceLedger) -> None:
        self.ledger = ledger

    def record(
        self,
        intent: ActionIntent,
        *,
        status: ActionStatus,
        result: Any,
        source_refs: tuple[str, ...] = (),
        evidence_refs: tuple[str, ...] = (),
        approval_grant_id: str | None = None,
    ) -> EvidenceEntry:
        metadata = {
            "event_type": "action",
            "action_id": intent.action_id,
            "actor": intent.actor,
            "operation": intent.operation,
            "target": intent.target,
            "reversibility": intent.reversibility.value,
            "idempotency_key": intent.idempotency_key,
            "status": status.value,
            "source_refs": list(source_refs),
            "evidence_refs": list(evidence_refs),
            "approval_grant_id": approval_grant_id,
        }
        return self.ledger.append(
            run_id=intent.run_id,
            stage="action_log",
            input_value={
                "action_fingerprint": intent.fingerprint,
                "request_hash": intent.request_hash,
            },
            output_value=result,
            metadata=metadata,
        )
