import unittest
from types import MappingProxyType

from kubera_innovation.authorization_grant import AuthorizationSigner
from kubera_innovation.external_intelligence import (
    CONTRACT_VERSION, Constraint, ContextClassification, ExecutionStatus, ExternalContext,
    ExternalIntelligenceRequest, ExternalIntelligenceResponse, ExternalRole, Finding,
    ROLE_MAX_CLASSIFICATION, Severity, Verdict, hash_context,
)

SECRET=b"k"*32

class ExternalIntelligenceTests(unittest.TestCase):
    def signer(self): return AuthorizationSigner(SECRET)
    def grant(self, target="architecture"): return self.signer().issue(scope="external_project_share", subject=target)

    def test_contract_has_ten_roles(self): self.assertEqual(len(ExternalRole),10)
    def test_hash_is_bound_to_content(self):
        with self.assertRaises(ValueError):
            ExternalContext("changed", hash_context("other"))
    def test_private_context_is_always_blocked(self):
        with self.assertRaises(PermissionError): ExternalContext.from_text("private", classification=ContextClassification.PRIVATE)
    def test_project_requires_signed_grant(self):
        with self.assertRaises(PermissionError): ExternalContext.from_text("project", classification=ContextClassification.PROJECT)
    def test_project_grant_must_match_target(self):
        ctx=ExternalContext.from_text("project", classification=ContextClassification.PROJECT, authorization_grant=self.grant("architecture"))
        req=ExternalIntelligenceRequest.build(role=ExternalRole.ARCHITECTURE_CRITIC,target="architecture",context=ctx,provider="claude")
        req.authorize(self.signer())
        bad=ExternalIntelligenceRequest.build(role=ExternalRole.ARCHITECTURE_CRITIC,target="other",context=ctx,provider="claude")
        with self.assertRaises(PermissionError): bad.authorize(self.signer())
    def test_role_policy_is_immutable(self):
        with self.assertRaises(TypeError): ROLE_MAX_CLASSIFICATION[ExternalRole.OPEN_SOURCE_SCOUT]=ContextClassification.PROJECT
    def test_public_only_role_rejects_project(self):
        ctx=ExternalContext.from_text("project", classification=ContextClassification.PROJECT, authorization_grant=self.grant("docs"))
        with self.assertRaises(PermissionError): ExternalIntelligenceRequest.build(role=ExternalRole.DOCUMENTATION_REVIEWER,target="docs",context=ctx,provider="claude")
    def test_unknown_constraint_fails(self):
        ctx=ExternalContext.from_text("public")
        with self.assertRaises(ValueError): ExternalIntelligenceRequest.build(role=ExternalRole.TEST_DESIGNER,target="x",context=ctx,constraints=("do_not_modify_cod",))
    def test_known_constraint_serializes(self):
        ctx=ExternalContext.from_text("public")
        req=ExternalIntelligenceRequest.build(role=ExternalRole.TEST_DESIGNER,target="x",context=ctx,constraints=(Constraint.DO_NOT_MODIFY_CODE,))
        self.assertEqual(req.to_payload()["constraints"],["do_not_modify_code"])
    def test_request_audit_fields(self):
        req=ExternalIntelligenceRequest.build(role=ExternalRole.ARCHITECTURE_CRITIC,target="x",context=ExternalContext.from_text("public"),provider="claude")
        p=req.to_payload(); self.assertEqual(p["contract_version"],CONTRACT_VERSION); self.assertIn("request_id",p); self.assertIn("context_hash",p["context"])
    def test_response_metadata_nonempty(self):
        req=ExternalIntelligenceRequest.build(role=ExternalRole.TEST_DESIGNER,target="x",context=ExternalContext.from_text("public"))
        with self.assertRaises(ValueError): ExternalIntelligenceResponse(req.request_id,ExecutionStatus.COMPLETED,"","anthropic","claude","v",1,Verdict.PASS)
    def test_completed_response(self):
        req=ExternalIntelligenceRequest.build(role=ExternalRole.TEST_DESIGNER,target="x",context=ExternalContext.from_text("public"))
        r=ExternalIntelligenceResponse(req.request_id,ExecutionStatus.COMPLETED,"ok","anthropic","claude","v",10,Verdict.PASS,(Finding(Severity.INFO,"ok",0.9),))
        self.assertEqual(r.to_payload()["verdict"],"pass")
    def test_provider_error_separate(self):
        req=ExternalIntelligenceRequest.build(role=ExternalRole.TEST_DESIGNER,target="x",context=ExternalContext.from_text("public"))
        r=ExternalIntelligenceResponse(req.request_id,ExecutionStatus.PROVIDER_ERROR,"unavailable","anthropic","claude","unknown",10,None,provider_error="down")
        self.assertIsNone(r.to_payload()["verdict"])

if __name__=="__main__": unittest.main()
