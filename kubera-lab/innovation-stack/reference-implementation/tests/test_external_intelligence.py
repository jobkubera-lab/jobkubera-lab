import unittest

from kubera_innovation.external_intelligence import (
    CONTRACT_VERSION,
    ContextClassification,
    ExecutionStatus,
    ExternalContext,
    ExternalIntelligenceRequest,
    ExternalIntelligenceResponse,
    ExternalRole,
    Finding,
    Severity,
    Verdict,
    hash_context,
)


class ExternalIntelligenceTests(unittest.TestCase):
    def test_contract_has_ten_roles(self):
        self.assertEqual(len(ExternalRole), 10)

    def test_context_hash_is_sha256(self):
        value = hash_context("hello")
        self.assertTrue(value.startswith("sha256:"))
        self.assertEqual(len(value), 71)

    def test_private_context_is_always_blocked(self):
        with self.assertRaises(PermissionError):
            ExternalContext.from_text(
                "private source",
                classification=ContextClassification.PRIVATE,
                share_authorized=True,
            )

    def test_project_context_requires_explicit_share_authorization(self):
        with self.assertRaises(PermissionError):
            ExternalContext.from_text(
                "project packet",
                classification=ContextClassification.PROJECT,
                share_authorized=False,
            )

    def test_project_context_can_be_authorized(self):
        ctx = ExternalContext.from_text(
            "sanitized project packet",
            classification=ContextClassification.PROJECT,
            share_authorized=True,
            redacted_fields=["api_key"],
        )
        self.assertEqual(ctx.classification, ContextClassification.PROJECT)
        self.assertEqual(ctx.redacted_fields, ("api_key",))

    def test_public_only_role_cannot_receive_project_context(self):
        ctx = ExternalContext.from_text(
            "project docs",
            classification=ContextClassification.PROJECT,
            share_authorized=True,
        )
        with self.assertRaises(PermissionError):
            ExternalIntelligenceRequest.build(
                role=ExternalRole.DOCUMENTATION_REVIEWER,
                target="docs",
                context=ctx,
                provider="claude",
            )

    def test_open_source_scout_is_public_only(self):
        ctx = ExternalContext.from_text(
            "project internals",
            classification=ContextClassification.PROJECT,
            share_authorized=True,
        )
        with self.assertRaises(PermissionError):
            ExternalIntelligenceRequest.build(
                role=ExternalRole.OPEN_SOURCE_SCOUT,
                target="plugin search",
                context=ctx,
                provider="claude",
            )

    def test_architecture_critic_can_receive_project_packet(self):
        ctx = ExternalContext.from_text(
            "sanitized architecture",
            classification=ContextClassification.PROJECT,
            share_authorized=True,
        )
        req = ExternalIntelligenceRequest.build(
            role=ExternalRole.ARCHITECTURE_CRITIC,
            target="authority budget",
            context=ctx,
            provider="claude",
        )
        self.assertEqual(req.max_role_classification, ContextClassification.PROJECT)

    def test_declared_ceiling_cannot_expand_role_policy(self):
        ctx = ExternalContext.from_text("public docs")
        with self.assertRaises(PermissionError):
            ExternalIntelligenceRequest.build(
                role=ExternalRole.DOCUMENTATION_REVIEWER,
                target="docs",
                context=ctx,
                provider="claude",
                max_role_classification=ContextClassification.PROJECT,
            )

    def test_external_ceiling_can_never_be_private(self):
        ctx = ExternalContext.from_text("public")
        with self.assertRaises(PermissionError):
            ExternalIntelligenceRequest.build(
                role=ExternalRole.RED_TEAM,
                target="policy",
                context=ctx,
                provider="claude",
                max_role_classification=ContextClassification.PRIVATE,
            )

    def test_request_contains_audit_fields(self):
        ctx = ExternalContext.from_text("public architecture")
        req = ExternalIntelligenceRequest.build(
            role=ExternalRole.ARCHITECTURE_CRITIC,
            target="architecture",
            context=ctx,
            provider="claude",
            timeout_seconds=45,
            budget_tokens=2500,
        )
        payload = req.to_payload()
        self.assertEqual(payload["contract_version"], CONTRACT_VERSION)
        self.assertIn("request_id", payload)
        self.assertIn("timestamp", payload)
        self.assertIn("context_hash", payload["context"])
        self.assertEqual(payload["timeout_seconds"], 45)
        self.assertEqual(payload["budget_tokens"], 2500)

    def test_timeout_budget_limits(self):
        ctx = ExternalContext.from_text("public")
        with self.assertRaises(ValueError):
            ExternalIntelligenceRequest.build(
                role=ExternalRole.ARCHITECTURE_CRITIC,
                target="x",
                context=ctx,
                timeout_seconds=0,
            )
        with self.assertRaises(ValueError):
            ExternalIntelligenceRequest.build(
                role=ExternalRole.ARCHITECTURE_CRITIC,
                target="x",
                context=ctx,
                budget_tokens=0,
            )

    def test_finding_confidence_range(self):
        with self.assertRaises(ValueError):
            Finding(Severity.HIGH, "bad", confidence=1.5)

    def test_completed_response_requires_verdict_and_metadata(self):
        req = ExternalIntelligenceRequest.build(
            role=ExternalRole.ARCHITECTURE_CRITIC,
            target="x",
            context=ExternalContext.from_text("public"),
            provider="claude",
        )
        response = ExternalIntelligenceResponse(
            request_id=req.request_id,
            execution_status=ExecutionStatus.COMPLETED,
            verdict=Verdict.NEEDS_CHANGES,
            summary="One gap found",
            provider="anthropic",
            model="claude",
            model_version="test-version",
            latency_ms=120,
            findings=(Finding(Severity.HIGH, "Gap", confidence=0.9),),
        )
        payload = response.to_payload()
        self.assertEqual(payload["execution_status"], "completed")
        self.assertEqual(payload["verdict"], "needs_changes")
        self.assertEqual(payload["provider"], "anthropic")
        self.assertEqual(payload["findings"][0]["confidence"], 0.9)

    def test_completed_response_without_verdict_fails(self):
        req = ExternalIntelligenceRequest.build(
            role=ExternalRole.TEST_DESIGNER,
            target="x",
            context=ExternalContext.from_text("public"),
        )
        with self.assertRaises(ValueError):
            ExternalIntelligenceResponse(
                request_id=req.request_id,
                execution_status=ExecutionStatus.COMPLETED,
                summary="",
                provider="anthropic",
                model="claude",
                model_version="x",
                latency_ms=10,
            )

    def test_provider_error_is_not_task_verdict(self):
        req = ExternalIntelligenceRequest.build(
            role=ExternalRole.TEST_DESIGNER,
            target="x",
            context=ExternalContext.from_text("public"),
        )
        response = ExternalIntelligenceResponse(
            request_id=req.request_id,
            execution_status=ExecutionStatus.PROVIDER_ERROR,
            verdict=None,
            summary="Provider unavailable",
            provider="anthropic",
            model="claude",
            model_version="unknown",
            latency_ms=400,
            provider_error="service_unavailable",
        )
        self.assertIsNone(response.to_payload()["verdict"])
        self.assertEqual(response.to_payload()["provider_error"], "service_unavailable")

    def test_failed_execution_cannot_claim_verdict(self):
        req = ExternalIntelligenceRequest.build(
            role=ExternalRole.TEST_DESIGNER,
            target="x",
            context=ExternalContext.from_text("public"),
        )
        with self.assertRaises(ValueError):
            ExternalIntelligenceResponse(
                request_id=req.request_id,
                execution_status=ExecutionStatus.TIMEOUT,
                verdict=Verdict.PASS,
                summary="bad state",
                provider="anthropic",
                model="claude",
                model_version="x",
                latency_ms=1000,
            )


if __name__ == "__main__":
    unittest.main()
