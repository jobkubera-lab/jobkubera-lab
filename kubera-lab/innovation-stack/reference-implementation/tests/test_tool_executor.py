from __future__ import annotations

import unittest

from kubera_innovation.authorization_grant import AuthorizationSigner
from kubera_innovation.constitution import Decision
from kubera_innovation.evidence_ledger import EvidenceLedger
from kubera_innovation.execution_controls import ActionLogger, IdempotencyStore, Reversibility
from kubera_innovation.handoff import HandoffArtifact, HandoffStatus
from kubera_innovation.tool_executor import (
    SovereignToolExecutor,
    ToolExecutionStatus,
    ToolRequest,
)


SCHEMA = {
    "type": "object",
    "properties": {
        "body": {"type": "string"},
        "token": {"type": "string"},
    },
    "required": ["body"],
    "additionalProperties": False,
}


class FakeAdapter:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def execute(self, *, tool_name, operation, target, arguments):
        snapshot = {
            "tool_name": tool_name,
            "operation": operation,
            "target": target,
            "arguments": dict(arguments),
        }
        self.calls.append(snapshot)
        return {"ok": True, "call": len(self.calls)}


class ToolExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = EvidenceLedger()
        self.store = IdempotencyStore()
        self.adapter = FakeAdapter()
        self.signer = AuthorizationSigner(b"s" * 32)
        self.executor = SovereignToolExecutor(
            adapter=self.adapter,
            idempotency_store=self.store,
            action_logger=ActionLogger(self.ledger),
            signer=self.signer,
        )

    def tearDown(self) -> None:
        self.store.close()
        self.ledger.close()

    def handoff(self, *, sources=("source:official",), evidence=("evidence:verified",)):
        return HandoffArtifact.create(
            task_id="task-1",
            from_agent="researcher",
            to_agent="operator",
            objective="prepare controlled tool action",
            status=HandoffStatus.READY,
            output_summary="verified inputs prepared",
            source_refs=sources,
            evidence_refs=evidence,
            next_action="execute through SovereignToolExecutor",
        )

    def request(
        self,
        *,
        operation="draft",
        body="hello",
        key="key-1",
        target="example",
        token=None,
    ):
        args = {"body": body}
        if token is not None:
            args["token"] = token
        return ToolRequest.create(
            action_id=f"action-{key}",
            run_id="run-1",
            actor="operator",
            tool_name="fake-tool",
            operation=operation,
            target=target,
            arguments=args,
            idempotency_key=key,
        )

    def execute(self, request, *, handoff=None, source_verified=True, evidence_verified=True, grant=None):
        return self.executor.execute(
            request,
            handoff=handoff or self.handoff(),
            schema=SCHEMA,
            source_verified=source_verified,
            evidence_verified=evidence_verified,
            policy_decision=Decision.ALLOW,
            grant=grant,
        )

    def test_no_source_means_tool_not_called(self):
        result = self.execute(
            self.request(),
            handoff=self.handoff(sources=()),
            source_verified=False,
        )
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_no_evidence_means_tool_not_called(self):
        result = self.execute(
            self.request(),
            handoff=self.handoff(evidence=()),
            evidence_verified=False,
        )
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_irreversible_operations_without_approval_never_call_tool(self):
        for index, operation in enumerate(("send", "publish", "pay", "delete", "sign"), start=1):
            with self.subTest(operation=operation):
                result = self.execute(self.request(operation=operation, key=f"irreversible-{index}"))
                self.assertEqual(result.status, ToolExecutionStatus.APPROVAL_REQUIRED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_exact_signed_approval_allows_irreversible_action_once(self):
        request = self.request(operation="publish", key="approved")
        intent = request.to_intent()
        grant = self.signer.issue(scope=intent.approval_scope, subject=intent.fingerprint)
        result = self.execute(request, grant=grant)
        self.assertEqual(result.status, ToolExecutionStatus.EXECUTED)
        self.assertEqual(len(self.adapter.calls), 1)

    def test_same_idempotency_key_same_request_replays_with_one_call(self):
        request = self.request(operation="draft", key="replay")
        first = self.execute(request)
        second = self.execute(request)
        self.assertEqual(first.status, ToolExecutionStatus.EXECUTED)
        self.assertEqual(second.status, ToolExecutionStatus.REPLAYED)
        self.assertEqual(len(self.adapter.calls), 1)

    def test_same_key_different_request_conflicts_without_second_call(self):
        first = self.execute(self.request(operation="draft", body="one", key="collision"))
        second = self.execute(self.request(operation="draft", body="two", key="collision"))
        self.assertEqual(first.status, ToolExecutionStatus.EXECUTED)
        self.assertEqual(second.status, ToolExecutionStatus.CONFLICT)
        self.assertEqual(len(self.adapter.calls), 1)

    def test_secret_is_redacted_before_adapter_sees_arguments(self):
        result = self.execute(
            self.request(operation="draft", key="privacy", token="sk-1234567890abcdef")
        )
        self.assertEqual(result.status, ToolExecutionStatus.EXECUTED)
        self.assertEqual(self.adapter.calls[0]["arguments"]["token"], "***REDACTED***")

    def test_invalid_schema_never_reaches_adapter(self):
        request = ToolRequest.create(
            action_id="bad-schema",
            run_id="run-1",
            actor="operator",
            tool_name="fake-tool",
            operation="draft",
            target="example",
            arguments={"unexpected": "value"},
            idempotency_key="bad-schema",
            reversibility=Reversibility.REVERSIBLE,
        )
        result = self.execute(request)
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_non_ready_handoff_never_reaches_adapter(self):
        blocked_handoff = HandoffArtifact.create(
            task_id="task-2",
            from_agent="researcher",
            to_agent="operator",
            objective="blocked task",
            status=HandoffStatus.BLOCKED,
            output_summary="not ready",
            source_refs=("source:official",),
            evidence_refs=("evidence:verified",),
            next_action="stop",
        )
        result = self.execute(self.request(key="handoff"), handoff=blocked_handoff)
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_success_and_replay_keep_evidence_chain_valid(self):
        request = self.request(key="ledger")
        self.execute(request)
        self.execute(request)
        self.assertTrue(self.ledger.verify_chain())
        self.assertGreaterEqual(len(self.ledger.entries("run-1")), 2)


if __name__ == "__main__":
    unittest.main()
