import unittest

from agent_fabric import (
    ActionIntent,
    Evidence,
    Fabric,
    Risk,
    Status,
    WorkerResult,
)


class FabricTests(unittest.TestCase):
    def test_worker_budget_is_enforced(self):
        fabric = Fabric(max_workers=1)

        def worker(job):
            return WorkerResult("w", job, [Evidence("s", "c")])

        with self.assertRaises(ValueError):
            fabric.run_collect(["a", "b"], worker)

    def test_external_write_requires_approval_flag(self):
        intent = ActionIntent(
            agent="publisher",
            action="publish",
            target="x://post/1",
            risk=Risk.EXTERNAL_WRITE,
            evidence=[Evidence("official", "verified")],
            confidence=0.9,
            approval_required=False,
        )
        with self.assertRaises(ValueError):
            intent.validate()

    def test_external_write_cannot_execute_before_human_approval(self):
        fabric = Fabric()
        intent = ActionIntent(
            agent="publisher",
            action="publish",
            target="x://post/1",
            risk=Risk.EXTERNAL_WRITE,
            evidence=[Evidence("official", "verified")],
            confidence=0.9,
            approval_required=True,
        )
        fabric.propose_action(intent)
        self.assertEqual(intent.status, Status.VERIFIED)
        with self.assertRaises(PermissionError):
            fabric.execute(intent, lambda _: {"ok": True})

    def test_approved_external_write_executes_and_is_logged(self):
        fabric = Fabric()
        intent = ActionIntent(
            agent="publisher",
            action="publish",
            target="x://post/1",
            risk=Risk.EXTERNAL_WRITE,
            evidence=[Evidence("official", "verified")],
            confidence=0.9,
            approval_required=True,
        )
        fabric.propose_action(intent)
        fabric.approve(intent, True)
        receipt = fabric.execute(intent, lambda _: {"post_id": "1"})
        self.assertEqual(receipt["post_id"], "1")
        self.assertEqual(intent.status, Status.EXECUTED)
        self.assertTrue(fabric.ledger.verify_chain())

    def test_verifier_filters_untrusted_findings(self):
        fabric = Fabric()
        results = [
            WorkerResult("a", "primary", [Evidence("official", "claim")]),
            WorkerResult("b", "rumor", [Evidence("unknown", "claim")]),
        ]
        accepted = fabric.verify(
            results,
            lambda result: result.evidence[0].source == "official",
        )
        self.assertEqual([r.finding for r in accepted], ["primary"])
        self.assertTrue(fabric.ledger.verify_chain())


if __name__ == "__main__":
    unittest.main()
