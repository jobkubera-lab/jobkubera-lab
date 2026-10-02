from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "KUBERA_AGENT_OS.md",
    "STATUS.md",
    "REPO_MAP.md",
    "kubera-lab/agent-os/README.md",
    "kubera-lab/kubera-tao-lab/README.md",
    "kubera-lab/real-estate-os/README.md",
    "kubera-lab/tender-intelligence/README.md",
    "kubera-lab/mcp-lab/README.md",
    "research/council-ai-service-finder/eval/v0.1",
]

REQUIRED_PROFILE_TEXT = [
    "AI Systems Builder · Infrastructure & Assurance · Evidence-Driven Automation",
    "KUBERA AGENT OS",
    "KUBERA TAO LAB",
    "KUBERA Real Estate OS",
]

FORBIDDEN_PROFILE_TEXT = [
    "1.1M+ Google Maps views",
    "1.8K profile impressions",
    "47 unit tests",
    "6 executable foundation prototypes",
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

    for text in FORBIDDEN_PROFILE_TEXT:
        if text in profile:
            errors.append(f"profile contains stale/unverified claim: {text}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("KUBERA portfolio audit: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
