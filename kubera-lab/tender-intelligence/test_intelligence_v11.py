from datetime import datetime, timezone

from intelligence_v11 import (
    assess_deadline,
    build_buyer_insight,
    cpv_match,
    generate_bid_pack,
    verify_requirements,
    win_gap_analysis,
)


def test_deadline_closed():
    now = datetime(2026, 9, 9, tzinfo=timezone.utc)
    result = assess_deadline("2026-09-01T12:00:00Z", now=now)
    assert result.status == "CLOSED"


def test_deadline_urgent():
    now = datetime(2026, 9, 9, tzinfo=timezone.utc)
    result = assess_deadline("2026-09-14T12:00:00Z", now=now)
    assert result.status == "URGENT"


def test_cpv_prefix_match():
    result = cpv_match(["72262000"], {"web": ["7226"], "data": ["723"]})
    assert result["matched_capabilities"] == ["web"]


def test_requirement_verifier():
    results = verify_requirements([
        "Supplier must hold Cyber Essentials Plus",
        "Experience with local authorities is desirable",
        "Provide an implementation plan",
    ])
    assert results[0].category == "MANDATORY"
    assert results[1].category == "DESIRABLE"
    assert results[2].category == "REVIEW"


def test_gap_analysis_flags_unmet_mandatory():
    reqs = verify_requirements(["Supplier must provide ISO 27001 certification"])
    gaps = win_gap_analysis(reqs, {}, evidence_keywords={"security": ["iso 27001"]})
    assert gaps[0].status == "GAP"


def test_buyer_intelligence_recurring_supplier():
    buyer = build_buyer_insight("Example Council", [
        {"buyer": "Example Council", "suppliers": ["Alpha Ltd"]},
        {"buyer": "Example Council", "suppliers": ["Alpha Ltd", "Beta Ltd"]},
    ])
    assert buyer.known_awards == 2
    assert buyer.recurring_suppliers == ["Alpha Ltd"]


def test_bid_pack_is_draft_only():
    deadline = assess_deadline("2026-10-01T12:00:00Z", now=datetime(2026, 9, 9, tzinfo=timezone.utc))
    reqs = verify_requirements(["Supplier should provide user research experience"])
    gaps = win_gap_analysis(reqs, {"research": ["repo"]}, evidence_keywords={"research": ["research"]})
    buyer = build_buyer_insight("Example Council", [])
    cpv = cpv_match(["79310000"], {"research": ["7931"]})
    pack = generate_bid_pack(
        {"title": "Research", "buyer": "Example Council", "source_url": "https://example", "notice_id": "1", "deadline": "2026-10-01T12:00:00Z"},
        {"decision": "REVIEW", "score": 60},
        deadline,
        reqs,
        gaps,
        buyer,
        cpv,
    )
    assert pack["status"] == "DRAFT_ONLY"
    assert pack["human_approval_required"] is True
