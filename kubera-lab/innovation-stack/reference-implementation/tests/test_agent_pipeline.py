import unittest

from kubera_innovation.agent_pipeline import (
    DeterministicAgentPipeline,
    PipelineVerdict,
    StageResult,
)
from kubera_innovation.evidence_ledger import EvidenceLedger


def builder(request):
    return StageResult({"artifact": request["idea"].upper()})


def critic_pass(request, built):
    return StageResult({"reviewed": built.content["artifact"]})


def critic_changes(request, built):
    return StageResult(
        {"reviewed": built.content["artifact"]},
        verdict=PipelineVerdict.NEEDS_CHANGES,
        findings=("add acceptance criteria",),
    )


def critic_block(request, built):
    return StageResult({"reason": "policy"}, verdict=PipelineVerdict.BLOCKED)


def verifier_pass(request, built, critique):
    return StageResult({"verified": True})


def verifier_changes(request, built, critique):
    return StageResult({"verified": False}, verdict=PipelineVerdict.NEEDS_CHANGES)


class AgentPipelineTests(unittest.TestCase):
    def setUp(self):
        self.ledger = EvidenceLedger()

    def tearDown(self):
        self.ledger.close()

    def test_happy_path_has_three_evidence_entries(self):
        pipeline = DeterministicAgentPipeline(builder=builder, critic=critic_pass, verifier=verifier_pass, ledger=self.ledger)
        result = pipeline.run({"idea": "test"}, run_id="run-1")
        self.assertEqual(result.verdict, PipelineVerdict.PASS)
        self.assertEqual(result.evidence_entries, 3)
        self.assertTrue(result.evidence_chain_valid)

    def test_critic_changes_propagate(self):
        pipeline = DeterministicAgentPipeline(builder=builder, critic=critic_changes, verifier=verifier_pass, ledger=self.ledger)
        result = pipeline.run({"idea": "test"})
        self.assertEqual(result.verdict, PipelineVerdict.NEEDS_CHANGES)

    def test_verifier_changes_propagate(self):
        pipeline = DeterministicAgentPipeline(builder=builder, critic=critic_pass, verifier=verifier_changes, ledger=self.ledger)
        result = pipeline.run({"idea": "test"})
        self.assertEqual(result.verdict, PipelineVerdict.NEEDS_CHANGES)

    def test_critic_block_skips_real_verifier(self):
        called = {"value": False}
        def verifier(request, built, critique):
            called["value"] = True
            return StageResult({"verified": True})
        pipeline = DeterministicAgentPipeline(builder=builder, critic=critic_block, verifier=verifier, ledger=self.ledger)
        result = pipeline.run({"idea": "test"})
        self.assertFalse(called["value"])
        self.assertEqual(result.verdict, PipelineVerdict.BLOCKED)
        self.assertEqual(result.verifier.content["reason"], "critic_blocked")

    def test_empty_request_rejected(self):
        pipeline = DeterministicAgentPipeline(builder=builder, critic=critic_pass, verifier=verifier_pass, ledger=self.ledger)
        with self.assertRaises(ValueError):
            pipeline.run({})

    def test_stage_output_is_machine_readable(self):
        payload = StageResult({"x": 1}, findings=("f1",)).to_payload()
        self.assertEqual(payload["verdict"], "pass")
        self.assertEqual(payload["findings"], ["f1"])


if __name__ == "__main__":
    unittest.main()
