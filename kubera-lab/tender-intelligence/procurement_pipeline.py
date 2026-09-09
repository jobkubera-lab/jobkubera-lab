from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from procurement_adapter import (
    deduplicate,
    evidence_record,
    fetch_contracts_finder,
    fetch_find_a_tender,
    normalize_package,
)
from tender_intelligence import load_json, score_opportunity


def _append_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")


def run(
    *,
    source: str,
    profile_path: str | Path,
    evidence_path: str | Path | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    profile = load_json(profile_path)

    if source == "find_a_tender":
        package, source_url = fetch_find_a_tender(
            updated_from=updated_from,
            updated_to=updated_to,
            limit=limit,
        )
    elif source == "contracts_finder":
        package, source_url = fetch_contracts_finder(
            published_from=updated_from,
            published_to=updated_to,
            limit=limit,
        )
    else:
        raise ValueError(f"Unsupported source: {source}")

    normalized = deduplicate(normalize_package(package, source=source, source_url=source_url))
    output: list[dict[str, Any]] = []
    ledger_records: list[dict[str, Any]] = []

    for opportunity in normalized:
        decision = score_opportunity(opportunity.as_tender_input(), profile)
        output.append(
            {
                "opportunity": opportunity.as_tender_input(),
                "decision": asdict(decision),
            }
        )
        ledger_records.append(evidence_record(opportunity))

    if evidence_path is not None and ledger_records:
        _append_jsonl(Path(evidence_path), ledger_records)

    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="KUBERA read-only UK procurement intake pipeline")
    parser.add_argument("--source", choices=["find_a_tender", "contracts_finder"], required=True)
    parser.add_argument("--profile", default="capabilities.json")
    parser.add_argument("--from", dest="updated_from")
    parser.add_argument("--to", dest="updated_to")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--evidence-jsonl")
    args = parser.parse_args()

    results = run(
        source=args.source,
        profile_path=args.profile,
        evidence_path=args.evidence_jsonl,
        updated_from=args.updated_from,
        updated_to=args.updated_to,
        limit=args.limit,
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
