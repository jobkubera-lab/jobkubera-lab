from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
import sqlite3
from threading import RLock
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
            "actor": self.actor,
            "operation": self.operation,
            "target": self.target,
            "request_hash": self.request_hash,
            "idempotency_key": self.idempotency_key,
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
    """Fail-closed source -> evidence -> action gate for consequential work."""

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
    IN_FLIGHT = "IN_FLIGHT"
    CONFLICT = "CONFLICT"


class IdempotencyState(str, Enum):
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"


@dataclass(frozen=True)
class IdempotencyDecision:
    outcome: IdempotencyOutcome
    state: IdempotencyState | None = None
    result_ref: str | None = None


class IdempotencyStore:
    """SQLite reservation store preventing duplicate side effects on retries.

    COMPLETE + same hash is a replay. PENDING + same hash is IN_FLIGHT and must
    never be executed again until an operator reconciles the external state.
    """

    def __init__(self, path: str = ":memory:") -> None:
        self._lock = RLock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
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
        with self._lock:
            try:
                self._conn.execute(
                    "INSERT INTO idempotency (key, request_hash, state, result_ref) VALUES (?, ?, 'PENDING', NULL)",
                    (key, request_hash),
                )
                self._conn.commit()
                return IdempotencyDecision(IdempotencyOutcome.NEW, IdempotencyState.PENDING)
            except sqlite3.IntegrityError:
                row = self._conn.execute(
                    "SELECT request_hash, state, result_ref FROM idempotency WHERE key = ?",
                    (key,),
                ).fetchone()
                assert row is not None
                existing_hash, state_text, result_ref = row
                state = IdempotencyState(state_text)
                if existing_hash != request_hash:
                    return IdempotencyDecision(IdempotencyOutcome.CONFLICT, state, result_ref)
                if state is IdempotencyState.PENDING:
                    return IdempotencyDecision(IdempotencyOutcome.IN_FLIGHT, state, result_ref)
                return IdempotencyDecision(IdempotencyOutcome.REPLAY, state, result_ref)

    def complete(self, key: str, *, result_ref: str) -> None:
        if not result_ref.strip():
            raise ValueError("result_ref must not be empty")
        with self._lock:
            cur = self._conn.execute(
                "UPDATE idempotency SET state = 'COMPLETE', result_ref = ? WHERE key = ? AND state = 'PENDING'",
                (result_ref, key),
            )
            if cur.rowcount == 1:
                self._conn.commit()
                return
            row = self._conn.execute(
                "SELECT state, result_ref FROM idempotency WHERE key = ?",
                (key,),
            ).fetchone()
            if row is None:
                raise KeyError(f"unknown idempotency key: {key}")
            state_text, existing_ref = row
            if state_text == IdempotencyState.COMPLETE.value and existing_ref == result_ref:
                return
            raise RuntimeError(f"idempotency key cannot be completed from state {state_text}")

    def close(self) -> None:
        with self._lock:
            self._conn.close()


class ActionStatus(str, Enum):
    QUEUED = "QUEUED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    EXECUTED = "EXECUTED"
    CONFIRMED_SUCCEEDED = "CONFIRMED_SUCCEEDED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    REPLAYED = "REPLAYED"
    UNKNOWN_EXTERNAL_STATE = "UNKNOWN_EXTERNAL_STATE"


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
