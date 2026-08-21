import unittest
from kubera_innovation.proof_work import ProofOfWork, ProofStage

class ProofWorkTests(unittest.TestCase):
    def test_valid_order(self):
        p=ProofOfWork("x"); p.add(ProofStage.IDEA,"idea"); p.add(ProofStage.TEST,"test"); self.assertTrue(p.validate_order())
    def test_invalid_order(self):
        p=ProofOfWork("x"); p.add(ProofStage.TEST,"test"); p.add(ProofStage.IDEA,"idea"); self.assertFalse(p.validate_order())
    def test_completion_stage_uses_verified_only(self):
        p=ProofOfWork("x"); p.add(ProofStage.IDEA,"idea",verified=True); p.add(ProofStage.RELEASE,"release",verified=False); self.assertEqual(p.completion_stage(),ProofStage.IDEA)
    def test_markdown(self):
        p=ProofOfWork("x"); p.add(ProofStage.PULL_REQUEST,"PR 1",reference="https://example.com",verified=True); md=p.render_markdown(); self.assertIn("Proof of Work",md); self.assertIn("PR 1",md); self.assertIn("✅",md)
    def test_empty_completion(self): self.assertIsNone(ProofOfWork("x").completion_stage())
    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError): ProofOfWork("x").add(ProofStage.IDEA,"")

if __name__ == "__main__": unittest.main()
