from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import unified_diff
from enum import Enum
from pathlib import Path


class ImprovementArtifact(str, Enum):
    RULE = "rule"
    SKILL = "skill"
    GATE = "gate"
    DOC = "doc"


class ProposalStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    DISMISSED = "dismissed"


class AgentState(str, Enum):
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    FINISHED = "finished"
    FAILED = "failed"
    IDLE = "idle"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PromotionThreshold:
    min_signals: int = 3
    min_conversations: int = 2
    min_pain: int = 3

    def __post_init__(self) -> None:
        if min(self.min_signals, self.min_conversations, self.min_pain) < 1:
            raise ValueError("promotion thresholds must be positive")


@dataclass(frozen=True)
class CorrectionSignal:
    signal_id: str
    conversation_id: str
    fingerprint: str
    summary: str
    artifact: ImprovementArtifact = ImprovementArtifact.RULE
    pain: int = 1

    def __post_init__(self) -> None:
        for name, value in (
            ("signal_id", self.signal_id),
            ("conversation_id", self.conversation_id),
            ("fingerprint", self.fingerprint),
            ("summary", self.summary),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        if not 1 <= self.pain <= 5:
            raise ValueError("pain must be between 1 and 5")


@dataclass(frozen=True)
class ClusterStats:
    fingerprint: str
    signal_count: int
    conversation_count: int
    pain_total: int
    signal_ids: tuple[str, ...]
    summaries: tuple[str, ...]


@dataclass(frozen=True)
class ImprovementProposal:
    proposal_id: str
    fingerprint: str
    artifact: ImprovementArtifact
    target_path: str
    proposed_content: str
    evidence_signal_ids: tuple[str, ...]
    conversation_count: int
    pain_total: int
    status: ProposalStatus
    reviewed_by: str | None = None
    reviewed_at: str | None = None


@dataclass(frozen=True)
class AgentSession:
    session_id: str
    harness: str
    task: str
    state: AgentState
    needs_approval: bool
    updated_at: str


class ImprovementRegistry:
    """Local, deterministic improvement loop for KUBERA agent guidance.

    The registry stores compact correction signals rather than full transcripts.
    Repeated evidence can create a proposal, but proposals never write files.
    A human must approve an exact proposal before its change payload can be
    handed to the normal repository workflow.
    """

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS correction_signals (
                signal_id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                fingerprint TEXT NOT NULL,
                summary TEXT NOT NULL,
                artifact TEXT NOT NULL,
                pain INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS improvement_proposals (
                proposal_id TEXT PRIMARY KEY,
                fingerprint TEXT NOT NULL,
                artifact TEXT NOT NULL,
                target_path TEXT NOT NULL,
                proposed_content TEXT NOT NULL,
                evidence_signal_ids TEXT NOT NULL,
                conversation_count INTEGER NOT NULL,
                pain_total INTEGER NOT NULL,
                status TEXT NOT NULL,
                reviewed_by TEXT,
                reviewed_at TEXT,
                created_at TEXT NOT NULL
            )"""
        )
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS agent_sessions (
                session_id TEXT PRIMARY KEY,
                harness TEXT NOT NULL,
                task TEXT NOT NULL,
                state TEXT NOT NULL,
                needs_approval INTEGER NOT NULL,
                updated_at TEXT NOT NULL
            )"""
        )
        self.conn.commit()

    @staticmethod
    def _ts() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _proposal_id(
        fingerprint: str, artifact: ImprovementArtifact, target_path: str, proposed_content: str
    ) -> str:
        payload = "\x1f".join((fingerprint, artifact.value, target_path, proposed_content))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]

    def record_signal(self, signal: CorrectionSignal) -> None:
        try:
            self.conn.execute(
                "INSERT INTO correction_signals VALUES (?,?,?,?,?,?,?)",
                (
                    signal.signal_id,
                    signal.conversation_id,
                    signal.fingerprint,
                    signal.summary,
                    signal.artifact.value,
                    signal.pain,
                    self._ts(),
                ),
            )
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"duplicate signal_id: {signal.signal_id}") from exc
        self.conn.commit()

    def cluster(self, fingerprint: str) -> ClusterStats:
        if not fingerprint.strip():
            raise ValueError("fingerprint must not be empty")
        rows = self.conn.execute(
            """SELECT signal_id, conversation_id, summary, pain
               FROM correction_signals
               WHERE fingerprint=?
               ORDER BY created_at, signal_id""",
            (fingerprint,),
        ).fetchall()
        return ClusterStats(
            fingerprint=fingerprint,
            signal_count=len(rows),
            conversation_count=len({row["conversation_id"] for row in rows}),
            pain_total=sum(int(row["pain"]) for row in rows),
            signal_ids=tuple(row["signal_id"] for row in rows),
            summaries=tuple(row["summary"] for row in rows),
        )

    def maybe_propose(
        self,
        fingerprint: str,
        *,
        artifact: ImprovementArtifact,
        target_path: str,
        proposed_content: str,
        threshold: PromotionThreshold = PromotionThreshold(),
    ) -> ImprovementProposal | None:
        if not target_path.strip():
            raise ValueError("target_path must not be empty")
        if not proposed_content.strip():
            raise ValueError("proposed_content must not be empty")

        stats = self.cluster(fingerprint)
        if (
            stats.signal_count < threshold.min_signals
            or stats.conversation_count < threshold.min_conversations
            or stats.pain_total < threshold.min_pain
        ):
            return None

        proposal_id = self._proposal_id(fingerprint, artifact, target_path, proposed_content)
        existing = self._proposal_row(proposal_id)
        if existing is not None:
            return self._proposal_from_row(existing)

        self.conn.execute(
            "INSERT INTO improvement_proposals VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                proposal_id,
                fingerprint,
                artifact.value,
                target_path,
                proposed_content,
                json.dumps(stats.signal_ids),
                stats.conversation_count,
                stats.pain_total,
                ProposalStatus.PROPOSED.value,
                None,
                None,
                self._ts(),
            ),
        )
        self.conn.commit()
        return self.get_proposal(proposal_id)

    def _proposal_row(self, proposal_id: str) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM improvement_proposals WHERE proposal_id=?", (proposal_id,)
        ).fetchone()

    @staticmethod
    def _proposal_from_row(row: sqlite3.Row) -> ImprovementProposal:
        return ImprovementProposal(
            proposal_id=row["proposal_id"],
            fingerprint=row["fingerprint"],
            artifact=ImprovementArtifact(row["artifact"]),
            target_path=row["target_path"],
            proposed_content=row["proposed_content"],
            evidence_signal_ids=tuple(json.loads(row["evidence_signal_ids"])),
            conversation_count=int(row["conversation_count"]),
            pain_total=int(row["pain_total"]),
            status=ProposalStatus(row["status"]),
            reviewed_by=row["reviewed_by"],
            reviewed_at=row["reviewed_at"],
        )

    def get_proposal(self, proposal_id: str) -> ImprovementProposal:
        row = self._proposal_row(proposal_id)
        if row is None:
            raise KeyError(proposal_id)
        return self._proposal_from_row(row)

    def review(self, proposal_id: str, *, approve: bool, actor: str) -> ImprovementProposal:
        if not actor.strip():
            raise ValueError("actor must not be empty")
        proposal = self.get_proposal(proposal_id)
        if proposal.status is not ProposalStatus.PROPOSED:
            raise ValueError("proposal has already been reviewed")
        status = ProposalStatus.APPROVED if approve else ProposalStatus.DISMISSED
        self.conn.execute(
            """UPDATE improvement_proposals
               SET status=?, reviewed_by=?, reviewed_at=?
               WHERE proposal_id=?""",
            (status.value, actor, self._ts(), proposal_id),
        )
        self.conn.commit()
        return self.get_proposal(proposal_id)

    def preview_diff(self, proposal_id: str, current_content: str) -> str:
        proposal = self.get_proposal(proposal_id)
        before = current_content.splitlines(keepends=True)
        after = proposal.proposed_content.splitlines(keepends=True)
        return "".join(
            unified_diff(
                before,
                after,
                fromfile=f"a/{proposal.target_path}",
                tofile=f"b/{proposal.target_path}",
            )
        )

    def approved_change(self, proposal_id: str) -> dict[str, str]:
        proposal = self.get_proposal(proposal_id)
        if proposal.status is not ProposalStatus.APPROVED:
            raise PermissionError("exact proposal is not human-approved")
        return {
            "proposal_id": proposal.proposal_id,
            "artifact": proposal.artifact.value,
            "target_path": proposal.target_path,
            "proposed_content": proposal.proposed_content,
        }

    def upsert_agent(
        self,
        session_id: str,
        *,
        harness: str,
        task: str,
        state: AgentState,
        needs_approval: bool = False,
    ) -> AgentSession:
        for name, value in (("session_id", session_id), ("harness", harness), ("task", task)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        timestamp = self._ts()
        self.conn.execute(
            """INSERT INTO agent_sessions
               (session_id, harness, task, state, needs_approval, updated_at)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT(session_id) DO UPDATE SET
                   harness=excluded.harness,
                   task=excluded.task,
                   state=excluded.state,
                   needs_approval=excluded.needs_approval,
                   updated_at=excluded.updated_at""",
            (session_id, harness, task, state.value, int(needs_approval), timestamp),
        )
        self.conn.commit()
        return self.get_agent(session_id)

    def get_agent(self, session_id: str) -> AgentSession:
        row = self.conn.execute(
            "SELECT * FROM agent_sessions WHERE session_id=?", (session_id,)
        ).fetchone()
        if row is None:
            raise KeyError(session_id)
        return AgentSession(
            session_id=row["session_id"],
            harness=row["harness"],
            task=row["task"],
            state=AgentState(row["state"]),
            needs_approval=bool(row["needs_approval"]),
            updated_at=row["updated_at"],
        )

    def list_agents(self) -> tuple[AgentSession, ...]:
        rows = self.conn.execute(
            """SELECT * FROM agent_sessions
               ORDER BY needs_approval DESC,
                        CASE state
                            WHEN 'failed' THEN 0
                            WHEN 'waiting_approval' THEN 1
                            WHEN 'running' THEN 2
                            WHEN 'unknown' THEN 3
                            WHEN 'idle' THEN 4
                            ELSE 5
                        END,
                        updated_at DESC,
                        session_id"""
        ).fetchall()
        return tuple(
            AgentSession(
                session_id=row["session_id"],
                harness=row["harness"],
                task=row["task"],
                state=AgentState(row["state"]),
                needs_approval=bool(row["needs_approval"]),
                updated_at=row["updated_at"],
            )
            for row in rows
        )

    def close(self) -> None:
        self.conn.close()
