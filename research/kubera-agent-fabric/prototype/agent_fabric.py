"""Minimal KUBERA Agent Fabric prototype.

This is an experimental reference implementation, not production-ready.
It demonstrates bounded workflow execution, explicit verification,
human approval gates, and an append-only evidence/action ledger.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Callable, Iterable, List, Optional


class Risk(str, Enum):
    READ_ONLY = "read_only"
    EXTERNAL_WRITE = "external_write"
    DESTRUCTIVE = "destructive"
    FINANCIAL = "financial"


class Status(str, Enum):
    PLANNED = "planned"
    VERIFIED = "verified"
    APPROVED = "approved"
    EXECUTED = "executed"
    REJECTED = "rejected"


@dataclass(frozen=True)
class Evidence:
    source: str
    claim: str
    observed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class ActionIntent:
    agent: str
    action: str
    target: str
    risk: Risk
    evidence: List[Evidence]
    confidence: float
    approval_required: bool
    expires_at: Optional[str] = None
    status: Status = Status.PLANNED

    def validate(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.risk != Risk.READ_ONLY and not self.approval_required:
            raise ValueError("non-read-only actions must require approval")
        if not self.evidence:
            raise ValueError("action intent requires evidence")


@dataclass(frozen=True)
class LedgerEntry:
    event: str
    payload: dict
    previous_hash: str
    hash: str
    created_at: str


class EvidenceLedger:
    """Small append-only hash-chained ledger for prototype use."""

    def __init__(self) -> None:
        self._entries: List[LedgerEntry] = []

    def append(self, event: str, payload: dict) -> LedgerEntry:
        previous_hash = self._entries[-1].hash if self._entries else "GENESIS"
        created_at = datetime.now(timezone.utc).isoformat()
        canonical = json.dumps(
            {
                "event": event,
                "payload": payload,
                "previous_hash": previous_hash,
                "created_at": created_at,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        entry = LedgerEntry(event, payload, previous_hash, digest, created_at)
        self._entries.append(entry)
        return entry

    @property
    def entries(self) -> tuple[LedgerEntry, ...]:
        return tuple(self._entries)

    def verify_chain(self) -> bool:
        previous = "GENESIS"
        for entry in self._entries:
            if entry.previous_hash != previous:
                return False
            canonical = json.dumps(
                {
                    "event": entry.event,
                    "payload": entry.payload,
                    "previous_hash": entry.previous_hash,
                    "created_at": entry.created_at,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            if hashlib.sha256(canonical.encode("utf-8")).hexdigest() != entry.hash:
                return False
            previous = entry.hash
        return True


@dataclass
class WorkerResult:
    worker: str
    finding: str
    evidence: List[Evidence]


class Fabric:
    def __init__(self, max_workers: int = 8) -> None:
        if max_workers < 1:
            raise ValueError("max_workers must be positive")
        self.max_workers = max_workers
        self.ledger = EvidenceLedger()

    def run_collect(
        self,
        jobs: Iterable[str],
        worker: Callable[[str], WorkerResult],
    ) -> list[WorkerResult]:
        jobs = list(jobs)
        if len(jobs) > self.max_workers:
            raise ValueError("worker budget exceeded")
        results = [worker(job) for job in jobs]
        self.ledger.append(
            "collect.complete",
            {"workers": len(results), "findings": [r.finding for r in results]},
        )
        return results

    def verify(
        self,
        results: Iterable[WorkerResult],
        verifier: Callable[[WorkerResult], bool],
    ) -> list[WorkerResult]:
        accepted = []
        for result in results:
            ok = verifier(result)
            self.ledger.append(
                "verify.result",
                {"worker": result.worker, "finding": result.finding, "accepted": ok},
            )
            if ok:
                accepted.append(result)
        return accepted

    def propose_action(self, intent: ActionIntent) -> ActionIntent:
        intent.validate()
        intent.status = Status.VERIFIED
        self.ledger.append("action.proposed", _intent_dict(intent))
        return intent

    def approve(self, intent: ActionIntent, approved: bool) -> ActionIntent:
        if intent.status != Status.VERIFIED:
            raise ValueError("intent must be verified before approval")
        intent.status = Status.APPROVED if approved else Status.REJECTED
        self.ledger.append("action.approval", _intent_dict(intent))
        return intent

    def execute(
        self,
        intent: ActionIntent,
        executor: Callable[[ActionIntent], dict],
    ) -> dict:
        if intent.risk != Risk.READ_ONLY and intent.status != Status.APPROVED:
            raise PermissionError("human approval required")
        if intent.risk == Risk.READ_ONLY and intent.status not in {
            Status.VERIFIED,
            Status.APPROVED,
        }:
            raise PermissionError("intent must be verified")
        receipt = executor(intent)
        intent.status = Status.EXECUTED
        self.ledger.append(
            "action.executed",
            {"intent": _intent_dict(intent), "receipt": receipt},
        )
        return receipt


def _intent_dict(intent: ActionIntent) -> dict:
    payload = asdict(intent)
    payload["risk"] = intent.risk.value
    payload["status"] = intent.status.value
    return payload
