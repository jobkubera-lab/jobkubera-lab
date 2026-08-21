"""Provider/runtime-neutral execution interface inspired by durable agent/workflow patterns."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Protocol
from uuid import uuid4


class RunStatus(str, Enum):
    READY="ready"; RUNNING="running"; PAUSED="paused"; COMPLETED="completed"; FAILED="failed"

@dataclass(frozen=True)
class RuntimeCheckpoint:
    checkpoint_id: str
    run_id: str
    status: RunStatus
    state_hash: str

@dataclass(frozen=True)
class RuntimeResult:
    run_id: str
    status: RunStatus
    output: dict
    checkpoint: RuntimeCheckpoint | None = None

class RuntimeAdapter(Protocol):
    """The KUBERA kernel talks to runtimes through this surface, not vendor APIs directly."""
    name: str
    def execute(self, *, run_id: str, input_payload: dict) -> RuntimeResult: ...
    def checkpoint(self, *, run_id: str) -> RuntimeCheckpoint: ...
    def resume(self, *, checkpoint_id: str) -> RuntimeResult: ...


def new_run_id() -> str:
    return str(uuid4())
