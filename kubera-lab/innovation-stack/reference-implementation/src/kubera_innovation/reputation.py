from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class ReputationSummary:
    subject_id: str
    dimensions: dict[str, float]
    overall: float
    verified_events: int


class ReputationEngine:
    """Evidence-weighted reputation. Only verified events affect scores."""

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""CREATE TABLE IF NOT EXISTS reputation_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, subject_id TEXT NOT NULL,
            dimension TEXT NOT NULL, score REAL NOT NULL, weight REAL NOT NULL,
            verified INTEGER NOT NULL, evidence_ref TEXT, created_at TEXT NOT NULL
        )""")
        self.conn.commit()

    @staticmethod
    def _ts() -> str:
        return datetime.now(timezone.utc).isoformat()

    def record(self, subject_id: str, dimension: str, score: float, *, weight: float = 1.0, verified: bool, evidence_ref: str | None = None) -> None:
        if not 0.0 <= score <= 1.0:
            raise ValueError("score must be between 0 and 1")
        if weight <= 0:
            raise ValueError("weight must be positive")
        if not subject_id or not dimension:
            raise ValueError("subject_id and dimension are required")
        self.conn.execute("INSERT INTO reputation_events(subject_id,dimension,score,weight,verified,evidence_ref,created_at) VALUES(?,?,?,?,?,?,?)", (subject_id, dimension, score, weight, 1 if verified else 0, evidence_ref, self._ts()))
        self.conn.commit()

    def summary(self, subject_id: str) -> ReputationSummary:
        rows = self.conn.execute("SELECT dimension, SUM(score*weight)/SUM(weight) AS weighted_score, COUNT(*) AS n FROM reputation_events WHERE subject_id=? AND verified=1 GROUP BY dimension ORDER BY dimension", (subject_id,)).fetchall()
        dimensions = {r["dimension"]: round(float(r["weighted_score"]), 4) for r in rows}
        total_events = sum(int(r["n"]) for r in rows)
        overall = round(sum(dimensions.values()) / len(dimensions), 4) if dimensions else 0.0
        return ReputationSummary(subject_id, dimensions, overall, total_events)

    def close(self) -> None:
        self.conn.close()
