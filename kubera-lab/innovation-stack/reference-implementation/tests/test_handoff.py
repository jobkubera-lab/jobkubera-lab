from __future__ import annotations

import unittest

from kubera_innovation.handoff import HandoffArtifact, HandoffStatus


class HandoffTests(unittest.TestCase):
    def make(self) -> HandoffArtifact:
        return HandoffArtifact.create(
            task_id="task-1",
            from_agent="researcher",
            to_agent="verifier",
            objective="Verify the source-backed claim.",
            status=HandoffStatus.READY,
            output_summary="Draft claim with two references.",
            source_refs=("source:a", "source:b"),
            evidence_refs=("ledger:1",),
            next_action="Open both sources and verify the claim.",
            created_at="2026-09-03T10:00:00Z",
        )

    def test_artifact_has_stable_hash(self) -> None:
        artifact = self.make()
        self.assertEqual(artifact.artifact_hash, artifact.artifact_hash)
        self.assertTrue(artifact.artifact_hash.startswith("sha256:"))

    def test_markdown_contains_next_owner_sources_and_evidence(self) -> None:
        text = self.make().to_markdown()
        self.assertIn("`verifier`", text)
        self.assertIn("source:a", text)
        self.assertIn("ledger:1", text)
        self.assertIn("Open both sources", text)

    def test_handoff_md_is_same_existing_format(self) -> None:
        artifact = self.make()
        self.assertEqual(artifact.to_handoff_md(), artifact.to_markdown())

    def test_empty_next_action_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            HandoffArtifact.create(
                task_id="task-1",
                from_agent="a",
                to_agent="b",
                objective="x",
                status=HandoffStatus.BLOCKED,
                output_summary="blocked",
                next_action=" ",
            )


if __name__ == "__main__":
    unittest.main()
