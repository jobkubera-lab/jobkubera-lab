from __future__ import annotations

import threading
import unittest

from kubera_innovation.authorization_grant import AuthorizationGrant, AuthorizationSigner
from kubera_innovation.constitution import Decision
from kubera_innovation.evidence_ledger import EvidenceLedger
from kubera_innovation.execution_controls import ActionLogger, IdempotencyOutcome, IdempotencyState, IdempotencyStore
from kubera_innovation.handoff import HandoffArtifact, HandoffStatus
from kubera_innovation.tool_executor import SovereignToolExecutor, ToolExecutionStatus, ToolRequest
from kubera_innovation.work_contract import WorkContract


SCHEMA = {
    "type": "object",
    "properties": {"body": {"type": "string"}, "token": {"type": "string"}},
    "required": ["body"],
    "additionalProperties": False,
}


class RecordingAdapter:
    def __init__(self, *, fail: bool = False) -> None:
        self.calls: list[dict] = []
        self.fail = fail

    def execute(self, *, tool_name, operation, target, arguments):
        self.calls.append({"tool_name": tool_name, "operation": operation, "target": target, "arguments": dict(arguments)})
        if self.fail:
            raise RuntimeError("provider outcome unavailable")
        return {"ok": True, "call": len(self.calls)}


class BlockingAdapter(RecordingAdapter):
    def __init__(self) -> None:
        super().__init__()
        self.started = threading.Event()
        self.release = threading.Event()

    def execute(self, *, tool_name, operation, target, arguments):
        self.calls.append({"tool_name": tool_name, "operation": operation, "target": target, "arguments": dict(arguments)})
        self.started.set()
        self.release.wait(timeout=2)
        return {"ok": True, "call": len(self.calls)}


class ToolExecutorHardeningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = EvidenceLedger()
        source = self.ledger.append(
            run_id="refs-hardening",
            stage="source_verification",
            input_value={"source": "official"},
            output_value={"verified": True},
            metadata={"reference_kind": "source", "verified": True},
        )
        evidence = self.ledger.append(
            run_id="refs-hardening",
            stage="evidence_verification",
            input_value={"evidence": "reviewed"},
            output_value={"verified": True},
            metadata={"reference_kind": "evidence", "verified": True},
        )
        self.source_ref = f"evidence:{source.entry_id}"
        self.evidence_ref = f"evidence:{evidence.entry_id}"
        self.contract = WorkContract(
            job="execute reviewed request",
            sources=("ledger refs",),
            judgment="use exact reviewed payload",
            output="tool result",
            forbidden=("delete", "pay"),
        )
        self.store = IdempotencyStore()
        self.adapter = RecordingAdapter()
        self.signer = AuthorizationSigner(b"h" * 32)
        self.executor = SovereignToolExecutor(
            adapter=self.adapter,
            idempotency_store=self.store,
            action_logger=ActionLogger(self.ledger),
            signer=self.signer,
        )

    def tearDown(self) -> None:
        self.store.close()
        self.ledger.close()

    def handoff(self):
        return HandoffArtifact.create(
            task_id="task-hardening",
            from_agent="researcher",
            to_agent="operator",
            objective="execute a reviewed tool action",
            status=HandoffStatus.READY,
            output_summary="source and evidence prepared",
            source_refs=(self.source_ref,),
            evidence_refs=(self.evidence_ref,),
            next_action="execute only through SovereignToolExecutor",
        )

    def request(self, *, actor="operator", operation="publish", target="example", body="hello", token=None, key="hardening-key"):
        arguments = {"body": body}
        if token is not None:
            arguments["token"] = token
        return ToolRequest.create(
            action_id=f"action-{key}",
            run_id="run-hardening",
            actor=actor,
            tool_name="fake-tool",
            operation=operation,
            target=target,
            arguments=arguments,
            idempotency_key=key,
        )

    def execute(self, request, *, grant=None, executor=None):
        return (executor or self.executor).execute(
            request,
            handoff=self.handoff(),
            work_contract=self.contract,
            schema=SCHEMA,
            policy_decision=Decision.ALLOW,
            grant=grant,
        )

    def grant_for(self, request):
        subject = self.executor.approval_subject(request, schema=SCHEMA)
        return self.signer.issue(scope=f"execute:{request.operation}", subject=subject)

    def test_approval_is_bound_to_final_sanitized_payload(self):
        request = self.request(token="sk-1234567890abcdef", key="sanitized")
        result = self.execute(request, grant=self.grant_for(request))
        self.assertEqual(result.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(self.adapter.calls[0]["arguments"]["token"], "***REDACTED***")

    def test_grant_for_raw_secret_payload_does_not_authorize_sanitized_execution(self):
        request = self.request(token="sk-1234567890abcdef", key="raw-grant")
        raw_hash = request.intent_for_hash(
            __import__("kubera_innovation.execution_controls", fromlist=["hash_request"]).hash_request(
                {"tool_name": request.tool_name, "operation": request.operation, "target": request.target, "arguments": request.arguments}
            )
        )
        grant = self.signer.issue(scope=raw_hash.approval_scope, subject=raw_hash.fingerprint)
        result = self.execute(request, grant=grant)
        self.assertEqual(result.status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_grant_cannot_move_to_different_actor(self):
        original = self.request(actor="operator-a", key="actor-key")
        grant = self.grant_for(original)
        changed = self.request(actor="operator-b", key="actor-key")
        self.assertEqual(self.execute(changed, grant=grant).status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_grant_cannot_move_to_new_idempotency_key(self):
        original = self.request(key="approved-key")
        grant = self.grant_for(original)
        changed = self.request(key="fresh-key")
        self.assertEqual(self.execute(changed, grant=grant).status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_grant_cannot_move_to_different_target(self):
        original = self.request(target="target-a", key="target-key")
        grant = self.grant_for(original)
        changed = self.request(target="target-b", key="target-key")
        self.assertEqual(self.execute(changed, grant=grant).status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_grant_cannot_authorize_modified_arguments(self):
        original = self.request(body="approved", key="payload-key")
        grant = self.grant_for(original)
        changed = self.request(body="changed", key="payload-key")
        self.assertEqual(self.execute(changed, grant=grant).status, ToolExecutionStatus.BLOCKED)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_pending_reservation_never_reexecutes_tool(self):
        request = self.request(operation="draft", key="pending")
        prepared = self.executor.prepare(request, schema=SCHEMA)
        first = self.store.reserve(request.idempotency_key, prepared.request_hash)
        self.assertEqual(first.outcome, IdempotencyOutcome.NEW)
        self.assertEqual(first.state, IdempotencyState.PENDING)
        result = self.execute(request)
        self.assertEqual(result.status, ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE)
        self.assertEqual(len(self.adapter.calls), 0)

    def test_adapter_exception_enters_unknown_state_and_retry_does_not_repeat(self):
        failing = RecordingAdapter(fail=True)
        executor = SovereignToolExecutor(adapter=failing, idempotency_store=self.store, action_logger=ActionLogger(self.ledger), signer=self.signer)
        request = self.request(operation="draft", key="exception")
        first = self.execute(request, executor=executor)
        second = self.execute(request, executor=executor)
        self.assertEqual(first.status, ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE)
        self.assertEqual(second.status, ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE)
        self.assertEqual(len(failing.calls), 1)

    def test_two_concurrent_same_key_requests_make_one_external_call(self):
        blocking = BlockingAdapter()
        executor = SovereignToolExecutor(adapter=blocking, idempotency_store=self.store, action_logger=ActionLogger(self.ledger), signer=self.signer)
        request = self.request(operation="draft", key="concurrent")
        results: list = []

        def run_first():
            results.append(self.execute(request, executor=executor))

        thread = threading.Thread(target=run_first)
        thread.start()
        self.assertTrue(blocking.started.wait(timeout=1))
        second = self.execute(request, executor=executor)
        blocking.release.set()
        thread.join(timeout=2)
        self.assertEqual(len(blocking.calls), 1)
        self.assertEqual(second.status, ToolExecutionStatus.UNKNOWN_EXTERNAL_STATE)
        self.assertEqual(results[0].status, ToolExecutionStatus.SUCCEEDED)

    def test_mutating_original_arguments_after_creation_does_not_change_execution(self):
        original = {"body": "approved"}
        request = ToolRequest.create(
            action_id="immutable",
            run_id="run-hardening",
            actor="operator",
            tool_name="fake-tool",
            operation="draft",
            target="example",
            arguments=original,
            idempotency_key="immutable",
        )
        original["body"] = "mutated"
        result = self.execute(request)
        self.assertEqual(result.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(self.adapter.calls[0]["arguments"]["body"], "approved")

    def test_completed_reservation_replays_with_complete_state(self):
        request = self.request(operation="draft", key="complete-state")
        first = self.execute(request)
        prepared = self.executor.prepare(request, schema=SCHEMA)
        replay = self.store.reserve(request.idempotency_key, prepared.request_hash)
        self.assertEqual(first.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(replay.outcome, IdempotencyOutcome.REPLAY)
        self.assertEqual(replay.state, IdempotencyState.COMPLETE)
        self.assertIsNotNone(replay.result_ref)

    def test_evidence_ledger_concurrent_appends_keep_chain_valid(self):
        errors: list[Exception] = []

        def append(index: int):
            try:
                self.ledger.append(run_id="run-ledger", stage="concurrent", input_value={"index": index}, output_value={"ok": True})
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=append, args=(index,)) for index in range(12)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=2)
        self.assertEqual(errors, [])
        self.assertEqual(len(self.ledger.entries("run-ledger")), 12)
        self.assertTrue(self.ledger.verify_chain())

    def test_malformed_authorization_grant_fails_closed(self):
        malformed = AuthorizationGrant(
            grant_id="bad", scope="execute:publish", subject="subject",
            issued_at="not-a-date", expires_at="also-not-a-date", signature="bad-signature",
        )
        self.assertFalse(self.signer.verify(malformed, required_scope="execute:publish", subject="subject"))

    def test_adapter_receives_only_tool_fields_and_final_arguments(self):
        request = self.request(operation="draft", token="Bearer abcdefghijklmnop", key="adapter-shape")
        result = self.execute(request)
        self.assertEqual(result.status, ToolExecutionStatus.SUCCEEDED)
        call = self.adapter.calls[0]
        self.assertEqual(set(call), {"tool_name", "operation", "target", "arguments"})
        self.assertNotIn("grant", call)
        self.assertNotIn("signer", call)
        self.assertEqual(call["arguments"]["token"], "***REDACTED***")


if __name__ == "__main__":
    unittest.main()
