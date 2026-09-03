from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from kubera_innovation.authorization_grant import AuthorizationSigner
from kubera_innovation.constitution import Decision
from kubera_innovation.evidence_ledger import EvidenceLedger
from kubera_innovation.execution_controls import ActionLogger, IdempotencyStore
from kubera_innovation.handoff import HandoffArtifact, HandoffStatus
from kubera_innovation.local_draft_adapter import LocalDraftAdapter
from kubera_innovation.tool_executor import SovereignToolExecutor, ToolExecutionStatus, ToolRequest
from kubera_innovation.work_contract import WorkContract


SCHEMA = {
    "type": "object",
    "properties": {"body": {"type": "string"}},
    "required": ["body"],
    "additionalProperties": False,
}


class LocalDraftDemoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.ledger = EvidenceLedger()
        self.store = IdempotencyStore()
        self.signer = AuthorizationSigner(b"d" * 32)
        self.adapter = LocalDraftAdapter(self.temp.name)
        self.executor = SovereignToolExecutor(
            adapter=self.adapter,
            idempotency_store=self.store,
            action_logger=ActionLogger(self.ledger),
            signer=self.signer,
        )

        source = self.ledger.append(
            run_id="demo",
            stage="verified_source",
            input_value={"source": "owner task"},
            output_value={"verified": True},
            metadata={"reference_kind": "source", "verified": True},
        )
        evidence = self.ledger.append(
            run_id="demo",
            stage="verified_evidence",
            input_value={"brief": "reviewed"},
            output_value={"verified": True},
            metadata={"reference_kind": "evidence", "verified": True},
        )
        self.handoff = HandoffArtifact.create(
            task_id="demo-draft",
            from_agent="brief-builder",
            to_agent="operator",
            objective="Write one local draft for human review.",
            status=HandoffStatus.READY,
            output_summary="Brief prepared.",
            source_refs=(f"evidence:{source.entry_id}",),
            evidence_refs=(f"evidence:{evidence.entry_id}",),
            next_action="Request approval then write via SovereignToolExecutor.",
        )
        self.contract = WorkContract(
            job="Write one local draft.",
            sources=("owner task",),
            judgment="Formatting only.",
            output="Local UTF-8 draft file.",
            forbidden=("send", "publish", "pay", "delete", "sign", "launch"),
        )
        self.request = ToolRequest.create(
            action_id="demo-write",
            run_id="demo",
            actor="operator",
            tool_name="local-draft",
            operation="write_draft",
            target="brief.txt",
            arguments={"body": "Prepared for human review."},
            idempotency_key="demo-write-v1",
        )

    def tearDown(self) -> None:
        self.store.close()
        self.ledger.close()
        self.temp.cleanup()

    def execute(self, *, grant=None):
        return self.executor.execute(
            self.request,
            handoff=self.handoff,
            work_contract=self.contract,
            schema=SCHEMA,
            policy_decision=Decision.REQUIRE_APPROVAL,
            grant=grant,
        )

    def test_task_brief_approval_then_local_draft_and_replay(self):
        before = self.execute()
        self.assertEqual(before.status, ToolExecutionStatus.APPROVAL_REQUIRED)
        self.assertFalse((Path(self.temp.name) / "brief.txt").exists())

        subject = self.executor.approval_subject(self.request, schema=SCHEMA)
        grant = self.signer.issue(scope="execute:write_draft", subject=subject)
        after = self.execute(grant=grant)
        self.assertEqual(after.status, ToolExecutionStatus.SUCCEEDED)
        self.assertEqual(
            (Path(self.temp.name) / "brief.txt").read_text(encoding="utf-8"),
            "Prepared for human review.",
        )

        replay = self.execute(grant=grant)
        self.assertEqual(replay.status, ToolExecutionStatus.REPLAYED)
        self.assertTrue(self.ledger.verify_chain())

    def test_adapter_rejects_path_escape(self):
        with self.assertRaises(ValueError):
            self.adapter.execute(
                tool_name="local-draft",
                operation="write_draft",
                target="../escape.txt",
                arguments={"body": "no"},
            )


if __name__ == "__main__":
    unittest.main()
