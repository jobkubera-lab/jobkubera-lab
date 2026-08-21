from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Iterable


class ProofStage(IntEnum):
    IDEA = 0
    ISSUE = 1
    BRANCH = 2
    COMMIT = 3
    PULL_REQUEST = 4
    TEST = 5
    MERGE = 6
    DEMO = 7
    RELEASE = 8


@dataclass(frozen=True)
class ProofItem:
    stage: ProofStage
    title: str
    reference: str = ""
    verified: bool = False


@dataclass
class ProofOfWork:
    project_name: str
    items: list[ProofItem] = field(default_factory=list)

    def add(self, stage: ProofStage, title: str, *, reference: str = "", verified: bool = False) -> None:
        if not title:
            raise ValueError("title is required")
        self.items.append(ProofItem(stage, title, reference, verified))

    def validate_order(self) -> bool:
        stages = [int(i.stage) for i in self.items]
        return stages == sorted(stages)

    def completion_stage(self) -> ProofStage | None:
        verified = [i.stage for i in self.items if i.verified]
        return max(verified) if verified else None

    def render_markdown(self) -> str:
        lines = [f"# Proof of Work — {self.project_name}", "", f"Order valid: **{'yes' if self.validate_order() else 'no'}**", "", "| Stage | Evidence | Verified |", "|---|---|---:|"]
        for item in self.items:
            evidence = item.title if not item.reference else f"[{item.title}]({item.reference})"
            lines.append(f"| {item.stage.name.replace('_', ' ').title()} | {evidence} | {'✅' if item.verified else '—'} |")
        return "\n".join(lines) + "\n"

    @classmethod
    def from_items(cls, project_name: str, items: Iterable[ProofItem]) -> "ProofOfWork":
        return cls(project_name=project_name, items=list(items))
