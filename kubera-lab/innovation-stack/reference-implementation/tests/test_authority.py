import unittest
from datetime import datetime, timedelta, timezone
from kubera_innovation.authority import AuthorityBudget, ControlLevel

class AuthorityTests(unittest.TestCase):
    def test_consume_within_budget(self):
        b=AuthorityBudget(ControlLevel.ACT,{"write":2}); self.assertTrue(b.consume("write").allowed); self.assertEqual(b.used("write"),1)
    def test_exhaustion(self):
        b=AuthorityBudget(ControlLevel.ACT,{"write":1}); self.assertTrue(b.consume("write").allowed); self.assertFalse(b.consume("write").allowed)
    def test_missing_capability_denied(self): self.assertFalse(AuthorityBudget(ControlLevel.ADMIN,{}).consume("delete").allowed)
    def test_insufficient_level(self): self.assertFalse(AuthorityBudget(ControlLevel.READ,{"write":5}).consume("write",required_level=ControlLevel.CREATE).allowed)
    def test_expired(self):
        b=AuthorityBudget(ControlLevel.ACT,{"write":1},expires_at=datetime.now(timezone.utc)-timedelta(seconds=1)); self.assertFalse(b.consume("write").allowed)
    def test_zero_amount_denied(self): self.assertFalse(AuthorityBudget(ControlLevel.ACT,{"write":1}).consume("write",amount=0).allowed)

if __name__ == "__main__": unittest.main()
