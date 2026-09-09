from __future__ import annotations

import importlib.util
import json
from dataclasses import asdict
from pathlib import Path
from types import ModuleType

from mcp.server import MCPServer

mcp = MCPServer("kubera-tender-mcp")

ROOT = Path(__file__).resolve().parents[2]
TENDER_DIR = ROOT / "tender-intelligence"
CAPABILITIES = TENDER_DIR / "capabilities.json"
V11_CONFIG = TENDER_DIR / "v11_config.json"


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _parse_object(raw: str, *, label: str) -> dict:
    if len(raw) > 250_000:
        raise ValueError(f"{label} is too large")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _parse_list(raw: str, *, label: str) -> list:
    if len(raw) > 250_000:
        raise ValueError(f"{label} is too large")
    value = json.loads(raw)
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a JSON array")
    return value


@mcp.tool()
def score_normalized_opportunity(opportunity_json: str) -> dict:
    """Score one already-normalized procurement opportunity using the existing KUBERA deterministic engine."""
    opportunity = _parse_object(opportunity_json, label="opportunity_json")
    engine = _load_module("kubera_tender_intelligence", TENDER_DIR / "tender_intelligence.py")
    profile = _load_json(CAPABILITIES)
    return asdict(engine.score_opportunity(opportunity, profile))


@mcp.tool()
def verify_tender_requirements(requirements_json: str) -> list[dict]:
    """Classify tender requirements as MANDATORY, DESIRABLE or REVIEW using deterministic markers."""
    requirements = _parse_list(requirements_json, label="requirements_json")
    v11 = _load_module("kubera_tender_v11", TENDER_DIR / "intelligence_v11.py")
    return [asdict(item) for item in v11.verify_requirements([str(x) for x in requirements])]


@mcp.tool()
def draft_bid_pack(opportunity_json: str, award_history_json: str = "[]") -> dict:
    """Prepare a DRAFT_ONLY qualification/bid pack. This tool never submits a bid."""
    opportunity = _parse_object(opportunity_json, label="opportunity_json")
    awards = _parse_list(award_history_json, label="award_history_json")
    base = _load_module("kubera_tender_intelligence_pack", TENDER_DIR / "tender_intelligence.py")
    v11 = _load_module("kubera_tender_v11_pack", TENDER_DIR / "intelligence_v11.py")
    profile = _load_json(CAPABILITIES)
    config = _load_json(V11_CONFIG)

    decision = base.score_opportunity(opportunity, profile)
    deadline = v11.assess_deadline(opportunity.get("deadline"))
    requirements = v11.verify_requirements(opportunity.get("requirements", []))
    cpv = v11.cpv_match(opportunity.get("cpv_codes", []), config.get("cpv_map", {}))
    gaps = v11.win_gap_analysis(
        requirements,
        config.get("capability_evidence", {}),
        evidence_keywords=config.get("evidence_keywords", {}),
    )
    buyer = v11.build_buyer_insight(str(opportunity.get("buyer") or ""), awards)
    pack = v11.generate_bid_pack(
        opportunity,
        asdict(decision),
        deadline,
        requirements,
        gaps,
        buyer,
        cpv,
    )
    pack["mcp_server"] = "kubera-tender-mcp"
    pack["submission_performed"] = False
    return pack


@mcp.resource("kubera://tender/policy")
def tender_policy() -> str:
    return (
        "Tender MCP is read-only/prepare-only. It may score normalized opportunities and create DRAFT_ONLY bid packs. "
        "It cannot submit bids, accept legal terms or claim unsupported certifications."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
