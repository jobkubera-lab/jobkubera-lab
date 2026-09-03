"""Signed human-authorization grants for external PROJECT context sharing.

Reference implementation: HMAC proves that a grant came from the trusted local
authority component holding the signing key. Production deployments should keep
that key outside application source/config and may replace HMAC with a hardware-
backed or asymmetric signer.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
from uuid import uuid4


@dataclass(frozen=True)
class AuthorizationGrant:
    grant_id: str
    scope: str
    subject: str
    issued_at: str
    expires_at: str
    signature: str

    def unsigned_payload(self) -> dict:
        return {
            "grant_id": self.grant_id,
            "scope": self.scope,
            "subject": self.subject,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
        }

    def to_payload(self) -> dict:
        return {**self.unsigned_payload(), "signature": self.signature}


class AuthorizationSigner:
    def __init__(self, secret: bytes):
        if len(secret) < 32:
            raise ValueError("authorization signing secret must be at least 32 bytes")
        self._secret = secret

    def _sign_payload(self, payload: dict) -> str:
        data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hmac.new(self._secret, data, hashlib.sha256).hexdigest()

    def issue(self, *, scope: str, subject: str, ttl_seconds: int = 300) -> AuthorizationGrant:
        if not scope.strip() or not subject.strip():
            raise ValueError("scope and subject must not be empty")
        if not 1 <= ttl_seconds <= 3600:
            raise ValueError("ttl_seconds must be between 1 and 3600")
        now = datetime.now(timezone.utc)
        payload = {
            "grant_id": str(uuid4()),
            "scope": scope,
            "subject": subject,
            "issued_at": now.isoformat().replace("+00:00", "Z"),
            "expires_at": (now + timedelta(seconds=ttl_seconds)).isoformat().replace("+00:00", "Z"),
        }
        return AuthorizationGrant(**payload, signature=self._sign_payload(payload))

    def verify(self, grant: AuthorizationGrant, *, required_scope: str, subject: str, now: datetime | None = None) -> bool:
        try:
            expected = self._sign_payload(grant.unsigned_payload())
            if not hmac.compare_digest(expected, grant.signature):
                return False
            if grant.scope != required_scope or grant.subject != subject:
                return False
            now = now or datetime.now(timezone.utc)
            expiry = datetime.fromisoformat(grant.expires_at.replace("Z", "+00:00"))
            issued = datetime.fromisoformat(grant.issued_at.replace("Z", "+00:00"))
            if issued.tzinfo is None or expiry.tzinfo is None or now.tzinfo is None:
                return False
            return issued <= now < expiry
        except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
            return False
