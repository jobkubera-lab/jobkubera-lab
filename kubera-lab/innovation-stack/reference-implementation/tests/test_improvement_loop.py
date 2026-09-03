import unittest

from kubera_innovation.improvement_loop import (
    AgentState,
    CorrectionSignal,
    ImprovementArtifact,
    ImprovementRegistry,
    PromotionThreshold,
    ProposalStatus,
)


class ImprovementLoopTests(unittest.TestCase):
    def setUp(self):
        self.registry = ImprovementRegistry()

    def tearDown(self):
        self.registry.close()

    def record_three(self, *, same_conversation=False):
        conversations = ["c1", "c1", "c1"] if same_conversation else ["c1", "c2", "c3"]
        for index, conversation_id in enumerate(conversations, start=1):
            self.registry.record_signal(
                CorrectionSignal(
                    signal_id=f"s{index}",
                    conversation_id=conversation_id,
                    fingerprint="protect-root-readme",
                    summary="Do not modify the protected profile README",
                    pain=1,
                )
            )

    def test_signal_validation(self):
        with self.assertRaises(ValueError):
            CorrectionSignal("", "c1", "x", "summary")
        with self.assertRaises(ValueError):
            CorrectionSignal("s1", "c1", "x", "summary", pain=6)

    def test_threshold_validation(self):
        with self.assertRaises(ValueError):
            PromotionThreshold(min_signals=0)

    def test_cluster_summarizes_minimal_signals(self):
        self.record_three()
        stats = self.registry.cluster("protect-root-readme")
        self.assertEqual(stats.signal_count, 3)
        self.assertEqual(stats.conversation_count, 3)
        self.assertEqual(stats.pain_total, 3)
        self.assertEqual(stats.signal_ids, ("s1", "s2", "s3"))

    def test_empty_cluster_is_valid(self):
        stats = self.registry.cluster("unknown")
        self.assertEqual(stats.signal_count, 0)
        with self.assertRaises(ValueError):
            self.registry.cluster(" ")

    def test_duplicate_signal_is_rejected(self):
        signal = CorrectionSignal("s1", "c1", "x", "summary")
        self.registry.record_signal(signal)
        with self.assertRaises(ValueError):
            self.registry.record_signal(signal)

    def test_proposal_waits_for_repeated_evidence(self):
        self.registry.record_signal(CorrectionSignal("s1", "c1", "x", "summary"))
        result = self.registry.maybe_propose(
            "x",
            artifact=ImprovementArtifact.RULE,
            target_path="AGENTS.md",
            proposed_content="Never change protected files.\n",
        )
        self.assertIsNone(result)

    def test_distinct_conversations_are_required(self):
        self.record_three(same_conversation=True)
        result = self.registry.maybe_propose(
            "protect-root-readme",
            artifact=ImprovementArtifact.RULE,
            target_path="AGENTS.md",
            proposed_content="Never change protected files.\n",
        )
        self.assertIsNone(result)

    def test_proposal_is_created_with_evidence(self):
        self.record_three()
        proposal = self.registry.maybe_propose(
            "protect-root-readme",
            artifact=ImprovementArtifact.GATE,
            target_path="AGENTS.md",
            proposed_content="Never change protected files.\n",
        )
        self.assertIsNotNone(proposal)
        self.assertEqual(proposal.status, ProposalStatus.PROPOSED)
        self.assertEqual(proposal.evidence_signal_ids, ("s1", "s2", "s3"))
        self.assertEqual(proposal.conversation_count, 3)

    def test_proposal_creation_is_idempotent(self):
        self.record_three()
        kwargs = dict(
            artifact=ImprovementArtifact.RULE,
            target_path="AGENTS.md",
            proposed_content="Never change protected files.\n",
        )
        first = self.registry.maybe_propose("protect-root-readme", **kwargs)
        second = self.registry.maybe_propose("protect-root-readme", **kwargs)
        self.assertEqual(first.proposal_id, second.proposal_id)

    def test_preview_diff_shows_exact_change(self):
        self.record_three()
        proposal = self.registry.maybe_propose(
            "protect-root-readme",
            artifact=ImprovementArtifact.RULE,
            target_path="AGENTS.md",
            proposed_content="line one\nnew line\n",
        )
        diff = self.registry.preview_diff(proposal.proposal_id, "line one\nold line\n")
        self.assertIn("-old line", diff)
        self.assertIn("+new line", diff)
        self.assertIn("a/AGENTS.md", diff)

    def test_unapproved_change_is_blocked(self):
        self.record_three()
        proposal = self.registry.maybe_propose(
            "protect-root-readme",
            artifact=ImprovementArtifact.RULE,
            target_path="AGENTS.md",
            proposed_content="rule\n",
        )
        with self.assertRaises(PermissionError):
            self.registry.approved_change(proposal.proposal_id)

    def test_human_review_unlocks_exact_payload_once(self):
        self.record_three()
        proposal = self.registry.maybe_propose(
            "protect-root-readme",
            artifact=ImprovementArtifact.RULE,
            target_path="AGENTS.md",
            proposed_content="rule\n",
        )
        reviewed = self.registry.review(proposal.proposal_id, approve=True, actor="Nikola")
        self.assertEqual(reviewed.status, ProposalStatus.APPROVED)
        self.assertEqual(reviewed.reviewed_by, "Nikola")
        payload = self.registry.approved_change(proposal.proposal_id)
        self.assertEqual(payload["target_path"], "AGENTS.md")
        self.assertEqual(payload["proposed_content"], "rule\n")
        with self.assertRaises(ValueError):
            self.registry.review(proposal.proposal_id, approve=True, actor="Nikola")

    def test_dismissed_proposal_never_unlocks_payload(self):
        self.record_three()
        proposal = self.registry.maybe_propose(
            "protect-root-readme",
            artifact=ImprovementArtifact.DOC,
            target_path="docs/rule.md",
            proposed_content="doc\n",
        )
        reviewed = self.registry.review(proposal.proposal_id, approve=False, actor="Nikola")
        self.assertEqual(reviewed.status, ProposalStatus.DISMISSED)
        with self.assertRaises(PermissionError):
            self.registry.approved_change(proposal.proposal_id)

    def test_agent_overview_prioritizes_approval_and_failures(self):
        self.registry.upsert_agent("a1", harness="Codex", task="tests", state=AgentState.RUNNING)
        self.registry.upsert_agent(
            "a2", harness="Claude", task="review", state=AgentState.WAITING_APPROVAL, needs_approval=True
        )
        self.registry.upsert_agent("a3", harness="Local", task="lint", state=AgentState.FAILED)
        agents = self.registry.list_agents()
        self.assertEqual(agents[0].session_id, "a2")
        self.assertEqual(agents[1].session_id, "a3")
        self.assertEqual(agents[2].session_id, "a1")

    def test_agent_upsert_refreshes_state(self):
        self.registry.upsert_agent("a1", harness="Codex", task="build", state=AgentState.RUNNING)
        updated = self.registry.upsert_agent(
            "a1", harness="Codex", task="build", state=AgentState.FINISHED
        )
        self.assertEqual(updated.state, AgentState.FINISHED)
        self.assertFalse(updated.needs_approval)
        with self.assertRaises(KeyError):
            self.registry.get_agent("missing")


if __name__ == "__main__":
    unittest.main()
