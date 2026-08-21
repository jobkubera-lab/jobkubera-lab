"""Cumulative budget for a series of external provider calls."""
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class ProviderSeriesBudget:
    max_calls: int
    max_tokens: int
    expires_at: datetime | None = None
    used_calls: int = 0
    used_tokens: int = 0

    def consume(self, *, tokens: int, now: datetime | None = None) -> None:
        if tokens <= 0: raise ValueError("tokens must be positive")
        now = now or datetime.now(timezone.utc)
        if self.expires_at is not None:
            if self.expires_at.tzinfo is None: raise ValueError("expires_at must be timezone-aware")
            if now >= self.expires_at: raise PermissionError("provider series budget expired")
        if self.used_calls + 1 > self.max_calls: raise PermissionError("provider call budget exhausted")
        if self.used_tokens + tokens > self.max_tokens: raise PermissionError("provider token budget exhausted")
        self.used_calls += 1; self.used_tokens += tokens

    @property
    def remaining_calls(self) -> int: return self.max_calls - self.used_calls
    @property
    def remaining_tokens(self) -> int: return self.max_tokens - self.used_tokens
