"""Safety-oriented metadata contract for third-party capability discovery."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class PluginVerdict(str, Enum):
    CANDIDATE = "CANDIDATE"
    WATCH = "WATCH"
    SANDBOX_APPROVED = "SANDBOX_APPROVED"
    ADOPTED = "ADOPTED"
    REJECTED = "REJECTED"


class ReviewState(str, Enum):
    NOT_REVIEWED = "NOT_REVIEWED"
    REVIEWED = "REVIEWED"


class LicenseState(str, Enum):
    UNKNOWN = "UNKNOWN_REVIEW_REQUIRED"
    VERIFIED = "VERIFIED"
    INCOMPATIBLE = "INCOMPATIBLE"


@dataclass(frozen=True)
class PermissionProfile:
    filesystem: str = "none"
    network: str = "none"
    credentials: str = "none"
    process_execution: bool = False

    def __post_init__(self) -> None:
        if self.filesystem not in {"none", "read", "write"}:
            raise ValueError("invalid filesystem permission")
        if self.network not in {"none", "restricted", "unrestricted"}:
            raise ValueError("invalid network permission")
        if self.credentials not in {"none", "selected", "broad"}:
            raise ValueError("invalid credentials permission")


@dataclass(frozen=True)
class PluginCandidate:
    plugin_id: str
    upstream: str
    source_catalog: str
    kubera_targets: tuple[str, ...] = field(default_factory=tuple)
    license_state: LicenseState = LicenseState.UNKNOWN
    security_state: ReviewState = ReviewState.NOT_REVIEWED
    permissions: PermissionProfile = field(default_factory=PermissionProfile)
    verdict: PluginVerdict = PluginVerdict.CANDIDATE

    def __post_init__(self) -> None:
        if not self.plugin_id.strip():
            raise ValueError("plugin_id must not be empty")
        if not self.upstream.startswith("https://github.com/"):
            raise ValueError("upstream must be a GitHub HTTPS URL")

    def eligible_for_sandbox(self) -> bool:
        return (
            self.license_state is LicenseState.VERIFIED
            and self.security_state is ReviewState.REVIEWED
            and self.verdict in {PluginVerdict.CANDIDATE, PluginVerdict.WATCH, PluginVerdict.SANDBOX_APPROVED}
        )

    def eligible_for_adoption(self) -> bool:
        return (
            self.license_state is LicenseState.VERIFIED
            and self.security_state is ReviewState.REVIEWED
            and self.verdict is PluginVerdict.ADOPTED
        )

    def to_payload(self) -> dict:
        return {
            "plugin_id": self.plugin_id,
            "upstream": self.upstream,
            "source_catalog": self.source_catalog,
            "kubera_targets": list(self.kubera_targets),
            "license_state": self.license_state.value,
            "security_state": self.security_state.value,
            "permissions": {
                "filesystem": self.permissions.filesystem,
                "network": self.permissions.network,
                "credentials": self.permissions.credentials,
                "process_execution": self.permissions.process_execution,
            },
            "verdict": self.verdict.value,
        }
