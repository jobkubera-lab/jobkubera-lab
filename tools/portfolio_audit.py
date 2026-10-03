from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "KUBERA_AGENT_OS.md",
    "STATUS.md",
    "REPO_MAP.md",
    "PORTFOLIO_REVIEW.md",
    "EVIDENCE_MATRIX.md",
    "kubera-lab/agent-os/README.md",
    "kubera-lab/kubera-tao-lab/README.md",
    "kubera-lab/real-estate-os/README.md",
    "kubera-lab/tender-intelligence/README.md",
    "kubera-lab/mcp-lab/README.md",
    "research/council-ai-service-finder/eval/v0.1",
]

REQUIRED_PROFILE_TEXT = [
    "AI Systems Builder",
    "AI Assurance & Infrastructure",
    "Evidence-Driven Automation",
    "KUBERA AGENT OS",
    "KUBERA TAO LAB",
    "KUBERA Real Estate OS",
]

FORBIDDEN_PUBLIC_TEXT = [
    "1.1M+ Google Maps views",
    "1.8K profile impressions",
    "47 unit tests",
    "6 executable foundation prototypes",
    "coingecko.com/en/coins/monero",
    "Live XMR/USD price",
]

PUBLIC_NARRATIVE_FILES = [
    "README.md",
    "ABOUT_KUBERA.md",
]


def main() -> int:
    errors = []

    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            errors.append(f"missing required portfolio path: {rel}")

    profile = (ROOT / "README.md").read_text(encoding="utf-8")

    for text in REQUIRED_PROFILE_TEXT:
        if text not in profile:
            errors.append(f"profile missing required text: {text}")

    for rel in PUBLIC_NARRATIVE_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing public narrative file: {rel}")
            continue
        body = path.read_text(encoding="utf-8")
        for text in FORBIDDEN_PUBLIC_TEXT:
            if text in body:
                errors.append(f"{rel} contains stale/unverified public claim: {text}")

    evidence = (ROOT / "EVIDENCE_MATRIX.md")
    if evidence.exists():
        body = evidence.read_text(encoding="utf-8")
        for required in ("173 tests passed", "89%", "34/34", "3/3", "16 tests passed"):
            if required not in body:
                errors.append(f"evidence matrix missing verified evidence: {required}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("KUBERA portfolio audit: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
