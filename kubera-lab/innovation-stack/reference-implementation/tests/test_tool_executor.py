from __future__ import annotations

from dataclasses import FrozenInstanceError
import unittest

from kubera_innovation.authorization_grant import AuthorizationSigner
from kubera_innovation.constitution import Decision
from kubera_innovation.evidence_ledger import EvidenceLedger
from kubera_innovation.execution_controls import ActionLogger, IdempotencyOutcome, IdempotencyStore
from kubera_innovation.handoff import HandoffArtifact, HandoffStatus
from kubera_innovation.tool_executor import SovereignToolExecutor, ToolExecutionStatus, ToolRequest
from kubera_innovation.work_contract import WorkContract


SCHEMA = {
    "type": "object",
    "properties": {
        "body": {"type": "string"},
        "token": {"type": "string"},
    },
    "required": ["body"],
    "additionalProperties": False,
}


class FakeToolAdapter:
    def __init__(self, *, mutate: bool = False, fail: bool = False) -> None:
        self.calls: list[dict] = []
        self.mutate = mutate
        self.fail = fail

    def execute(self, *, tool_name, operation, target, arguments):
        snapshot = {
            "tool_name": tool_name,
            "operation": operation,
            "target": target,
            "arguments": dict(arguments),
        }
        self.calls.append(snapshot)
        if self.mutate:
            arguments["body"] = "adapter-mutated"
        if self.fail:
            raise RuntimeError("external outcome unavailable")
        return {"ok": True, "call": len(self.calls)}


class ToolExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = EvidenceLedger()
        self.source_entry = self.ledger.append(
            run_id="refs",
            stage="source_verification",
            input_value={"url": "https://example.invalid/source"},
            output_value={"verified": True},
            metadata={"reference_kind": "source", "verified": True},
        )
        self.evidence_entry = self.ledger.append(
            run_id="refs",
            stage="evidence_verification",
            input_value={"claim": "prepared"},
            output_value={"verified": True},
            metadata={"reference_kind": "evidence", "verified": True},
        )
        self.source_ref = f"evidence:{self.source_entry.entry_id}"
        self.evidence_ref = f"evidence:{self.evidence_entry.entry_id}"
        self.store = IdempotencyStore()
        self.adapter = FakeToolAdapter()
        self.signer = AuthorizationSigner(b"s" * 32)
        self.executor = SovereignToolExecutor(
            adapter=self.adapter,
            idempotency_store=self.store,
            action_logger=ActionLogger(self.ledger),
            signer=self.signer,
        )
        self.contract = WorkContract(
            job="prepare and execute one reviewed tool action",
            sources=("verified ledger references only",),
            judgment="apply the approved operation to the approved target",
            output="structured tool result",
            forbidden=("delete", "pay"),
        )

    def tearDown(self) -> None:
        self.store.close()
        self.ledger.close()

    def handoff(self, *, sources=None, evidence=None, status=HandoffStatus.READY):
        return HandoffArtifact.create(
            task_id="task-1",
            from_agent="researcher",
            to_agent="operator",
            objective="prepare controlled tool action",
            status=status,
            output_summary="verified inputs prepared",
            source_refs=tuple(sources if sources is not None else (self.source_ref,)),
            evidence_refs=tuple(evidence if evidence is not None else (self.evidence_ref,)),
            next_action="execute only through SovereignToolExecutor",
        )

    def request(self, *, operation="draft", body="hello", key="key-1", target="example", token=None):
        arguments = {"body": body}
        if token is not None:
            arguments["token"] = token
        return ToolRequest.create(
            action_id=f"action-{key}",
            run_id="run-1",
            actor="operator",
            tool_name="fake-tool",
            operation=operation,
            target=target,
            arguments=arguments,
            idempotency_key=key,
        )

    def execute(self, request, *, handoff=None, grant=None, policy=Decision.ALLOW, contract=None, executor=None):
        return (executor or self.executor).execute(
            request,
            handoff=handoff or self.handoff(),
            work_contract=contract or self.contract,
            schema=SCHEMA,
            policy_decision=policy,
            grant=grant,
        )

    def grant_for(self, request):
        subject = self.executor.approval_subject(request, schema=SCHEMA)
        return self.signer.issue(scope=f"execute:{request.operation}", subject=subject)

    def test_reversible_allowed_adapter_one(self):
        result = self.execute(self.request(operation="draft", key="reversible"))
        self.assertEqual(result.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(len(self.adapter.calls), 1)

    def test_irreversible_no_grant_adapter_zero(self):
        result = self.execute(self.request(operation="publish", key="no-grant"))
        self.assertEqual(result.status, ToolExecutionStatus.APPROVAL_REQUIRED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_policy_allow_irreversible_without_grant_is_still_blocked_from_tool(self):
        result = self.execute(self.request(operation="sign", key="policy-allow"), policy=Decision.ALLOW)
        self.assertEqual(result.status, ToolExecutionStatus.APPROVAL_REQUIRED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_exact_grant_adapter_one(self):
        request = self.request(operation="publish", key="exact-grant")
        result = self.execute(request, grant=self.grant_for(request))
        self.assertEqual(result.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(len(self.adapter.calls), 1)

    def test_modified_args_after_grant_adapter_zero(self):
        approved = self.request(operation="publish", body="approved", key="mutated")
        grant = self.grant_for(approved)
        changed = self.request(operation="publish", body="changed", key="mutated")
        result = self.execute(changed, grant=grant)
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_missing_source_ref_adapter_zero(self):
        result = self.execute(
            self.request(key="missing-source"),
            handoff=self.handoff(sources=("evidence:not-present",)),
        )
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_missing_evidence_ref_adapter_zero(self):
        result = self.execute(
            self.request(key="missing-evidence"),
            handoff=self.handoff(evidence=("evidence:not-present",)),
        )
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_secret_redacted_before_adapter(self):
        result = self.execute(self.request(key="privacy", token="sk-1234567890abcdef"))
        self.assertEqual(result.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(self.adapter.calls[0]["arguments"]["token"], "***REDACTED***")

    def test_schema_extra_field_blocked(self):
        request = ToolRequest.create(
            action_id="bad-schema",
            run_id="run-1",
            actor="operator",
            tool_name="fake-tool",
            operation="draft",
            target="example",
            arguments={"body": "ok", "extra": "blocked"},
            idempotency_key="bad-schema",
        )
        result = self.execute(request)
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_replay_after_complete_adapter_still_one(self):
        request = self.request(key="replay")
        first = self.execute(request)
        second = self.execute(request)
        self.assertEqual(first.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(second.status, ToolExecutionStatus.REPLAYED)
        self.assertEqual(len(self.adapter.calls), 1)

    def test_same_key_different_fingerprint_conflict_no_second_call(self):
        first = self.execute(self.request(body="one", key="collision"))
        second = self.execute(self.request(body="two", key="collision"))
        self.assertEqual(first.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(second.status, ToolExecutionStatus.CONFLICT)
        self.assertEqual(len(self.adapter.calls), 1)

    def test_pending_then_second_submit_unknown_adapter_zero(self):
        request = self.request(key="pending")
        prepared = self.executor.prepare(request, schema=SCHEMA)
        reservation = self.store.reserve(request.idempotency_key, prepared.request_hash)
        self.assertEqual(reservation.outcome, IdempotencyOutcome.NEW)
        result = self.execute(request)
        self.assertEqual(result.status, ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_blocked_writes_blocked_not_success_status(self):
        self.execute(
            self.request(key="blocked-log"),
            handoff=self.handoff(sources=("evidence:missing",)),
        )
        action_entries = [entry for entry in self.ledger.entries("run-1") if entry.metadata.get("event_type") == "action"]
        self.assertTrue(action_entries)
        self.assertEqual(action_entries[-1].metadata["status"], "BLOCKED")
        self.assertNotEqual(action_entries[-1].metadata["status"], "CONFIRMED_SUCCEEDED")

    def test_request_is_frozen_and_adapter_mutation_does_not_change_it(self):
        request = self.request(body="original", key="frozen")
        with self.assertRaises(FrozenInstanceError):
            request.target = "changed"
        mutating = FakeToolAdapter(mutate=True)
        executor = SovereignToolExecutor(
            adapter=mutating,
            idempotency_store=self.store,
            action_logger=ActionLogger(self.ledger),
            signer=self.signer,
        )
        result = self.execute(request, executor=executor)
        self.assertEqual(result.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(request.arguments["body"], "original")

    def test_signer_not_passed_into_adapter(self):
        self.execute(self.request(key="adapter-shape"))
        call = self.adapter.calls[0]
        self.assertEqual(set(call), {"tool_name", "operation", "target", "arguments"})
        self.assertNotIn("signer", call)
        self.assertNotIn("grant", call)

    def test_empty_forbidden_contract_fails_closed_for_irreversible(self):
        unsafe_contract = WorkContract(
            job="publish",
            sources=("verified ledger references only",),
            judgment="prepare approved content",
            output="publication result",
            forbidden=(),
        )
        request = self.request(operation="publish", key="empty-forbidden")
        result = self.execute(request, contract=unsafe_contract)
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_adapter_exception_then_retry_never_blind_reexecutes(self):
        failing = FakeToolAdapter(fail=True)
        executor = SovereignToolExecutor(
            adapter=failing,
            idempotency_store=self.store,
            action_logger=ActionLogger(self.ledger),
            signer=self.signer,
        )
        request = self.request(key="exception")
        first = self.execute(request, executor=executor)
        second = self.execute(request, executor=executor)
        self.assertEqual(first.status, ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE)
        self.assertEqual(second.status, ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE)
        self.assertEqual(len(failing.calls), 1)

    def test_success_is_confirmed_in_canonical_ledger(self):
        result = self.execute(self.request(key="confirmed"))
        self.assertEqual(result.status, ToolExecutionStatus.SUCCEEDED)
        action_entries = [entry for entry in self.ledger.entries("run-1") if entry.metadata.get("event_type") == "action"]
        self.assertEqual(action_entries[-1].metadata["status"], "CONFIRMED_SUCCEEDED")
        self.assertTrue(self.ledger.verify_chain())


if __name__ == "__main__":
    unittest.main()
