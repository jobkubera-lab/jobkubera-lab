from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class VaccineDecision:
    action: str
    rule_id: str | None
    reason: str


class FailureVaccineRegistry:
    """Explicit preventive rules learned from validated failures."""

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""CREATE TABLE IF NOT EXISTS vaccines (
            rule_id TEXT PRIMARY KEY, trigger_type TEXT NOT NULL, pattern TEXT NOT NULL,
            action TEXT NOT NULL, reason TEXT NOT NULL, severity TEXT NOT NULL, created_at TEXT NOT NULL
        )""")
        self.conn.commit()

    @staticmethod
    def _ts() -> str:
        return datetime.now(timezone.utc).isoformat()

    def add_rule(self, rule_id: str, *, trigger_type: str, pattern: str, action: str = "BLOCK", reason: str, severity: str = "HIGH") -> None:
        if trigger_type not in {"exact", "contains", "regex"}:
            raise ValueError("unsupported trigger_type")
        if action not in {"WARN", "BLOCK"}:
            raise ValueError("action must be WARN or BLOCK")
        if trigger_type == "regex":
            re.compile(pattern)
        self.conn.execute("INSERT INTO vaccines VALUES (?,?,?,?,?,?,?)", (rule_id, trigger_type, pattern, action, reason, severity, self._ts()))
        self.conn.commit()

    @staticmethod
    def _matches(trigger_type: str, pattern: str, event: str) -> bool:
        if trigger_type == "exact":
            return event == pattern
        if trigger_type == "contains":
            return pattern in event
        return re.search(pattern, event) is not None

    def check(self, event: str) -> VaccineDecision:
        rows = self.conn.execute("SELECT * FROM vaccines ORDER BY CASE action WHEN 'BLOCK' THEN 0 ELSE 1 END, rule_id").fetchall()
        for row in rows:
            if self._matches(row["trigger_type"], row["pattern"], event):
                return VaccineDecision(row["action"], row["rule_id"], row["reason"])
        return VaccineDecision("ALLOW", None, "no vaccine rule matched")

    def regression_test_template(self, rule_id: str) -> str:
        row = self.conn.execute("SELECT * FROM vaccines WHERE rule_id=?", (rule_id,)).fetchone()
        if not row:
            raise KeyError(rule_id)
        return (f"# Regression test for {rule_id}\n# Trigger: {row['trigger_type']} {row['pattern']!r}\n# Expected action: {row['action']}\ndef test_prevent_known_failure():\n    # Arrange a scenario that reproduces the validated failure.\n    # Assert the preventive gate stops or warns before side effects.\n    raise NotImplementedError\n")

    def close(self) -> None:
        self.conn.close()
