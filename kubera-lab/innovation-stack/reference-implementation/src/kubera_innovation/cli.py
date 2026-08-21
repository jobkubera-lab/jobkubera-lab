from __future__ import annotations

import argparse
import json

from .authority import AuthorityBudget, ControlLevel
from .constitution import Constitution, Decision, PolicyRule
from .failure_vaccine import FailureVaccineRegistry
from .proof_work import ProofOfWork, ProofStage
from .reality_graph import RealityGraph
from .reputation import ReputationEngine


def demo() -> dict:
    constitution = Constitution([
        PolicyRule("deny-delete", "file.delete", Decision.DENY, priority=10, reason="destructive delete requires separate policy"),
        PolicyRule("allow-read", "file.read", Decision.ALLOW, priority=20, reason="read access allowed"),
    ])
    policy, policy_reason = constitution.evaluate("file.read", project="demo")
    budget = AuthorityBudget(ControlLevel.ACT, {"file_write": 2, "github_pr": 1})
    budget_result = budget.consume("file_write", required_level=ControlLevel.CREATE)

    graph = RealityGraph()
    graph.add_node("project:demo", "Project", "Demo", visibility="PUBLIC")
    graph.add_node("idea:demo", "Idea", "Human-controlled automation", visibility="PUBLIC")
    graph.add_edge("idea:demo", "CREATED_FROM", "project:demo")
    public_graph = graph.export_public()

    vaccines = FailureVaccineRegistry()
    vaccines.add_rule("wrong-branch", trigger_type="contains", pattern="deploy from feature branch", action="BLOCK", reason="deployment must use the approved release branch")
    vaccine = vaccines.check("attempt to deploy from feature branch")

    rep = ReputationEngine()
    rep.record("builder-agent", "code_quality", 0.9, verified=True, evidence_ref="test:1")
    rep.record("builder-agent", "tool_safety", 1.0, verified=True, evidence_ref="test:2")
    reputation = rep.summary("builder-agent")

    proof = ProofOfWork("KUBERA Reference Demo")
    proof.add(ProofStage.IDEA, "Architecture defined", verified=True)
    proof.add(ProofStage.TEST, "Reference tests", verified=True)

    result = {
        "constitution": {"decision": policy.value, "reason": policy_reason},
        "authority": {"allowed": budget_result.allowed, "remaining": budget_result.remaining},
        "public_graph": public_graph,
        "failure_vaccine": {"action": vaccine.action, "rule_id": vaccine.rule_id},
        "reputation": {"overall": reputation.overall, "dimensions": reputation.dimensions, "verified_events": reputation.verified_events},
        "proof_order_valid": proof.validate_order(),
    }
    graph.close(); vaccines.close(); rep.close()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(prog="kubera-innovation")
    sub = parser.add_subparsers(dest="command", required=True)
    demo_parser = sub.add_parser("demo", help="run a safe in-memory reference demo")
    demo_parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()
    if args.command == "demo":
        result = demo()
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            for key, value in result.items():
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()
