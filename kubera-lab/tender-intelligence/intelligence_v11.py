from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class DeadlineAssessment:
    status: str
    days_remaining: int | None
    urgency_score: int
    message: str


@dataclass(frozen=True)
class RequirementFinding:
    text: str
    category: str
    confidence: float
    reason: str


@dataclass(frozen=True)
class GapItem:
    requirement: str
    status: str
    evidence: list[str]
    action: str


@dataclass(frozen=True)
class BuyerInsight:
    buyer: str
    known_awards: int
    recurring_suppliers: list[str]
    notes: list[str]


MANDATORY_MARKERS = (
    "must",
    "shall",
    "required",
    "mandatory",
    "minimum",
    "essential",
    "pass/fail",
    "condition of participation",
)
DESIRABLE_MARKERS = (
    "should",
    "desirable",
    "preferred",
    "advantageous",
    "nice to have",
)


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    candidate = value.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def assess_deadline(deadline: str | None, *, now: datetime | None = None) -> DeadlineAssessment:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    target = _parse_iso(deadline)
    if target is None:
        return DeadlineAssessment("UNKNOWN", None, 0, "Deadline missing or invalid")
    days = (target - now).days
    if target <= now:
        return DeadlineAssessment("CLOSED", days, -100, "Deadline has passed")
    if days <= 2:
        return DeadlineAssessment("CRITICAL", days, -20, "Less than 72 hours remain")
    if days <= 7:
        return DeadlineAssessment("URGENT", days, -10, "One week or less remains")
    if days <= 21:
        return DeadlineAssessment("ACTIVE", days, 5, "Enough time for structured bid review")
    return DeadlineAssessment("EARLY", days, 8, "Good lead time for qualification and evidence gathering")


def cpv_match(cpv_codes: Iterable[str], cpv_map: dict[str, list[str]]) -> dict[str, Any]:
    codes = [str(c).replace("-", "").strip() for c in cpv_codes]
    matched: dict[str, list[str]] = {}
    for capability, prefixes in cpv_map.items():
        hits = [code for code in codes if any(code.startswith(str(prefix).replace("-", "")) for prefix in prefixes)]
        if hits:
            matched[capability] = sorted(set(hits))
    return {
        "matched_capabilities": sorted(matched),
        "matches": matched,
        "match_count": sum(len(v) for v in matched.values()),
    }


def verify_requirements(requirements: Iterable[str]) -> list[RequirementFinding]:
    findings: list[RequirementFinding] = []
    for raw in requirements:
        text = str(raw).strip()
        if not text:
            continue
        lowered = text.lower()
        mandatory = [m for m in MANDATORY_MARKERS if m in lowered]
        desirable = [m for m in DESIRABLE_MARKERS if m in lowered]
        if mandatory:
            findings.append(RequirementFinding(text, "MANDATORY", 0.92, f"Matched mandatory marker(s): {', '.join(mandatory)}"))
        elif desirable:
            findings.append(RequirementFinding(text, "DESIRABLE", 0.82, f"Matched desirable marker(s): {', '.join(desirable)}"))
        else:
            findings.append(RequirementFinding(text, "REVIEW", 0.55, "No deterministic mandatory/desirable marker found"))
    return findings


def win_gap_analysis(
    requirement_findings: Iterable[RequirementFinding],
    capability_evidence: dict[str, list[str]],
    *,
    evidence_keywords: dict[str, list[str]] | None = None,
) -> list[GapItem]:
    evidence_keywords = evidence_keywords or {}
    gaps: list[GapItem] = []
    for finding in requirement_findings:
        lowered = finding.text.lower()
        evidence: list[str] = []
        for capability, keywords in evidence_keywords.items():
            if any(keyword.lower() in lowered for keyword in keywords):
                evidence.extend(capability_evidence.get(capability, []))
        evidence = sorted(set(evidence))
        if evidence:
            status = "EVIDENCED"
            action = "Reference evidence in the bid response and confirm scope matches the requirement."
        elif finding.category == "MANDATORY":
            status = "GAP"
            action = "Obtain evidence, partner capability or do not bid if this remains a mandatory unmet condition."
        else:
            status = "REVIEW"
            action = "Confirm whether this criterion materially affects scoring and prepare evidence if useful."
        gaps.append(GapItem(finding.text, status, evidence, action))
    return gaps


def build_buyer_insight(buyer: str, award_records: Iterable[dict[str, Any]]) -> BuyerInsight:
    buyer_key = buyer.strip().lower()
    suppliers: dict[str, int] = {}
    count = 0
    notes: list[str] = []
    for record in award_records:
        record_buyer = str(record.get("buyer") or "").strip().lower()
        if buyer_key and record_buyer != buyer_key:
            continue
        count += 1
        for supplier in record.get("suppliers", []) or []:
            name = str(supplier).strip()
            if name:
                suppliers[name] = suppliers.get(name, 0) + 1
    recurring = [name for name, n in sorted(suppliers.items(), key=lambda x: (-x[1], x[0].lower())) if n >= 2]
    if count == 0:
        notes.append("No local award-history evidence supplied for this buyer")
    elif recurring:
        notes.append("Recurring suppliers detected in supplied award history")
    else:
        notes.append("Award history supplied, but no recurring supplier detected")
    return BuyerInsight(buyer, count, recurring, notes)


def generate_bid_pack(
    opportunity: dict[str, Any],
    decision: dict[str, Any],
    deadline: DeadlineAssessment,
    requirements: list[RequirementFinding],
    gaps: list[GapItem],
    buyer: BuyerInsight,
    cpv: dict[str, Any],
) -> dict[str, Any]:
    mandatory = [asdict(r) for r in requirements if r.category == "MANDATORY"]
    desirable = [asdict(r) for r in requirements if r.category == "DESIRABLE"]
    review = [asdict(r) for r in requirements if r.category == "REVIEW"]
    open_gaps = [asdict(g) for g in gaps if g.status == "GAP"]
    return {
        "status": "DRAFT_ONLY",
        "human_approval_required": True,
        "opportunity": {
            "title": opportunity.get("title"),
            "buyer": opportunity.get("buyer"),
            "source_url": opportunity.get("source_url"),
            "notice_id": opportunity.get("notice_id"),
            "deadline": opportunity.get("deadline"),
        },
        "qualification": decision,
        "deadline_intelligence": asdict(deadline),
        "cpv_intelligence": cpv,
        "buyer_intelligence": asdict(buyer),
        "requirements": {
            "mandatory": mandatory,
            "desirable": desirable,
            "review": review,
        },
        "win_gap_analysis": [asdict(g) for g in gaps],
        "go_no_go_checklist": [
            "Confirm all mandatory conditions are met",
            "Confirm delivery capacity and subcontracting assumptions",
            "Confirm insurance/certification requirements",
            "Confirm pricing model and contract value are commercially viable",
            "Confirm deadline leaves enough time for a compliant response",
            "Confirm evidence links are current and truthful",
            "Human approves BID / REVIEW / NO-BID decision",
        ],
        "draft_response_sections": [
            "Executive summary",
            "Understanding of the requirement",
            "Delivery approach",
            "Evidence and relevant experience",
            "Security, privacy and governance",
            "Implementation plan and milestones",
            "Quality assurance and human oversight",
            "Commercial response",
            "Risks and mitigations",
        ],
        "blockers_before_bid": open_gaps,
    }


def load_checkpoint(path: str | Path) -> dict[str, Any]:
    file = Path(path)
    if not file.exists():
        return {"version": 1, "sources": {}}
    with file.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("Checkpoint must be a JSON object")
    data.setdefault("version", 1)
    data.setdefault("sources", {})
    return data


def save_checkpoint(path: str | Path, checkpoint: dict[str, Any]) -> None:
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    temp = file.with_suffix(file.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as fh:
        json.dump(checkpoint, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
    temp.replace(file)


def update_checkpoint(
    checkpoint: dict[str, Any],
    *,
    source: str,
    cursor: str | None,
    high_watermark: str | None,
    processed: int,
) -> dict[str, Any]:
    checkpoint = json.loads(json.dumps(checkpoint))
    sources = checkpoint.setdefault("sources", {})
    sources[source] = {
        "cursor": cursor,
        "high_watermark": high_watermark,
        "processed": int(processed),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    return checkpoint
