import unittest

from kubera_innovation.external_intelligence import (
    ContextClassification,
    ExternalContext,
    ExternalIntelligenceRequest,
    ExternalIntelligenceResponse,
    ExternalRole,
    Finding,
    Severity,
    Verdict,
)


class ExternalIntelligenceTests(unittest.TestCase):
    def test_contract_has_ten_roles(self):
        self.assertEqual(len(ExternalRole), 10)

    def test_public_context_does_not_require_share_flag(self):
        ctx = ExternalContext("Public README excerpt")
        self.assertEqual(ctx.classification, ContextClassification.PUBLIC)

    def test_project_context_requires_explicit_share_authorization(self):
        with self.assertRaises(PermissionError):
            ExternalContext("Internal design", ContextClassification.PROJECT, False)

    def test_private_context_requires_explicit_share_authorization(self):
        with self.assertRaises(PermissionError):
            ExternalContext("Private code", ContextClassification.PRIVATE, False)

    def test_private_context_can_be_explicitly_authorized(self):
        ctx = ExternalContext("Selected private excerpt", ContextClassification.PRIVATE, True)
        self.assertTrue(ctx.share_authorized)

    def test_empty_target_fails(self):
        ctx = ExternalContext("Public context")
        with self.assertRaises(ValueError):
            ExternalIntelligenceRequest(ExternalRole.TEST_DESIGNER, " ", ctx)

    def test_request_payload_is_provider_independent(self):
        ctx = ExternalContext("Architecture excerpt", ContextClassification.PROJECT, True)
        req = ExternalIntelligenceRequest.build(
            role=ExternalRole.ARCHITECTURE_CRITIC,
            target="authority budget",
            context=ctx,
            constraints=["do_not_modify_code"],
            provider="claude",
        )
        payload = req.to_payload()
        self.assertEqual(payload["role"], "architecture_critic")
        self.assertEqual(payload["provider"], "claude")
        self.assertEqual(payload["contract_version"], "1.0")

    def test_response_serializes_verdict_and_finding(self):
        response = ExternalIntelligenceResponse(
            Verdict.NEEDS_CHANGES,
            "One gap found",
            (Finding(Severity.HIGH, "Missing normalization", "evidence", "normalize first"),),
        )
        payload = response.to_payload()
        self.assertEqual(payload["verdict"], "needs_changes")
        self.assertEqual(payload["findings"][0]["severity"], "high")


if __name__ == "__main__":
    unittest.main()
