import unittest

from kubera_innovation.plugin_registry import (
    LicenseState,
    PermissionProfile,
    PluginCandidate,
    PluginVerdict,
    ReviewState,
)


class PluginRegistryTests(unittest.TestCase):
    def test_unreviewed_candidate_cannot_enter_sandbox(self):
        p = PluginCandidate("x", "https://github.com/a/b", "catalog")
        self.assertFalse(p.eligible_for_sandbox())

    def test_license_and_security_review_enable_sandbox_eligibility(self):
        p = PluginCandidate(
            "x", "https://github.com/a/b", "catalog",
            license_state=LicenseState.VERIFIED,
            security_state=ReviewState.REVIEWED,
        )
        self.assertTrue(p.eligible_for_sandbox())

    def test_adoption_requires_explicit_adopted_verdict(self):
        p = PluginCandidate(
            "x", "https://github.com/a/b", "catalog",
            license_state=LicenseState.VERIFIED,
            security_state=ReviewState.REVIEWED,
        )
        self.assertFalse(p.eligible_for_adoption())

    def test_adopted_with_reviews_is_eligible(self):
        p = PluginCandidate(
            "x", "https://github.com/a/b", "catalog",
            license_state=LicenseState.VERIFIED,
            security_state=ReviewState.REVIEWED,
            verdict=PluginVerdict.ADOPTED,
        )
        self.assertTrue(p.eligible_for_adoption())

    def test_invalid_upstream_is_rejected(self):
        with self.assertRaises(ValueError):
            PluginCandidate("x", "http://example.com/a", "catalog")

    def test_invalid_permission_profile_fails(self):
        with self.assertRaises(ValueError):
            PermissionProfile(filesystem="root")

    def test_permission_payload_is_explicit(self):
        p = PluginCandidate(
            "x", "https://github.com/a/b", "catalog",
            permissions=PermissionProfile(filesystem="read", network="restricted", credentials="selected", process_execution=True),
        )
        payload = p.to_payload()
        self.assertEqual(payload["permissions"]["filesystem"], "read")
        self.assertTrue(payload["permissions"]["process_execution"])

    def test_unknown_license_is_default(self):
        p = PluginCandidate("x", "https://github.com/a/b", "catalog")
        self.assertEqual(p.license_state, LicenseState.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
