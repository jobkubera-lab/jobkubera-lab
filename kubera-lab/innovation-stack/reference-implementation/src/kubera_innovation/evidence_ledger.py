"""Append-only local Evidence Ledger with hash-chained records."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import sqlite3
from typing import Any, Optional
from uuid import uuid4


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class EvidenceEntry:
    entry_id: str
    run_id: str
    stage: str
    timestamp: str
    input_hash: str
    output_hash: str
    previous_hash: str
    entry_hash: str
    metadata: dict[str, Any]


class EvidenceLedger:
    """SQLite-backed append-only ledger for deterministic workflow evidence.

    This is a reference integrity mechanism, not a cryptographic signature system.
    A production implementation should add signed checkpoints and protected storage.
    """

    GENESIS_HASH = "GENESIS"

    def __init__(self, path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS evidence (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id TEXT NOT NULL UNIQUE,
                run_id TEXT NOT NULL,
                stage TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                input_hash TEXT NOT NULL,
                output_hash TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                entry_hash TEXT NOT NULL UNIQUE,
                metadata_json TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    @staticmethod
    def hash_value(value: Any) -> str:
        return "sha256:" + sha256(_canonical_json(value).encode("utf-8")).hexdigest()

    def _last_hash(self) -> str:
        row = self._conn.execute(
            "SELECT entry_hash FROM evidence ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        return row[0] if row else self.GENESIS_HASH

    def append(
        self,
        *,
        run_id: str,
        stage: str,
        input_value: Any,
        output_value: Any,
        metadata: Optional[dict[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> EvidenceEntry:
        if not run_id.strip() or not stage.strip():
            raise ValueError("run_id and stage must not be empty")
        metadata = dict(metadata or {})
        ts = timestamp or _utc_now()
        input_hash = self.hash_value(input_value)
        output_hash = self.hash_value(output_value)
        previous_hash = self._last_hash()
        entry_id = str(uuid4())
        envelope = {
            "entry_id": entry_id,
            "run_id": run_id,
            "stage": stage,
            "timestamp": ts,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "previous_hash": previous_hash,
            "metadata": metadata,
        }
        entry_hash = "sha256:" + sha256(_canonical_json(envelope).encode("utf-8")).hexdigest()
        self._conn.execute(
            """
            INSERT INTO evidence
            (entry_id, run_id, stage, timestamp, input_hash, output_hash, previous_hash, entry_hash, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry_id,
                run_id,
                stage,
                ts,
                input_hash,
                output_hash,
                previous_hash,
                entry_hash,
                _canonical_json(metadata),
            ),
        )
        self._conn.commit()
        return EvidenceEntry(
            entry_id,
            run_id,
            stage,
            ts,
            input_hash,
            output_hash,
            previous_hash,
            entry_hash,
            metadata,
        )

    def entries(self, run_id: Optional[str] = None) -> list[EvidenceEntry]:
        query = "SELECT entry_id, run_id, stage, timestamp, input_hash, output_hash, previous_hash, entry_hash, metadata_json FROM evidence"
        params: tuple[Any, ...] = ()
        if run_id is not None:
            query += " WHERE run_id = ?"
            params = (run_id,)
        query += " ORDER BY sequence ASC"
        rows = self._conn.execute(query, params).fetchall()
        return [
            EvidenceEntry(*row[:-1], json.loads(row[-1]))
            for row in rows
        ]

    def verify_chain(self) -> bool:
        rows = self._conn.execute(
            "SELECT entry_id, run_id, stage, timestamp, input_hash, output_hash, previous_hash, entry_hash, metadata_json FROM evidence ORDER BY sequence ASC"
        ).fetchall()
        expected_previous = self.GENESIS_HASH
        for row in rows:
            entry_id, run_id, stage, ts, input_hash, output_hash, previous_hash, entry_hash, metadata_json = row
            if previous_hash != expected_previous:
                return False
            envelope = {
                "entry_id": entry_id,
                "run_id": run_id,
                "stage": stage,
                "timestamp": ts,
                "input_hash": input_hash,
                "output_hash": output_hash,
                "previous_hash": previous_hash,
                "metadata": json.loads(metadata_json),
            }
            recomputed = "sha256:" + sha256(_canonical_json(envelope).encode("utf-8")).hexdigest()
            if recomputed != entry_hash:
                return False
            expected_previous = entry_hash
        return True

    def close(self) -> None:
        self._conn.close()
