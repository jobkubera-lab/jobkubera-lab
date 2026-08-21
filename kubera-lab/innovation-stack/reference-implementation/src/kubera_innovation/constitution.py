from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fnmatch import fnmatch
from typing import Iterable


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


@dataclass(frozen=True)
class PolicyRule:
    rule_id: str
    action_pattern: str
    decision: Decision
    priority: int = 100
    project_pattern: str = "*"
    reason: str = ""

    def matches(self, action: str, project: str) -> bool:
        return fnmatch(action, self.action_pattern) and fnmatch(project, self.project_pattern)


class Constitution:
    """Deterministic owner policy. First matching rule wins; default is approval."""

    def __init__(self, rules: Iterable[PolicyRule] = (), *, default_decision: Decision = Decision.REQUIRE_APPROVAL) -> None:
        self._rules = sorted(list(rules), key=lambda r: (r.priority, r.rule_id))
        self.default_decision = default_decision

    def evaluate(self, action: str, *, project: str = "*") -> tuple[Decision, str]:
        action = action.strip()
        project = project.strip() or "*"
        if not action:
            return Decision.DENY, "empty action is invalid"
        for rule in self._rules:
            if rule.matches(action, project):
                return rule.decision, rule.reason or f"matched rule {rule.rule_id}"
        return self.default_decision, "no matching rule"

    @property
    def rules(self) -> tuple[PolicyRule, ...]:
        return tuple(self._rules)
