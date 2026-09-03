from __future__ import annotations

import json
from pathlib import Path

from kubera_innovation.authorization_grant import AuthorizationSigner
from kubera_innovation.constitution import Decision
from kubera_innovation.evidence_ledger import EvidenceLedger
from kubera_innovation.execution_controls import ActionLogger, IdempotencyStore
from kubera_innovation.handoff import HandoffArtifact, HandoffStatus
from kubera_innovation.local_draft_adapter import LocalDraftAdapter
from kubera_innovation.tool_executor import SovereignToolExecutor, ToolRequest
from kubera_innovation.work_contract import WorkContract


SCHEMA = {
    "type": "object",
    "properties": {"body": {"type": "string"}},
    "required": ["body"],
    "additionalProperties": False,
}


def _verified_ref(ledger: EvidenceLedger, *, run_id: str, kind: str, value: str) -> str:
    entry = ledger.append(
        run_id=run_id,
        stage=f"verified_{kind}",
        input_value={"value": value},
        output_value={"verified": True},
        metadata={"reference_kind": kind, "verified": True},
    )
    return f"evidence:{entry.entry_id}"


def run_demo(output_dir: str | Path = "demo-output") -> dict:
    """Run task -> brief -> approval -> local draft through SovereignToolExecutor."""
    run_id = "operator-demo"
    ledger = EvidenceLedger()
    store = IdempotencyStore()
    signer = AuthorizationSigner(b"demo-signing-secret-for-reference-only"[:32])
    adapter = LocalDraftAdapter(output_dir)
    executor = SovereignToolExecutor(
        adapter=adapter,
        idempotency_store=store,
        action_logger=ActionLogger(ledger),
        signer=signer,
    )

    try:
        source_ref = _verified_ref(
            ledger,
            run_id=run_id,
            kind="source",
            value="demo:owner-provided-task",
        )
        evidence_ref = _verified_ref(
            ledger,
            run_id=run_id,
            kind="evidence",
            value="demo:brief-reviewed",
        )

        handoff = HandoffArtifact.create(
            task_id="demo-draft",
            from_agent="brief-builder",
            to_agent="operator",
            objective="Create a local draft file only after explicit approval.",
            status=HandoffStatus.READY,
            output_summary="Draft text prepared and source/evidence references verified.",
            source_refs=(source_ref,),
            evidence_refs=(evidence_ref,),
            next_action="Request approval, then write the local draft through SovereignToolExecutor.",
        )

        contract = WorkContract(
            job="Prepare one local draft file for human review.",
            sources=("owner-provided task", "verified ledger evidence"),
            judgment="May format the supplied brief; may not send or publish it.",
            output="A UTF-8 local draft file for human review.",
            forbidden=("send", "publish", "pay", "delete", "sign", "launch", "accept terms"),
        )

        request = ToolRequest.create(
            action_id="demo-write-draft",
            run_id=run_id,
            actor="operator",
            tool_name="local-draft",
            operation="write_draft",
            target="customer-brief.txt",
            arguments={
                "body": "KUBERA demo brief\n\nPrepared for human review. Nothing was sent or published.\n"
            },
            idempotency_key="demo-write-draft-v1",
        )

        before_approval = executor.execute(
            request,
            handoff=handoff,
            work_contract=contract,
            schema=SCHEMA,
            policy_decision=Decision.REQUIRE_APPROVAL,
        )

        subject = executor.approval_subject(request, schema=SCHEMA)
        grant = signer.issue(scope="execute:write_draft", subject=subject)

        after_approval = executor.execute(
            request,
            handoff=handoff,
            work_contract=contract,
            schema=SCHEMA,
            policy_decision=Decision.REQUIRE_APPROVAL,
            grant=grant,
        )

        replay = executor.execute(
            request,
            handoff=handoff,
            work_contract=contract,
            schema=SCHEMA,
            policy_decision=Decision.REQUIRE_APPROVAL,
            grant=grant,
        )

        return {
            "before_approval": before_approval.status.value,
            "after_approval": after_approval.status.value,
            "replay": replay.status.value,
            "draft_file": str((adapter.root / "customer-brief.txt").resolve()),
            "ledger_valid": ledger.verify_chain(),
        }
    finally:
        store.close()
        ledger.close()


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2))
