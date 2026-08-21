import unittest
from kubera_innovation.reputation import ReputationEngine

class ReputationTests(unittest.TestCase):
    def setUp(self): self.r=ReputationEngine()
    def tearDown(self): self.r.close()
    def test_verified_event_counts(self): self.r.record("a","accuracy",1.0,verified=True); self.assertEqual(self.r.summary("a").verified_events,1)
    def test_unverified_event_ignored(self): self.r.record("a","accuracy",0.0,verified=False); self.assertEqual(self.r.summary("a").overall,0.0)
    def test_weighted_average(self): self.r.record("a","accuracy",1.0,weight=3,verified=True); self.r.record("a","accuracy",0.0,weight=1,verified=True); self.assertEqual(self.r.summary("a").dimensions["accuracy"],0.75)
    def test_multiple_dimensions(self): self.r.record("a","accuracy",1.0,verified=True); self.r.record("a","safety",0.5,verified=True); self.assertEqual(self.r.summary("a").overall,0.75)
    def test_score_bounds(self):
        with self.assertRaises(ValueError): self.r.record("a","accuracy",1.1,verified=True)
    def test_weight_positive(self):
        with self.assertRaises(ValueError): self.r.record("a","accuracy",1.0,weight=0,verified=True)

if __name__ == "__main__": unittest.main()
