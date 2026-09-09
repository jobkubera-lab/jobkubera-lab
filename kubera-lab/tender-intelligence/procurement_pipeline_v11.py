from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from intelligence_v11 import (
    assess_deadline,
    build_buyer_insight,
    cpv_match,
    generate_bid_pack,
    load_checkpoint,
    save_checkpoint,
    update_checkpoint,
    verify_requirements,
    win_gap_analysis,
)
from procurement_adapter import (
    deduplicate,
    evidence_record,
    fetch_contracts_finder,
    fetch_find_a_tender,
    normalize_package,
)
from tender_intelligence import load_json, score_opportunity


def _next_cursor(package: dict[str, Any]) -> str | None:
    links = package.get("links") or {}
    if isinstance(links, dict):
        for key in ("next", "nextCursor", "next_cursor"):
            value = links.get(key)
            if value:
                return str(value)
    for key in ("nextCursor", "next_cursor"):
        value = package.get(key)
        if value:
            return str(value)
    return None


def _append_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")


def run_v11(
    *,
    source: str,
    profile_path: str | Path,
    v11_config_path: str | Path,
    checkpoint_path: str | Path,
    evidence_path: str | Path | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    limit: int = 100,
    max_pages: int = 5,
    award_history_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    profile = load_json(profile_path)
    v11 = load_json(v11_config_path)
    checkpoint = load_checkpoint(checkpoint_path)
    source_state = checkpoint.get("sources", {}).get(source, {})
    cursor = source_state.get("cursor")
    award_records = []
    if award_history_path and Path(award_history_path).exists():
        loaded = load_json(award_history_path)
        award_records = loaded if isinstance(loaded, list) else loaded.get("awards", [])

    all_opportunities = []
    last_cursor = cursor
    for _page in range(max_pages):
        if source == "find_a_tender":
            package, source_url = fetch_find_a_tender(
                updated_from=updated_from,
                updated_to=updated_to,
                limit=limit,
                cursor=last_cursor,
            )
        elif source == "contracts_finder":
            package, source_url = fetch_contracts_finder(
                published_from=updated_from,
                published_to=updated_to,
                limit=limit,
                cursor=last_cursor,
            )
        else:
            raise ValueError(f"Unsupported source: {source}")

        all_opportunities.extend(normalize_package(package, source=source, source_url=source_url))
        next_cursor = _next_cursor(package)
        if not next_cursor or next_cursor == last_cursor:
            last_cursor = next_cursor
            break
        last_cursor = next_cursor

    normalized = deduplicate(all_opportunities)
    output: list[dict[str, Any]] = []
    ledger_records: list[dict[str, Any]] = []
    high_watermark: str | None = None

    for opportunity in normalized:
        tender_input = opportunity.as_tender_input()
        decision_obj = score_opportunity(tender_input, profile)
        decision = asdict(decision_obj)
        deadline = assess_deadline(opportunity.deadline)
        cpv = cpv_match(opportunity.cpv_codes, v11.get("cpv_map", {}))
        requirements = verify_requirements(opportunity.requirements)
        gaps = win_gap_analysis(
            requirements,
            v11.get("capability_evidence", {}),
            evidence_keywords=v11.get("evidence_keywords", {}),
        )
        buyer = build_buyer_insight(opportunity.buyer, award_records)
        bid_pack = generate_bid_pack(tender_input, decision, deadline, requirements, gaps, buyer, cpv)

        if deadline.status == "CLOSED":
            decision["decision"] = "NO_BID"
            decision.setdefault("review_reasons", []).append("Tender deadline has passed")

        output.append({
            "opportunity": tender_input,
            "decision": decision,
            "deadline_intelligence": asdict(deadline),
            "cpv_intelligence": cpv,
            "requirements": [asdict(r) for r in requirements],
            "win_gap_analysis": [asdict(g) for g in gaps],
            "buyer_intelligence": asdict(buyer),
            "bid_pack": bid_pack,
        })
        ledger_records.append(evidence_record(opportunity))
        if opportunity.published_date and (high_watermark is None or opportunity.published_date > high_watermark):
            high_watermark = opportunity.published_date

    checkpoint = update_checkpoint(
        checkpoint,
        source=source,
        cursor=last_cursor,
        high_watermark=high_watermark or source_state.get("high_watermark"),
        processed=len(normalized),
    )
    save_checkpoint(checkpoint_path, checkpoint)

    if evidence_path is not None and ledger_records:
        _append_jsonl(Path(evidence_path), ledger_records)

    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="KUBERA Tender Intelligence v1.1 pipeline")
    parser.add_argument("--source", choices=["find_a_tender", "contracts_finder"], required=True)
    parser.add_argument("--profile", default="capabilities.json")
    parser.add_argument("--v11-config", default="v11_config.json")
    parser.add_argument("--checkpoint", default="state/procurement_checkpoint.json")
    parser.add_argument("--from", dest="updated_from")
    parser.add_argument("--to", dest="updated_to")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=5)
    parser.add_argument("--evidence-jsonl")
    parser.add_argument("--award-history")
    args = parser.parse_args()

    results = run_v11(
        source=args.source,
        profile_path=args.profile,
        v11_config_path=args.v11_config,
        checkpoint_path=args.checkpoint,
        evidence_path=args.evidence_jsonl,
        updated_from=args.updated_from,
        updated_to=args.updated_to,
        limit=args.limit,
        max_pages=args.max_pages,
        award_history_path=args.award_history,
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
