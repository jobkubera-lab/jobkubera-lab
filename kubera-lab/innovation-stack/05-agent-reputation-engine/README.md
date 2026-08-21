# Agent Reputation Engine

**Status:** `PROTOTYPE`  
**Layer:** Agent Quality

## Purpose
Measure how reliable an agent, skill or model has actually been instead of assuming every successful-looking answer is trustworthy.

## Prototype implementation
The v0.1 runtime stores multidimensional reputation events in SQLite and computes weighted scores **only from events explicitly marked verified**. Unverified activity cannot increase reputation.

➡️ [Open the reference implementation](../reference-implementation/)

## Signals
- test pass rate;
- self-check failures;
- human corrections;
- verified task success;
- citation/source quality;
- repeated failure rate;
- recency of evaluation.

## Score design
Prototype dimensions can include `accuracy`, `tool_safety`, `research_quality`, `code_quality`, `latency` and `cost`. Scores remain decomposable instead of hiding everything behind one number.

## Anti-gaming rule
Activity alone must not raise reputation. Only validated outcomes count.

## Integrations
Agent Laboratory, Self-Check Agent, Failure Memory, Evidence Ledger, Model Router.
