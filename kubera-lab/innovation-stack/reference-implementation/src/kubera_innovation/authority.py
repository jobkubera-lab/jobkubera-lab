from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from typing import Mapping


class ControlLevel(IntEnum):
    READ = 0
    CREATE = 1
    ACT = 2
    ADMIN = 3


@dataclass(frozen=True)
class GrantDecision:
    allowed: bool
    reason: str
    remaining: int | None = None


@dataclass
class AuthorityBudget:
    """Temporary consumable authority grant. Omitted capabilities are denied."""

    level: ControlLevel
    limits: Mapping[str, int]
    expires_at: datetime | None = None
    _used: dict[str, int] = field(default_factory=dict, init=False, repr=False)

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def is_expired(self, now: datetime | None = None) -> bool:
        if self.expires_at is None:
            return False
        now = now or self._now()
        if self.expires_at.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware")
        return now >= self.expires_at

    def can_consume(self, capability: str, *, required_level: ControlLevel = ControlLevel.ACT, amount: int = 1, now: datetime | None = None) -> GrantDecision:
        if amount <= 0:
            return GrantDecision(False, "amount must be positive")
        if self.is_expired(now):
            return GrantDecision(False, "authority grant expired")
        if self.level < required_level:
            return GrantDecision(False, f"requires {required_level.name}")
        if capability not in self.limits:
            return GrantDecision(False, "capability not granted")
        limit = int(self.limits[capability])
        used = self._used.get(capability, 0)
        remaining = limit - used
        if remaining < amount:
            return GrantDecision(False, "authority budget exhausted", max(remaining, 0))
        return GrantDecision(True, "allowed", remaining - amount)

    def consume(self, capability: str, *, required_level: ControlLevel = ControlLevel.ACT, amount: int = 1, now: datetime | None = None) -> GrantDecision:
        decision = self.can_consume(capability, required_level=required_level, amount=amount, now=now)
        if decision.allowed:
            self._used[capability] = self._used.get(capability, 0) + amount
        return decision

    def used(self, capability: str) -> int:
        return self._used.get(capability, 0)
