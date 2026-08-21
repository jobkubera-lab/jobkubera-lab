import unittest
from datetime import datetime, timedelta, timezone
from dataclasses import replace
from kubera_innovation.authorization_grant import AuthorizationSigner

class AuthorizationGrantTests(unittest.TestCase):
    def setUp(self): self.signer=AuthorizationSigner(b"s"*32)
    def test_valid_grant(self):
        g=self.signer.issue(scope="external_project_share",subject="target")
        self.assertTrue(self.signer.verify(g,required_scope="external_project_share",subject="target"))
    def test_tamper_fails(self):
        g=self.signer.issue(scope="external_project_share",subject="target")
        self.assertFalse(self.signer.verify(replace(g,subject="other"),required_scope="external_project_share",subject="other"))
    def test_wrong_scope_fails(self):
        g=self.signer.issue(scope="other",subject="target")
        self.assertFalse(self.signer.verify(g,required_scope="external_project_share",subject="target"))
    def test_short_secret_rejected(self):
        with self.assertRaises(ValueError): AuthorizationSigner(b"short")
