"""Tool-call safety primitives for the KUBERA reference runtime.

These small, dependency-free components were adapted from the supplied engineering
pack, then hardened to fit the existing KUBERA governance model. They do not
replace AuthorityBudget/GovernanceGate, EvidenceLedger, or FailureVaccineRegistry.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
import time
from typing import Any, Mapping

_REDACTED = "***REDACTED***"


@dataclass(frozen=True)
class SecretScanResult:
    value: Any
    redacted_paths: tuple[str, ...]

    @property
    def clean(self) -> bool:
        return not self.redacted_paths


class PrivacyGate:
    """Redact likely credentials from nested tool parameters before outbound use."""

    _KEY_PATTERN = re.compile(
        r"(?:api[_-]?key|password|passwd|secret|token|authorization|credential)",
        re.IGNORECASE,
    )
    _VALUE_PATTERNS = (
        re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}", re.IGNORECASE),
        re.compile(r"\bsk-(?:live_|test_)?[A-Za-z0-9_-]{12,}\b", re.IGNORECASE),
        re.compile(r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^\s]+", re.IGNORECASE),
    )

    @classmethod
    def _redact_string(cls, key: str | None, value: str) -> tuple[str, bool]:
        if key and cls._KEY_PATTERN.search(key):
            return _REDACTED, True
        redacted = value
        changed = False
        for pattern in cls._VALUE_PATTERNS:
            updated, count = pattern.subn(_REDACTED, redacted)
            if count:
                changed = True
                redacted = updated
        return redacted, changed

    @classmethod
    def sanitize(cls, value: Any) -> SecretScanResult:
        paths: list[str] = []

        def walk(item: Any, path: str, key: str | None = None) -> Any:
            if isinstance(item, str):
                redacted, changed = cls._redact_string(key, item)
                if changed:
                    paths.append(path or "$value")
                return redacted
            if isinstance(item, Mapping):
                result: dict[Any, Any] = {}
                for child_key, child_value in item.items():
                    child_path = f"{path}.{child_key}" if path else str(child_key)
                    result[child_key] = walk(child_value, child_path, str(child_key))
                return result
            if isinstance(item, list):
                return [walk(child, f"{path}[{index}]", key) for index, child in enumerate(item)]
            if isinstance(item, tuple):
                return tuple(walk(child, f"{path}[{index}]", key) for index, child in enumerate(item))
            return item

        sanitized = walk(value, "")
        return SecretScanResult(sanitized, tuple(paths))


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    error: str | None = None


class ToolValidator:
    """Strict validator for the JSON-Schema subset used by reference tools."""

    _PYTHON_TYPES = {
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
        "array": list,
        "object": dict,
        "null": type(None),
    }

    @classmethod
    def validate(cls, params: Mapping[str, Any], schema: Mapping[str, Any]) -> ValidationResult:
        if schema.get("type", "object") != "object":
            return ValidationResult(False, "tool input schema must have type=object")
        if not isinstance(params, Mapping):
            return ValidationResult(False, "tool params must be an object")

        required = schema.get("required", [])
        for field in required:
            if field not in params:
                return ValidationResult(False, f"missing required field: {field}")

        properties = schema.get("properties", {})
        allow_extra = schema.get("additionalProperties", False)
        for key, value in params.items():
            if key not in properties:
                if not allow_extra:
                    return ValidationResult(False, f"unexpected field: {key}")
                continue
            rule = properties[key]
            expected = rule.get("type")
            if expected:
                py_type = cls._PYTHON_TYPES.get(expected)
                if py_type is None:
                    return ValidationResult(False, f"unsupported schema type: {expected}")
                if expected in {"number", "integer"} and isinstance(value, bool):
                    return ValidationResult(False, f"field '{key}' must be {expected}")
                if not isinstance(value, py_type):
                    return ValidationResult(False, f"field '{key}' must be {expected}")
            if "enum" in rule and value not in rule["enum"]:
                return ValidationResult(False, f"field '{key}' must be one of {rule['enum']}")
        return ValidationResult(True)


class ToolLoopGuard:
    """Fail closed when a tool loop exceeds iteration or wall-clock budgets."""

    def __init__(self, *, max_iterations: int = 32, timeout_seconds: float = 60.0) -> None:
        if max_iterations <= 0:
            raise ValueError("max_iterations must be positive")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.max_iterations = max_iterations
        self.timeout_seconds = timeout_seconds
        self._iterations = 0
        self._started_at: float | None = None

    def start(self) -> None:
        self._iterations = 0
        self._started_at = time.monotonic()

    def step(self) -> None:
        if self._started_at is None:
            raise RuntimeError("tool loop guard must be started before step()")
        self._iterations += 1
        if self._iterations > self.max_iterations:
            raise RuntimeError("tool loop iteration budget exhausted")
        if time.monotonic() - self._started_at > self.timeout_seconds:
            raise TimeoutError("tool loop time budget exhausted")

    @property
    def iterations(self) -> int:
        return self._iterations
