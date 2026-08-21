from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VALID_VISIBILITY = {"PRIVATE", "PROJECT", "PUBLIC"}


@dataclass(frozen=True)
class Node:
    node_id: str
    node_type: str
    label: str
    visibility: str
    metadata: dict[str, Any]


class RealityGraph:
    """Small SQLite-backed graph with explicit visibility labels."""

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY, node_type TEXT NOT NULL, label TEXT NOT NULL,
                visibility TEXT NOT NULL, metadata_json TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS edges (
                edge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL, relation TEXT NOT NULL, target_id TEXT NOT NULL,
                metadata_json TEXT NOT NULL, created_at TEXT NOT NULL,
                UNIQUE(source_id, relation, target_id),
                FOREIGN KEY(source_id) REFERENCES nodes(node_id),
                FOREIGN KEY(target_id) REFERENCES nodes(node_id)
            );
        """)
        self.conn.commit()

    @staticmethod
    def _ts() -> str:
        return datetime.now(timezone.utc).isoformat()

    def add_node(self, node_id: str, node_type: str, label: str, *, visibility: str = "PROJECT", metadata: dict[str, Any] | None = None) -> None:
        if visibility not in VALID_VISIBILITY:
            raise ValueError(f"invalid visibility: {visibility}")
        if not node_id or not node_type or not label:
            raise ValueError("node_id, node_type and label are required")
        self.conn.execute("INSERT INTO nodes(node_id,node_type,label,visibility,metadata_json,created_at) VALUES(?,?,?,?,?,?)", (node_id, node_type, label, visibility, json.dumps(metadata or {}, sort_keys=True), self._ts()))
        self.conn.commit()

    def add_edge(self, source_id: str, relation: str, target_id: str, *, metadata: dict[str, Any] | None = None) -> None:
        if not relation:
            raise ValueError("relation is required")
        known = self.conn.execute("SELECT node_id FROM nodes WHERE node_id IN (?,?)", (source_id, target_id)).fetchall()
        if len({r["node_id"] for r in known}) != 2:
            raise KeyError("both source and target nodes must exist")
        self.conn.execute("INSERT INTO edges(source_id,relation,target_id,metadata_json,created_at) VALUES(?,?,?,?,?)", (source_id, relation, target_id, json.dumps(metadata or {}, sort_keys=True), self._ts()))
        self.conn.commit()

    def get_node(self, node_id: str) -> Node | None:
        row = self.conn.execute("SELECT * FROM nodes WHERE node_id=?", (node_id,)).fetchone()
        if not row:
            return None
        return Node(row["node_id"], row["node_type"], row["label"], row["visibility"], json.loads(row["metadata_json"]))

    def neighbors(self, node_id: str, *, relation: str | None = None) -> list[Node]:
        sql = "SELECT n.* FROM edges e JOIN nodes n ON n.node_id=e.target_id WHERE e.source_id=?"
        params: list[Any] = [node_id]
        if relation is not None:
            sql += " AND e.relation=?"
            params.append(relation)
        sql += " ORDER BY n.node_id"
        rows = self.conn.execute(sql, params).fetchall()
        return [Node(r["node_id"], r["node_type"], r["label"], r["visibility"], json.loads(r["metadata_json"])) for r in rows]

    def export_public(self) -> dict[str, list[dict[str, Any]]]:
        nodes = self.conn.execute("SELECT * FROM nodes WHERE visibility='PUBLIC' ORDER BY node_id").fetchall()
        node_ids = {r["node_id"] for r in nodes}
        edges = self.conn.execute("SELECT * FROM edges ORDER BY edge_id").fetchall()
        return {
            "nodes": [{"id": r["node_id"], "type": r["node_type"], "label": r["label"], "metadata": json.loads(r["metadata_json"])} for r in nodes],
            "edges": [{"source": r["source_id"], "relation": r["relation"], "target": r["target_id"], "metadata": json.loads(r["metadata_json"])} for r in edges if r["source_id"] in node_ids and r["target_id"] in node_ids],
        }

    def close(self) -> None:
        self.conn.close()
