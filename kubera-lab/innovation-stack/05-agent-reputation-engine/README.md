# Agent Reputation Engine

**Status:** `CONCEPT`  
**Layer:** Agent Quality

## Purpose
Measure how reliable an agent, skill or model has actually been instead of assuming every successful-looking answer is trustworthy.

## Signals
- test pass rate;
- self-check failures;
- human corrections;
- verified task success;
- citation/source quality;
- repeated failure rate;
- recency of evaluation.

## Score design
Scores should be multidimensional, for example:
`accuracy`, `tool_safety`, `research_quality`, `code_quality`, `latency`, `cost`.

A single 0–100 score may be displayed, but raw components remain available.

## Routing use
The Orchestrator can prefer the highest-reputation eligible skill for the task while still respecting permissions and cost.

## Anti-gaming rule
Activity alone must not raise reputation. Only validated outcomes count.

## Integrations
Agent Laboratory, Self-Check Agent, Failure Memory, Evidence Ledger, Model Router.
