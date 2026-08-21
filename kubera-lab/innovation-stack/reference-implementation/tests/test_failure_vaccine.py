import unittest
from kubera_innovation.failure_vaccine import FailureVaccineRegistry

class FailureVaccineTests(unittest.TestCase):
    def setUp(self): self.v=FailureVaccineRegistry()
    def tearDown(self): self.v.close()
    def test_contains_block(self): self.v.add_rule("r1",trigger_type="contains",pattern="wrong branch",reason="prevent deployment mistake"); self.assertEqual(self.v.check("deploy from wrong branch").action,"BLOCK")
    def test_no_match_allows(self): self.assertEqual(self.v.check("safe action").action,"ALLOW")
    def test_warn_rule(self): self.v.add_rule("r1",trigger_type="exact",pattern="risky",action="WARN",reason="review"); self.assertEqual(self.v.check("risky").action,"WARN")
    def test_regex(self): self.v.add_rule("r1",trigger_type="regex",pattern=r"port \d+ unavailable",reason="known port failure"); self.assertEqual(self.v.check("port 8080 unavailable").rule_id,"r1")
    def test_bad_trigger_type(self):
        with self.assertRaises(ValueError): self.v.add_rule("x",trigger_type="semantic",pattern="x",reason="x")
    def test_template(self): self.v.add_rule("r1",trigger_type="exact",pattern="x",reason="x"); self.assertIn("test_prevent_known_failure",self.v.regression_test_template("r1"))

if __name__ == "__main__": unittest.main()
