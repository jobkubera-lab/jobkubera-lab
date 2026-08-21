import unittest
from kubera_innovation.constitution import Constitution, Decision, PolicyRule

class ConstitutionTests(unittest.TestCase):
    def test_allow_rule(self):
        c = Constitution([PolicyRule("r1", "file.read", Decision.ALLOW)])
        self.assertEqual(c.evaluate("file.read")[0], Decision.ALLOW)
    def test_default_requires_approval(self):
        self.assertEqual(Constitution().evaluate("network.fetch")[0], Decision.REQUIRE_APPROVAL)
    def test_priority_wins(self):
        c = Constitution([PolicyRule("allow-all", "file.*", Decision.ALLOW, priority=100), PolicyRule("deny-delete", "file.delete", Decision.DENY, priority=10)])
        self.assertEqual(c.evaluate("file.delete")[0], Decision.DENY)
    def test_project_scope(self):
        c = Constitution([PolicyRule("private", "publish", Decision.DENY, project_pattern="private-*")])
        self.assertEqual(c.evaluate("publish", project="private-core")[0], Decision.DENY)
    def test_empty_action_denied(self):
        self.assertEqual(Constitution().evaluate("")[0], Decision.DENY)

if __name__ == "__main__": unittest.main()
