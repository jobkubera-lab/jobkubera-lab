"""Single controlled execution boundary for KUBERA / DZAMBALA tools.

KUBERA prepares. The human remains the authority.

The executor composes existing handoff, privacy, validation, source/evidence/action
and idempotency primitives. No live provider adapter is wired in this reference.
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
from .work_contract import WorkContract


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


IRREVERSIBLE_OPERATIONS = frozenset(
    {"send", "publish", "pay", "delete", "sign", "buy", "accept terms", "accept_terms", "launch"}
)


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
        return cls(
            action_id=str(action_id).strip(),
            run_id=str(run_id).strip(),
            actor=str(actor).strip(),
            tool_name=str(tool_name).strip(),
            operation=str(operation).strip(),
            target=str(target).strip(),
            arguments_json=_canonical_json(dict(arguments)),
            idempotency_key=str(idempotency_key).strip(),
            reversibility=reversibility,
        )

    @property
    def arguments(self) -> dict[str, Any]:
        return json.loads(self.arguments_json)

    @property
    def effective_reversibility(self) -> Reversibility:
        if self.reversibility is Reversibility.IRREVERSIBLE:
            return Reversibility.IRREVERSIBLE
        if self.operation.casefold() in IRREVERSIBLE_OPERATIONS:
            return Reversibility.IRREVERSIBLE
        return Reversibility.REVERSIBLE

    def intent_for_hash(self, request_hash: str) -> ActionIntent:
        return ActionIntent(
            action_id=self.action_id,
            run_id=self.run_id,
            actor=self.actor,
            operation=self.operation,
            target=self.target,
            request_hash=request_hash,
            reversibility=self.effective_reversibility,
            idempotency_key=self.idempotency_key,
        )


@dataclass(frozen=True)
class PreparedToolCall:
    """Final immutable payload shared by approval, idempotency and execution."""

    request: ToolRequest
    arguments_json: str
    request_hash: str
    intent: ActionIntent
    redacted_paths: tuple[str, ...]

    @property
    def arguments(self) -> dict[str, Any]:
        return json.loads(self.arguments_json)


class ToolAdapter(Protocol):
    """Narrow adapter boundary; signer/grant/governance objects never cross it."""

    def execute(
        self,
        *,
        tool_name: str,
        operation: str,
        target: str,
        arguments: Mapping[str, Any],
    ) -> Any: ...


class ToolExecutionStatus(str, Enum):
    PREPARED = "PREPARED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    RESERVED = "RESERVED"
    EXECUTING = "EXECUTING"
    SUCCEEDED = "SUCCEEDED"
    EXECUTED = "SUCCEEDED"  # compatibility alias
    FAILED = "FAILED"
    UNKNOWN_EXTERNAL_STATE = "UNKNOWN_EXTERNAL_STATE"
    BLOCKED = "BLOCKED"
    REPLAYED = "REPLAYED"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class ToolExecutionResult:
    status: ToolExecutionStatus
    result: Any = None
    evidence_entry_id: str | None = None
    result_ref: str | None = None
    reason: str = ""

    @property
    def executed(self) -> bool:
        return self.status is ToolExecutionStatus.SUCCEEDED


class SovereignToolExecutor:
    """The only reference execution choke point for injected ToolAdapter calls.

    Real deployments must additionally keep provider credentials and raw clients
    outside agent/plugin reach. Python code cannot stop arbitrary code that already
    owns those credentials from bypassing this object.
    """

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
        self._ledger = action_logger.ledger
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

    def _references_verified(self, refs: tuple[str, ...], *, expected_kind: str) -> bool:
        if not refs:
            return False
        for ref in refs:
            entry = self._ledger.resolve_reference(ref)
            if entry is None:
                return False
            if entry.metadata.get("reference_kind") != expected_kind:
                return False
            if entry.metadata.get("verified") is not True:
                return False
        return True

    def prepare(self, request: ToolRequest, *, schema: Mapping[str, Any]) -> PreparedToolCall:
        """Sanitize, validate and freeze the exact payload that may be executed."""
        scan = PrivacyGate.sanitize(request.arguments)
        sanitized = scan.value
        validation = ToolValidator.validate(sanitized, schema)
        if not validation.valid:
            raise ValueError(validation.error or "tool validation failed")
        finalized_json = _canonical_json(sanitized)
        finalized_arguments = json.loads(finalized_json)
        finalized_hash = hash_request(
            {
                "tool_name": request.tool_name,
                "operation": request.operation,
                "target": request.target,
                "arguments": finalized_arguments,
            }
        )
        return PreparedToolCall(
            request=request,
            arguments_json=finalized_json,
            request_hash=finalized_hash,
            intent=request.intent_for_hash(finalized_hash),
            redacted_paths=scan.redacted_paths,
        )

    def approval_subject(self, request: ToolRequest, *, schema: Mapping[str, Any]) -> str:
        return self.prepare(request, schema=schema).intent.fingerprint

    def execute(
        self,
        request: ToolRequest,
        *,
        handoff: HandoffArtifact,
        work_contract: WorkContract,
        schema: Mapping[str, Any],
        policy_decision: Decision,
        grant: AuthorizationGrant | None = None,
    ) -> ToolExecutionResult:
        if not isinstance(handoff, HandoffArtifact) or handoff.status is not HandoffStatus.READY:
            return ToolExecutionResult(ToolExecutionStatus.BLOCKED, reason="ready handoff required")

        try:
            prepared = self.prepare(request, schema=schema)
        except (TypeError, ValueError) as exc:
            fallback_hash = hash_request(
                {"tool_name": request.tool_name, "operation": request.operation, "target": request.target}
            )
            intent = request.intent_for_hash(fallback_hash)
            entry = self._log(
                intent,
                status=ActionStatus.BLOCKED,
                result={"reason": str(exc)},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.BLOCKED,
                evidence_entry_id=entry.entry_id,
                reason=str(exc),
            )

        intent = prepared.intent

        if work_contract.forbids(request.operation):
            entry = self._log(
                intent,
                status=ActionStatus.BLOCKED,
                result={"reason": "operation forbidden by WorkContract"},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.BLOCKED,
                evidence_entry_id=entry.entry_id,
                reason="operation forbidden by WorkContract",
            )

        if intent.reversibility is Reversibility.IRREVERSIBLE and not work_contract.irreversible_boundary_declared:
            entry = self._log(
                intent,
                status=ActionStatus.BLOCKED,
                result={"reason": "WorkContract forbidden boundary required for irreversible action"},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.BLOCKED,
                evidence_entry_id=entry.entry_id,
                reason="WorkContract forbidden boundary required for irreversible action",
            )

        source_ok = self._references_verified(handoff.source_refs, expected_kind="source")
        evidence_ok = self._references_verified(handoff.evidence_refs, expected_kind="evidence")
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

        reservation = self._idempotency.reserve(request.idempotency_key, prepared.request_hash)
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
        if reservation.outcome is IdempotencyOutcome.IN_FLIGHT:
            entry = self._log(
                intent,
                status=ActionStatus.UNKNOWN_EXTERNAL_STATE,
                result={"reason": "pending idempotency reservation requires reconciliation"},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE,
                evidence_entry_id=entry.entry_id,
                reason="pending reservation; reconcile before retry",
            )
        if reservation.outcome is IdempotencyOutcome.REPLAY:
            entry = self._log(
                intent,
                status=ActionStatus.REPLAYED,
                result={"result_ref": reservation.result_ref, "replayed": True},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.REPLAYED,
                evidence_entry_id=entry.entry_id,
                result_ref=reservation.result_ref,
                reason="completed action replayed without side effect",
            )

        try:
            result = self._adapter.execute(
                tool_name=request.tool_name,
                operation=request.operation,
                target=request.target,
                arguments=prepared.arguments,
            )
        except Exception as exc:
            entry = self._log(
                intent,
                status=ActionStatus.UNKNOWN_EXTERNAL_STATE,
                result={"error_type": type(exc).__name__, "error": str(exc)},
                handoff=handoff,
                grant=grant,
            )
            return ToolExecutionResult(
                ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE,
                evidence_entry_id=entry.entry_id,
                reason="adapter outcome unknown; reconcile before retry",
            )

        result_ref = "result:" + hash_request(result).split(":", 1)[1]
        try:
            self._idempotency.complete(request.idempotency_key, result_ref=result_ref)
        except Exception:
            return ToolExecutionResult(
                ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE,
                result=result,
                reason="external action returned but completion persistence failed; reconcile before retry",
            )

        try:
            entry = self._log(
                intent,
                status=ActionStatus.CONFIRMED_SUCCEEDED,
                result=result,
                handoff=handoff,
                grant=grant,
            )
        except Exception:
            return ToolExecutionResult(
                ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE,
                result=result,
                result_ref=result_ref,
                reason="action completed but success evidence could not be recorded; reconcile ledger",
            )

        return ToolExecutionResult(
            ToolExecutionStatus.SUCCEEDED,
            result=result,
            evidence_entry_id=entry.entry_id,
            result_ref=result_ref,
            reason="all gates passed and tool executed once",
        )
