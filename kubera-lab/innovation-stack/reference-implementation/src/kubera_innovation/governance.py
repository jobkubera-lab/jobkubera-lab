from __future__ import annotations

from dataclasses import dataclass

from .authority import AuthorityBudget, ControlLevel
from .constitution import Constitution, Decision


@dataclass(frozen=True)
class AuthorizationResult:
    allowed: bool
    requires_approval: bool
    reason: str
    remaining: int | None = None


class GovernanceGate:
    """Combines permanent owner policy with temporary consumable authority."""

    def __init__(self, constitution: Constitution, budget: AuthorityBudget) -> None:
        self.constitution = constitution
        self.budget = budget

    def authorize(self, action: str, capability: str, *, project: str = "*", required_level: ControlLevel = ControlLevel.ACT, amount: int = 1) -> AuthorizationResult:
        policy, reason = self.constitution.evaluate(action, project=project)
        if policy is Decision.DENY:
            return AuthorizationResult(False, False, f"constitution denied: {reason}")
        if policy is Decision.REQUIRE_APPROVAL:
            return AuthorizationResult(False, True, f"human approval required: {reason}")
        grant = self.budget.consume(capability, required_level=required_level, amount=amount)
        return AuthorizationResult(grant.allowed, False, grant.reason if grant.allowed else f"authority denied: {grant.reason}", grant.remaining)
