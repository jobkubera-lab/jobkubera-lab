"""Single controlled execution boundary for reference external tools.

KUBERA prepares. The human remains the authority.

This module composes existing handoff, privacy, validation, source/evidence/action
and idempotency primitives. Tool adapters are injected and receive only finalized
sanitized arguments; no live provider integration is included here.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Mapping, Protocol

from .authorization_grant import AuthorizationGrant, AuthorizationSigner
from .constitution import Decision
from .execution_controls import (
    ActionIntent,
    ActionLogger,
    ActionStatus,
    GateOutcome,
    IdempotencyOutcome,
    IdempotencyStore,
    Reversibility,
    SourceEvidenceActionGate,
    hash_request,
)
from .handoff import HandoffArtifact, HandoffStatus
from .tool_safety import PrivacyGate, ToolValidator


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


IRREVERSIBLE_OPERATIONS = frozenset({"send", "publish", "pay", "delete", "sign"})


@dataclass(frozen=True)
class ToolRequest:
    """Immutable canonical request before governance and adapter execution."""

    action_id: str
    run_id: str
    actor: str
    tool_name: str
    operation: str
    target: str
    arguments_json: str
    idempotency_key: str
    reversibility: Reversibility = Reversibility.REVERSIBLE

    @classmethod
    def create(
        cls,
        *,
        action_id: str,
        run_id: str,
        actor: str,
        tool_name: str,
        operation: str,
        target: str,
        arguments: Mapping[str, Any],
        idempotency_key: str,
        reversibility: Reversibility = Reversibility.REVERSIBLE,
    ) -> "ToolRequest":
        text_fields = {
            "action_id": action_id,
            "run_id": run_id,
            "actor": actor,
            "tool_name": tool_name,
            "operation": operation,
            "target": target,
            "idempotency_key": idempotency_key,
        }
        empty = [name for name, value in text_fields.items() if not str(value).strip()]
        if empty:
            raise ValueError(f"tool request fields must not be empty: {', '.join(empty)}")
        if not isinstance(arguments, Mapping):
            raise TypeError("tool arguments must be a mapping")
        # Canonical JSON both validates JSON-serializability and prevents later
        # caller mutation from changing the approved request identity.
        arguments_json = _canonical_json(dict(arguments))
        return cls(
            action_id=str(action_id).strip(),
            run_id=str(run_id).strip(),
            actor=str(actor).strip(),
            tool_name=str(tool_name).strip(),
            operation=str(operation).strip(),
            target=str(target).strip(),
            arguments_json=arguments_json,
            idempotency_key=str(idempotency_key).strip(),
            reversibility=reversibility,
        )

    @property
    def arguments(self) -> dict[str, Any]:
        # Return a fresh object so adapters cannot mutate the canonical request.
        return json.loads(self.arguments_json)

    @property
    def request_hash(self) -> str:
        return hash_request(
            {
                "tool_name": self.tool_name,
                "operation": self.operation,
                "target": self.target,
                "arguments": self.arguments,
            }
        )

    @property
    def effective_reversibility(self) -> Reversibility:
        if self.reversibility is Reversibility.IRREVERSIBLE:
            return Reversibility.IRREVERSIBLE
        if self.operation.casefold() in IRREVERSIBLE_OPERATIONS:
            return Reversibility.IRREVERSIBLE
        return Reversibility.REVERSIBLE

    def to_intent(self) -> ActionIntent:
        return ActionIntent(
            action_id=self.action_id,
            run_id=self.run_id,
            actor=self.actor,
            operation=self.operation,
            target=self.target,
            request_hash=self.request_hash,
            reversibility=self.effective_reversibility,
            idempotency_key=self.idempotency_key,
        )


class ToolAdapter(Protocol):
    """Narrow adapter boundary. Governance objects and signing secrets stay outside."""

    def execute(
        self,
        *,
        tool_name: str,
        operation: str,
        target: str,
        arguments: Mapping[str, Any],
    ) -> Any: ...


class ToolExecutionStatus(str, Enum):
    EXECUTED = "EXECUTED"
    BLOCKED = "BLOCKED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    REPLAYED = "REPLAYED"
    CONFLICT = "CONFLICT"
    PENDING_RECONCILIATION = "PENDING_RECONCILIATION"


@dataclass(frozen=True)
class ToolExecutionResult:
    status: ToolExecutionStatus
    result: Any = None
    evidence_entry_id: str | None = None
    result_ref: str | None = None
    reason: str = ""

    @property
    def executed(self) -> bool:
        return self.status is ToolExecutionStatus.EXECUTED


class SovereignToolExecutor:
    """Compose all mandatory gates before an injected tool adapter is callable."""

    def __init__(
        self,
        *,
        adapter: ToolAdapter,
        idempotency_store: IdempotencyStore,
        action_logger: ActionLogger,
        gate: SourceEvidenceActionGate | None = None,
        signer: AuthorizationSigner | None = None,
    ) -> None:
        self._adapter = adapter
        self._idempotency = idempotency_store
        self._logger = action_logger
        self._gate = gate or SourceEvidenceActionGate()
        self._signer = signer

    def _log(
        self,
        intent: ActionIntent,
        *,
        status: ActionStatus,
        result: Any,
        handoff: HandoffArtifact,
        grant: AuthorizationGrant | None,
    ):
        return self._logger.record(
            intent,
            status=status,
            result=result,
            source_refs=handoff.source_refs,
            evidence_refs=handoff.evidence_refs,
            approval_grant_id=grant.grant_id if grant else None,
        )

    def execute(
        self,
        request: ToolRequest,
        *,
        handoff: HandoffArtifact,
        schema: Mapping[str, Any],
        source_verified: bool,
        evidence_verified: bool,
        policy_decision: Decision,
        grant: AuthorizationGrant | None = None,
    ) -> ToolExecutionResult:
        intent = request.to_intent()

        if not isinstance(handoff, HandoffArtifact) or handoff.status is not HandoffStatus.READY:
            # A non-ready/missing handoff must never reach the adapter.
            if isinstance(handoff, HandoffArtifact):
                entry = self._log(
                    intent,
                    status=ActionStatus.BLOCKED,
                    result={"reason": "ready handoff required"},
                    handoff=handoff,
                    grant=grant,
                )
                return ToolExecutionResult(
                    ToolExecutionStatus.BLOCKED,
                    evidence_entry_id=entry.entry_id,
                    reason="ready handoff required",
                )
            return ToolExecutionResult(ToolExecutionStatus.BLOCKED, reason="handoff required")

        # Privacy is enforced before exact adapter arguments are validated or exposed.
        scan = PrivacyGate.sanitize(request.arguments)
        sanitized = scan.value
        validation = ToolValidator.validate(sanitized, schema)
        if not validation.valid:
            entry = self._log(
                intent,
                status=ActionStatus.BLOCKED,
                result={"reason": validation.error, "redacted_paths": list(scan.redacted_paths)},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.BLOCKED,
                evidence_entry_id=entry.entry_id,
                reason=validation.error or "tool validation failed",
            )

        # Verified booleans alone are insufficient: the handoff must carry refs.
        source_ok = bool(source_verified and handoff.source_refs)
        evidence_ok = bool(evidence_verified and handoff.evidence_refs)
        decision = self._gate.evaluate(
            intent,
            source_verified=source_ok,
            evidence_verified=evidence_ok,
            policy_decision=policy_decision,
            grant=grant,
            signer=self._signer,
        )
        if decision.outcome is GateOutcome.REQUIRE_APPROVAL:
            entry = self._log(
                intent,
                status=ActionStatus.APPROVAL_REQUIRED,
                result={"reason": decision.reason},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.APPROVAL_REQUIRED,
                evidence_entry_id=entry.entry_id,
                reason=decision.reason,
            )
        if decision.outcome is GateOutcome.BLOCK:
            entry = self._log(
                intent,
                status=ActionStatus.BLOCKED,
                result={"reason": decision.reason},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.BLOCKED,
                evidence_entry_id=entry.entry_id,
                reason=decision.reason,
            )

        reservation = self._idempotency.reserve(request.idempotency_key, request.request_hash)
        if reservation.outcome is IdempotencyOutcome.CONFLICT:
            entry = self._log(
                intent,
                status=ActionStatus.BLOCKED,
                result={"reason": "idempotency key conflicts with another request"},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.CONFLICT,
                evidence_entry_id=entry.entry_id,
                reason="idempotency conflict",
            )
        if reservation.outcome is IdempotencyOutcome.REPLAY:
            status = (
                ToolExecutionStatus.REPLAYED
                if reservation.result_ref
                else ToolExecutionStatus.PENDING_RECONCILIATION
            )
            entry = self._log(
                intent,
                status=ActionStatus.REPLAYED,
                result={"result_ref": reservation.result_ref, "replayed": True},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                status,
                evidence_entry_id=entry.entry_id,
                result_ref=reservation.result_ref,
                reason=(
                    "existing completed action replayed without side effect"
                    if reservation.result_ref
                    else "existing reservation has no confirmed result; reconcile before retry"
                ),
            )

        try:
            # Adapter receives only finalized sanitized arguments, never signer/grant objects.
            result = self._adapter.execute(
                tool_name=request.tool_name,
                operation=request.operation,
                target=request.target,
                arguments=json.loads(_canonical_json(sanitized)),
            )
        except Exception as exc:  # fail closed: reservation remains PENDING
            entry = self._log(
                intent,
                status=ActionStatus.FAILED,
                result={"error_type": type(exc).__name__, "error": str(exc)},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.PENDING_RECONCILIATION,
                evidence_entry_id=entry.entry_id,
                reason="adapter outcome not safely repeatable; reconcile before retry",
            )

        entry = self._log(
            intent,
            status=ActionStatus.EXECUTED,
            result=result,
            handoff=handoff,
            grant=grant,
        )
        result_ref = f"evidence:{entry.entry_id}"
        self._idempotency.complete(request.idempotency_key, result_ref=result_ref)
        return ToolExecutionResult(
            ToolExecutionStatus.EXECUTED,
            result=result,
            evidence_entry_id=entry.entry_id,
            result_ref=result_ref,
            reason="all gates passed and tool executed once",
        )
