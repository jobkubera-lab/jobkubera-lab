from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkContract:
    """Minimal specialist contract for KUBERA / DZAMBALA work.

    The five fields define what the worker is doing, which source classes it may
    rely on, what judgment it is allowed to exercise, the required output, and
    explicit forbidden actions. An empty ``forbidden`` boundary is not sufficient
    authority for irreversible execution.
    """

    job: str
    sources: tuple[str, ...]
    judgment: str
    output: str
    forbidden: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.job.strip():
            raise ValueError("job must not be empty")
        if not self.judgment.strip():
            raise ValueError("judgment must not be empty")
        if not self.output.strip():
            raise ValueError("output must not be empty")
        if not self.sources or any(not str(item).strip() for item in self.sources):
            raise ValueError("sources must contain at least one non-empty source rule")
        if any(not str(item).strip() for item in self.forbidden):
            raise ValueError("forbidden rules must not contain empty values")

    @property
    def irreversible_boundary_declared(self) -> bool:
        return bool(self.forbidden)

    def forbids(self, operation: str) -> bool:
        name = operation.strip().casefold()
        rules = {item.strip().casefold() for item in self.forbidden}
        return "*" in rules or name in rules
