from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
from typing import Iterable
from uuid import uuid4


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class HandoffStatus(str, Enum):
    READY = "READY"
    BLOCKED = "BLOCKED"
    COMPLETE = "COMPLETE"


@dataclass(frozen=True)
class HandoffArtifact:
    """Immutable task-transfer artifact between specialist agents."""

    handoff_id: str
    task_id: str
    from_agent: str
    to_agent: str
    objective: str
    status: HandoffStatus
    output_summary: str
    source_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    next_action: str
    created_at: str

    @classmethod
    def create(
        cls,
        *,
        task_id: str,
        from_agent: str,
        to_agent: str,
        objective: str,
        status: HandoffStatus,
        output_summary: str,
        source_refs: Iterable[str] = (),
        evidence_refs: Iterable[str] = (),
        next_action: str,
        created_at: str | None = None,
    ) -> "HandoffArtifact":
        values = {
            "task_id": task_id,
            "from_agent": from_agent,
            "to_agent": to_agent,
            "objective": objective,
            "output_summary": output_summary,
            "next_action": next_action,
        }
        empty = [name for name, value in values.items() if not value.strip()]
        if empty:
            raise ValueError(f"handoff fields must not be empty: {', '.join(empty)}")
        return cls(
            handoff_id=str(uuid4()),
            task_id=task_id.strip(),
            from_agent=from_agent.strip(),
            to_agent=to_agent.strip(),
            objective=objective.strip(),
            status=status,
            output_summary=output_summary.strip(),
            source_refs=tuple(str(x).strip() for x in source_refs if str(x).strip()),
            evidence_refs=tuple(str(x).strip() for x in evidence_refs if str(x).strip()),
            next_action=next_action.strip(),
            created_at=created_at or _utc_now(),
        )

    def payload(self) -> dict[str, object]:
        return {
            "handoff_id": self.handoff_id,
            "task_id": self.task_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "objective": self.objective,
            "status": self.status.value,
            "output_summary": self.output_summary,
            "source_refs": list(self.source_refs),
            "evidence_refs": list(self.evidence_refs),
            "next_action": self.next_action,
            "created_at": self.created_at,
        }

    @property
    def artifact_hash(self) -> str:
        return "sha256:" + sha256(_canonical_json(self.payload()).encode("utf-8")).hexdigest()

    def to_markdown(self) -> str:
        sources = "\n".join(f"- {ref}" for ref in self.source_refs) or "- none"
        evidence = "\n".join(f"- {ref}" for ref in self.evidence_refs) or "- none"
        return (
            f"# HANDOFF {self.handoff_id}\n\n"
            f"- Task: `{self.task_id}`\n"
            f"- From: `{self.from_agent}`\n"
            f"- To: `{self.to_agent}`\n"
            f"- Status: **{self.status.value}**\n"
            f"- Created: `{self.created_at}`\n"
            f"- Artifact hash: `{self.artifact_hash}`\n\n"
            f"## Objective\n\n{self.objective}\n\n"
            f"## Output summary\n\n{self.output_summary}\n\n"
            f"## Sources\n\n{sources}\n\n"
            f"## Evidence\n\n{evidence}\n\n"
            f"## Next action\n\n{self.next_action}\n"
        )
