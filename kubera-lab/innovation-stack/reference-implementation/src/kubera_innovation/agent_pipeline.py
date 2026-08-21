"""Deterministic Builder → Critic → Verifier pipeline.

No LLM or external provider is called here. Each role is an injected callable,
which makes the control flow deterministic and testable before provider adapters exist.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
from uuid import uuid4

from .evidence_ledger import EvidenceLedger


class PipelineVerdict(str, Enum):
    PASS = "pass"
    NEEDS_CHANGES = "needs_changes"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class StageResult:
    content: dict[str, Any]
    verdict: PipelineVerdict = PipelineVerdict.PASS
    findings: tuple[str, ...] = field(default_factory=tuple)

    def to_payload(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "verdict": self.verdict.value,
            "findings": list(self.findings),
        }


@dataclass(frozen=True)
class PipelineResult:
    run_id: str
    verdict: PipelineVerdict
    builder: StageResult
    critic: StageResult
    verifier: StageResult
    evidence_entries: int
    evidence_chain_valid: bool

    def to_payload(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "verdict": self.verdict.value,
            "builder": self.builder.to_payload(),
            "critic": self.critic.to_payload(),
            "verifier": self.verifier.to_payload(),
            "evidence_entries": self.evidence_entries,
            "evidence_chain_valid": self.evidence_chain_valid,
        }


Builder = Callable[[dict[str, Any]], StageResult]
Critic = Callable[[dict[str, Any], StageResult], StageResult]
Verifier = Callable[[dict[str, Any], StageResult, StageResult], StageResult]


class DeterministicAgentPipeline:
    """Runs fixed stages and records every handoff in an Evidence Ledger."""

    def __init__(self, *, builder: Builder, critic: Critic, verifier: Verifier, ledger: EvidenceLedger) -> None:
        self.builder = builder
        self.critic = critic
        self.verifier = verifier
        self.ledger = ledger

    def run(self, request: dict[str, Any], *, run_id: str | None = None) -> PipelineResult:
        if not isinstance(request, dict) or not request:
            raise ValueError("request must be a non-empty dictionary")
        rid = run_id or str(uuid4())

        builder_result = self.builder(dict(request))
        self._record(rid, "builder", request, builder_result)

        critic_result = self.critic(dict(request), builder_result)
        self._record(rid, "critic", builder_result.to_payload(), critic_result)

        if critic_result.verdict is PipelineVerdict.BLOCKED:
            verifier_result = StageResult(
                {"reason": "critic_blocked"},
                verdict=PipelineVerdict.BLOCKED,
                findings=("verification skipped because critic blocked the artifact",),
            )
        else:
            verifier_result = self.verifier(dict(request), builder_result, critic_result)
        self._record(rid, "verifier", critic_result.to_payload(), verifier_result)

        final_verdict = self._final_verdict(critic_result, verifier_result)
        entries = self.ledger.entries(rid)
        return PipelineResult(
            run_id=rid,
            verdict=final_verdict,
            builder=builder_result,
            critic=critic_result,
            verifier=verifier_result,
            evidence_entries=len(entries),
            evidence_chain_valid=self.ledger.verify_chain(),
        )

    def _record(self, run_id: str, stage: str, input_value: Any, result: StageResult) -> None:
        self.ledger.append(
            run_id=run_id,
            stage=stage,
            input_value=input_value,
            output_value=result.to_payload(),
            metadata={"verdict": result.verdict.value},
        )

    @staticmethod
    def _final_verdict(critic: StageResult, verifier: StageResult) -> PipelineVerdict:
        if PipelineVerdict.BLOCKED in {critic.verdict, verifier.verdict}:
            return PipelineVerdict.BLOCKED
        if PipelineVerdict.NEEDS_CHANGES in {critic.verdict, verifier.verdict}:
            return PipelineVerdict.NEEDS_CHANGES
        return PipelineVerdict.PASS
