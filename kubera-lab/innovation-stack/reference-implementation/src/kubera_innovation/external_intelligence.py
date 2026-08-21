"""Hardened provider-independent contract for KUBERA External Intelligence Nodes."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from types import MappingProxyType
from typing import Iterable, Optional
from uuid import UUID, uuid4

from .authorization_grant import AuthorizationGrant, AuthorizationSigner

CONTRACT_VERSION = "3.0"


class ExternalRole(str, Enum):
    INDEPENDENT_AUDITOR = "independent_auditor"
    RED_TEAM = "red_team"
    ARCHITECTURE_CRITIC = "architecture_critic"
    TEST_DESIGNER = "test_designer"
    SPECIFICATION_ENGINEER = "specification_engineer"
    VISUAL_ARCHITECTURE_AGENT = "visual_architecture_agent"
    RESEARCH_CHALLENGER = "research_challenger"
    OPEN_SOURCE_SCOUT = "open_source_scout"
    DOCUMENTATION_REVIEWER = "documentation_reviewer"
    CRITIC_VERIFIER = "critic_verifier"


class ContextClassification(str, Enum):
    PUBLIC = "PUBLIC"
    PROJECT = "PROJECT"
    PRIVATE = "PRIVATE"


class Severity(str, Enum):
    INFO = "info"; LOW = "low"; MEDIUM = "medium"; HIGH = "high"; CRITICAL = "critical"


class Verdict(str, Enum):
    PASS = "pass"; NEEDS_CHANGES = "needs_changes"; BLOCKED = "blocked"; INCONCLUSIVE = "inconclusive"


class ExecutionStatus(str, Enum):
    COMPLETED = "completed"; PROVIDER_ERROR = "provider_error"; SCHEMA_VALIDATION_FAILED = "schema_validation_failed"; BLOCKED = "blocked"; TIMEOUT = "timeout"


class Constraint(str, Enum):
    DO_NOT_MODIFY_CODE = "do_not_modify_code"
    RETURN_STRUCTURED_FINDINGS = "return_structured_findings"
    SEPARATE_FACTS_FROM_ASSUMPTIONS = "separate_facts_from_assumptions"
    FOCUS_SECURITY_PRIVACY_CORRECTNESS = "focus_security_privacy_correctness"
    FOCUS_BYPASS_AND_FAILURE_MODES = "focus_bypass_and_failure_modes"
    DO_NOT_REQUEST_PRIVATE_CONTEXT = "do_not_request_private_context"


ROLE_MAX_CLASSIFICATION = MappingProxyType({
    ExternalRole.OPEN_SOURCE_SCOUT: ContextClassification.PUBLIC,
    ExternalRole.DOCUMENTATION_REVIEWER: ContextClassification.PUBLIC,
    ExternalRole.VISUAL_ARCHITECTURE_AGENT: ContextClassification.PROJECT,
    ExternalRole.RESEARCH_CHALLENGER: ContextClassification.PROJECT,
    ExternalRole.SPECIFICATION_ENGINEER: ContextClassification.PROJECT,
    ExternalRole.TEST_DESIGNER: ContextClassification.PROJECT,
    ExternalRole.ARCHITECTURE_CRITIC: ContextClassification.PROJECT,
    ExternalRole.INDEPENDENT_AUDITOR: ContextClassification.PROJECT,
    ExternalRole.RED_TEAM: ContextClassification.PROJECT,
    ExternalRole.CRITIC_VERIFIER: ContextClassification.PROJECT,
})
_CLASSIFICATION_ORDER = MappingProxyType({ContextClassification.PUBLIC: 0, ContextClassification.PROJECT: 1, ContextClassification.PRIVATE: 2})


def hash_context(text: str) -> str:
    if not text:
        raise ValueError("context text must not be empty")
    return "sha256:" + sha256(text.encode("utf-8")).hexdigest()


def _validate_uuid(value: str) -> None:
    UUID(value)


def _validate_timestamp(value: str) -> None:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone information")


@dataclass(frozen=True)
class ExternalContext:
    summary: str
    context_hash: str
    classification: ContextClassification = ContextClassification.PUBLIC
    redacted_fields: tuple[str, ...] = field(default_factory=tuple)
    authorization_grant: AuthorizationGrant | None = None

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ValueError("context summary must not be empty")
        if self.classification is ContextClassification.PRIVATE:
            raise PermissionError("PRIVATE context must never be sent to an external provider")
        if self.context_hash != hash_context(self.summary):
            raise ValueError("context_hash must match the exact context summary")
        if any(not item.strip() for item in self.redacted_fields):
            raise ValueError("redacted_fields must not contain empty values")
        if self.classification is ContextClassification.PROJECT and self.authorization_grant is None:
            raise PermissionError("PROJECT context requires a signed authorization grant")

    @classmethod
    def from_text(cls, text: str, *, classification: ContextClassification = ContextClassification.PUBLIC,
                  redacted_fields: Iterable[str] = (), authorization_grant: AuthorizationGrant | None = None) -> "ExternalContext":
        return cls(text, hash_context(text), classification, tuple(redacted_fields), authorization_grant)

    def verify_project_grant(self, signer: AuthorizationSigner, *, target: str) -> bool:
        if self.classification is ContextClassification.PUBLIC:
            return True
        assert self.authorization_grant is not None
        return signer.verify(self.authorization_grant, required_scope="external_project_share", subject=target)


@dataclass(frozen=True)
class ExternalIntelligenceRequest:
    role: ExternalRole
    target: str
    context: ExternalContext
    constraints: tuple[Constraint, ...] = field(default_factory=tuple)
    provider: str = "unspecified"
    request_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    contract_version: str = CONTRACT_VERSION
    max_role_classification: Optional[ContextClassification] = None
    timeout_seconds: int = 60
    budget_tokens: int = 6000

    def __post_init__(self) -> None:
        if self.contract_version != CONTRACT_VERSION: raise ValueError("unsupported contract_version")
        _validate_uuid(self.request_id); _validate_timestamp(self.timestamp)
        if not self.target.strip() or not self.provider.strip(): raise ValueError("target/provider must not be empty")
        if not 1 <= self.timeout_seconds <= 600: raise ValueError("timeout_seconds must be between 1 and 600")
        if not 1 <= self.budget_tokens <= 200000: raise ValueError("budget_tokens must be between 1 and 200000")
        if any(not isinstance(item, Constraint) for item in self.constraints): raise ValueError("unknown constraint; use Constraint enum")
        role_ceiling = ROLE_MAX_CLASSIFICATION[self.role]
        declared = self.max_role_classification or role_ceiling
        if declared is ContextClassification.PRIVATE: raise PermissionError("external role ceiling can never be PRIVATE")
        if _CLASSIFICATION_ORDER[declared] > _CLASSIFICATION_ORDER[role_ceiling]: raise PermissionError("declared ceiling exceeds role policy")
        if _CLASSIFICATION_ORDER[self.context.classification] > _CLASSIFICATION_ORDER[declared]: raise PermissionError("context exceeds role ceiling")
        object.__setattr__(self, "max_role_classification", declared)

    @classmethod
    def build(cls, *, role: ExternalRole, target: str, context: ExternalContext,
              constraints: Iterable[Constraint] = (), provider: str = "unspecified", **kwargs) -> "ExternalIntelligenceRequest":
        return cls(role, target, context, tuple(constraints), provider, **kwargs)

    def authorize(self, signer: AuthorizationSigner) -> None:
        if not self.context.verify_project_grant(signer, target=self.target):
            raise PermissionError("invalid, expired or incorrectly scoped project-sharing grant")

    def to_payload(self) -> dict:
        return {
            "contract_version": self.contract_version, "request_id": self.request_id, "timestamp": self.timestamp,
            "role": self.role.value, "target": self.target, "provider": self.provider,
            "max_role_classification": self.max_role_classification.value, "timeout_seconds": self.timeout_seconds,
            "budget_tokens": self.budget_tokens,
            "context": {"classification": self.context.classification.value, "summary": self.context.summary,
                        "context_hash": self.context.context_hash, "redacted_fields": list(self.context.redacted_fields),
                        "authorization_grant_id": self.context.authorization_grant.grant_id if self.context.authorization_grant else None},
            "constraints": [c.value for c in self.constraints],
        }


@dataclass(frozen=True)
class Finding:
    severity: Severity
    title: str
    confidence: float = 1.0
    evidence: str = ""
    suggested_fix: str = ""
    def __post_init__(self) -> None:
        if not self.title.strip(): raise ValueError("finding title must not be empty")
        if not 0 <= self.confidence <= 1: raise ValueError("finding confidence must be between 0 and 1")
    def to_payload(self) -> dict:
        return {"severity": self.severity.value, "confidence": self.confidence, "title": self.title,
                "evidence": self.evidence, "suggested_fix": self.suggested_fix}


@dataclass(frozen=True)
class ExternalIntelligenceResponse:
    request_id: str
    execution_status: ExecutionStatus
    summary: str
    provider: str
    model: str
    model_version: str
    latency_ms: int
    verdict: Optional[Verdict] = None
    findings: tuple[Finding, ...] = field(default_factory=tuple)
    unresolved_risks: tuple[str, ...] = field(default_factory=tuple)
    provider_error: Optional[str] = None
    contract_version: str = CONTRACT_VERSION

    def __post_init__(self) -> None:
        if self.contract_version != CONTRACT_VERSION: raise ValueError("unsupported contract_version")
        _validate_uuid(self.request_id)
        if any(not x.strip() for x in (self.summary, self.provider, self.model, self.model_version)):
            raise ValueError("summary/provider/model/model_version must not be empty")
        if self.latency_ms < 0: raise ValueError("latency_ms must not be negative")
        if self.execution_status is ExecutionStatus.COMPLETED and self.verdict is None: raise ValueError("completed execution requires verdict")
        if self.execution_status is not ExecutionStatus.COMPLETED and self.verdict is not None: raise ValueError("failed execution must not claim verdict")
        if self.execution_status is ExecutionStatus.PROVIDER_ERROR and not self.provider_error: raise ValueError("provider_error details required")

    def to_payload(self) -> dict:
        return {"contract_version": self.contract_version, "request_id": self.request_id,
                "execution_status": self.execution_status.value, "verdict": self.verdict.value if self.verdict else None,
                "summary": self.summary, "provider": self.provider, "model": self.model, "model_version": self.model_version,
                "latency_ms": self.latency_ms, "findings": [f.to_payload() for f in self.findings],
                "unresolved_risks": list(self.unresolved_risks), "provider_error": self.provider_error}
