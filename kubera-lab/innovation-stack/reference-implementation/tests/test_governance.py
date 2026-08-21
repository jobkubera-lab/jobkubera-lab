import unittest
from kubera_innovation.authority import AuthorityBudget, ControlLevel
from kubera_innovation.constitution import Constitution, Decision, PolicyRule
from kubera_innovation.governance import GovernanceGate

class GovernanceGateTests(unittest.TestCase):
    def test_constitution_deny_prevents_budget_spend(self):
        c=Constitution([PolicyRule("deny","delete",Decision.DENY)]); b=AuthorityBudget(ControlLevel.ADMIN,{"delete":1}); r=GovernanceGate(c,b).authorize("delete","delete",required_level=ControlLevel.ADMIN); self.assertFalse(r.allowed); self.assertEqual(b.used("delete"),0)
    def test_approval_does_not_spend_budget(self):
        c=Constitution(); b=AuthorityBudget(ControlLevel.ACT,{"write":1}); r=GovernanceGate(c,b).authorize("write","write"); self.assertTrue(r.requires_approval); self.assertEqual(b.used("write"),0)
    def test_allow_then_budget(self):
        c=Constitution([PolicyRule("allow","write",Decision.ALLOW)]); b=AuthorityBudget(ControlLevel.ACT,{"write":1}); r=GovernanceGate(c,b).authorize("write","write"); self.assertTrue(r.allowed); self.assertEqual(r.remaining,0)
    def test_allow_but_capability_missing(self):
        c=Constitution([PolicyRule("allow","write",Decision.ALLOW)]); r=GovernanceGate(c,AuthorityBudget(ControlLevel.ACT,{})).authorize("write","write"); self.assertFalse(r.allowed)

if __name__ == "__main__": unittest.main()
