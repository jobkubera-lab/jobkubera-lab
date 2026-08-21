"""Provider-independent contract for KUBERA External Intelligence Nodes.

This module validates structured handoffs. It does not call any external API and
must not be treated as a production data-loss-prevention boundary.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Iterable


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
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Verdict(str, Enum):
    PASS = "pass"
    NEEDS_CHANGES = "needs_changes"
    BLOCKED = "blocked"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True)
class ExternalContext:
    summary: str
    classification: ContextClassification = ContextClassification.PUBLIC
    share_authorized: bool = False

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ValueError("context summary must not be empty")
        if self.classification is not ContextClassification.PUBLIC and not self.share_authorized:
            raise PermissionError(
                f"{self.classification.value} context requires explicit external sharing authorization"
            )


@dataclass(frozen=True)
class ExternalIntelligenceRequest:
    role: ExternalRole
    target: str
    context: ExternalContext
    constraints: tuple[str, ...] = field(default_factory=tuple)
    provider: str = "unspecified"

    def __post_init__(self) -> None:
        if not self.target.strip():
            raise ValueError("target must not be empty")
        if not self.provider.strip():
            raise ValueError("provider must not be empty")
        if any(not item.strip() for item in self.constraints):
            raise ValueError("constraints must not contain empty values")

    @classmethod
    def build(
        cls,
        *,
        role: ExternalRole,
        target: str,
        context: ExternalContext,
        constraints: Iterable[str] = (),
        provider: str = "unspecified",
    ) -> "ExternalIntelligenceRequest":
        return cls(role, target, context, tuple(constraints), provider)

    def to_payload(self) -> dict:
        return {
            "contract_version": "1.0",
            "role": self.role.value,
            "target": self.target,
            "provider": self.provider,
            "context": {
                "classification": self.context.classification.value,
                "share_authorized": self.context.share_authorized,
                "summary": self.context.summary,
            },
            "constraints": list(self.constraints),
        }


@dataclass(frozen=True)
class Finding:
    severity: Severity
    title: str
    evidence: str = ""
    suggested_fix: str = ""

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("finding title must not be empty")

    def to_payload(self) -> dict:
        return {
            "severity": self.severity.value,
            "title": self.title,
            "evidence": self.evidence,
            "suggested_fix": self.suggested_fix,
        }


@dataclass(frozen=True)
class ExternalIntelligenceResponse:
    verdict: Verdict
    summary: str
    findings: tuple[Finding, ...] = field(default_factory=tuple)
    unresolved_risks: tuple[str, ...] = field(default_factory=tuple)

    def to_payload(self) -> dict:
        return {
            "contract_version": "1.0",
            "verdict": self.verdict.value,
            "summary": self.summary,
            "findings": [finding.to_payload() for finding in self.findings],
            "unresolved_risks": list(self.unresolved_risks),
        }
