from __future__ import annotations

import unittest

from kubera_innovation.authorization_grant import AuthorizationSigner
from kubera_innovation.constitution import Decision
from kubera_innovation.evidence_ledger import EvidenceLedger
from kubera_innovation.execution_controls import (
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


class ExecutionControlTests(unittest.TestCase):
    def intent(self, reversibility: Reversibility = Reversibility.REVERSIBLE) -> ActionIntent:
        return ActionIntent(
            action_id="a-1",
            run_id="r-1",
            actor="publisher",
            operation="publish",
            target="example",
            request_hash=hash_request({"body": "hello"}),
            reversibility=reversibility,
            idempotency_key="publish:example:1",
        )

    def test_source_gate_fails_closed(self) -> None:
        result = SourceEvidenceActionGate().evaluate(
            self.intent(), source_verified=False, evidence_verified=True, policy_decision=Decision.ALLOW
        )
        self.assertEqual(result.outcome, GateOutcome.BLOCK)

    def test_evidence_gate_fails_closed(self) -> None:
        result = SourceEvidenceActionGate().evaluate(
            self.intent(), source_verified=True, evidence_verified=False, policy_decision=Decision.ALLOW
        )
        self.assertEqual(result.outcome, GateOutcome.BLOCK)

    def test_reversible_allowed_when_policy_allows(self) -> None:
        result = SourceEvidenceActionGate().evaluate(
            self.intent(), source_verified=True, evidence_verified=True, policy_decision=Decision.ALLOW
        )
        self.assertTrue(result.allowed)

    def test_irreversible_requires_approval_even_when_policy_allows(self) -> None:
        result = SourceEvidenceActionGate().evaluate(
            self.intent(Reversibility.IRREVERSIBLE),
            source_verified=True,
            evidence_verified=True,
            policy_decision=Decision.ALLOW,
        )
        self.assertTrue(result.requires_approval)

    def test_signed_grant_is_bound_to_exact_action(self) -> None:
        signer = AuthorizationSigner(b"x" * 32)
        intent = self.intent(Reversibility.IRREVERSIBLE)
        grant = signer.issue(scope=intent.approval_scope, subject=intent.fingerprint)
        result = SourceEvidenceActionGate().evaluate(
            intent,
            source_verified=True,
            evidence_verified=True,
            policy_decision=Decision.ALLOW,
            grant=grant,
            signer=signer,
        )
        self.assertTrue(result.allowed)

        changed = ActionIntent(
            action_id=intent.action_id,
            run_id=intent.run_id,
            actor=intent.actor,
            operation=intent.operation,
            target=intent.target,
            request_hash=hash_request({"body": "changed"}),
            reversibility=intent.reversibility,
            idempotency_key=intent.idempotency_key,
        )
        denied = SourceEvidenceActionGate().evaluate(
            changed,
            source_verified=True,
            evidence_verified=True,
            policy_decision=Decision.ALLOW,
            grant=grant,
            signer=signer,
        )
        self.assertEqual(denied.outcome, GateOutcome.BLOCK)

    def test_policy_denial_cannot_be_overridden_by_grant(self) -> None:
        signer = AuthorizationSigner(b"x" * 32)
        intent = self.intent(Reversibility.IRREVERSIBLE)
        grant = signer.issue(scope=intent.approval_scope, subject=intent.fingerprint)
        result = SourceEvidenceActionGate().evaluate(
            intent,
            source_verified=True,
            evidence_verified=True,
            policy_decision=Decision.DENY,
            grant=grant,
            signer=signer,
        )
        self.assertEqual(result.outcome, GateOutcome.BLOCK)

    def test_idempotent_retry_replays_instead_of_reserving_again(self) -> None:
        store = IdempotencyStore()
        try:
            request_hash = hash_request({"x": 1})
            first = store.reserve("k", request_hash)
            self.assertEqual(first.outcome, IdempotencyOutcome.NEW)
            store.complete("k", result_ref="evidence:123")
            retry = store.reserve("k", request_hash)
            self.assertEqual(retry.outcome, IdempotencyOutcome.REPLAY)
            self.assertEqual(retry.result_ref, "evidence:123")
        finally:
            store.close()

    def test_idempotency_key_reuse_with_different_request_is_conflict(self) -> None:
        store = IdempotencyStore()
        try:
            store.reserve("k", hash_request({"x": 1}))
            conflict = store.reserve("k", hash_request({"x": 2}))
            self.assertEqual(conflict.outcome, IdempotencyOutcome.CONFLICT)
        finally:
            store.close()

    def test_action_log_reuses_hash_chained_evidence_ledger(self) -> None:
        ledger = EvidenceLedger()
        try:
            entry = ActionLogger(ledger).record(
                self.intent(),
                status=ActionStatus.EXECUTED,
                result={"ok": True},
                source_refs=("source:1",),
                evidence_refs=("evidence:1",),
            )
            self.assertEqual(entry.stage, "action_log")
            self.assertEqual(entry.metadata["status"], "EXECUTED")
            self.assertTrue(ledger.verify_chain())
        finally:
            ledger.close()


if __name__ == "__main__":
    unittest.main()
