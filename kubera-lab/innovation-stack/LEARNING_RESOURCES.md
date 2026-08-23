# DZAMBALA Learning & Reference Stack

Curated from [`owainlewis/awesome-artificial-intelligence`](https://github.com/owainlewis/awesome-artificial-intelligence) (verified: real repository, 15.2k stars — not the ~16k claimed in the summary you saw, but close). This is not the full list — it's filtered down to what's actually relevant to building DZAMBALA/KUBERA, following the same principle already written in `DZAMBALA.md`: *what already exists in the world → what we can take → what we must build ourselves.*

Suggested location in the repo: `kubera-lab/innovation-stack/LEARNING_RESOURCES.md`, linked from `DZAMBALA.md`'s "2040 Research Directions" section.

## 1. Agent design fundamentals — read before writing more pipeline code

These directly inform `agent_pipeline.py` and the Builder → Critic → Verifier pattern already in the repo.

- **Building Effective Agents (Anthropic)** — https://www.anthropic.com/engineering/building-effective-agents
  The clearest existing writeup of when a fixed pipeline (what DZAMBALA has now) is the right call vs. when you actually need a more dynamic agent loop. Read this before deciding whether `agent_pipeline.py` should ever become non-deterministic.
- **A Practical Guide to Building Agents (OpenAI)** — https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
  Covers guardrails and escalation-to-human patterns — directly comparable to your `AuthorizationGrant` / Human Authority Budget work.
- **Google — Agents Companion (whitepaper)** — https://www.kaggle.com/whitepaper-agent-companion
  Has a section on agent evaluation and multi-agent coordination worth comparing against your Agent Society design.

## 2. Frameworks worth evaluating as a `RuntimeAdapter` implementation

Not to copy — to plug in *underneath* your `RuntimeAdapter` protocol so you don't rebuild durable execution yourselves.

- **LangGraph** — https://www.langchain.com/langgraph (already discussed — checkpointing, not true durable execution, per the independent review I found earlier)
- **Google ADK** — https://google.github.io/adk-docs/
- **Pydantic-AI** — https://ai.pydantic.dev/ — worth a look specifically because it's schema-first, which matches how `ExternalIntelligenceRequest`/`Response` are already built as strict dataclasses.
- **PocketFlow** — https://the-pocket.github.io/PocketFlow/ — reportedly ~100 lines, useful as a minimal reference implementation to read end-to-end in an afternoon, not to use in production.
- **CrewAI** / **AutoGen** — already compared in the earlier audit; role-based (CrewAI) vs. conversation-based (AutoGen), both weaker than what you have on privacy/evidence.

## 3. MCP and local-agent tooling

- **Goose** — https://block.github.io/goose/ — described as an "extensible, MCP-driven local agent." Worth reading its source for how it structures MCP tool permissions — directly comparable to `Skill DNA`'s `allowed_tools` field.
- **Nanocoder** — https://github.com/Nano-Collective/nanocoder — a coding agent built to run against Ollama and LM Studio specifically. Relevant because it's solving the exact problem your Model Router needs for the local-model branch: routing to a small local model with a real, working adapter you can read the code of.

## 4. Reinforcement learning — for Agent Reputation + Failure Vaccine

This is the part of the list most people would skip, but it's the most directly useful for the reputation formula from the last audit round.

- **Reinforcement Learning: An Introduction, 2nd ed. (Sutton & Barto)** — https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf
  Free, the standard reference. The chapters on exploration-vs-exploitation and non-stationary reward estimation are directly relevant to how `Model Router` should treat a provider whose reputation is drifting over time, not just a static score.
- **DeepMind — Introduction to Reinforcement Learning (video course)** — https://www.youtube.com/playlist?list=PLqYmG7hTraZDM-OYHWgPebj2MfCFzFObQ
  Faster on-ramp than the book if you want the intuition before the math.

## What I deliberately left out

The source list also has general LLM courses (Stanford, MIT, Hugging Face), IDE tooling (Cursor, GitHub Copilot), and multimodal/image/video generation tools. None of that is currently load-bearing for DZAMBALA's actual gap (Provider Adapter, Model Router, Skill DNA, Context Firewall) — adding it would be noise in the repo, not signal. If a future module actually needs it (e.g. multimodal input for Cosmic English content generation), that's a separate, smaller list at that time.
