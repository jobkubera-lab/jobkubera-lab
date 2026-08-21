# KUBERA Reality Graph

**Status:** `CONCEPT`  
**Layer:** Reality / Memory

## Purpose
Create a user-owned graph linking projects, ideas, places, files, decisions, events and evidence without mixing everything into one chat history.

## Core entities
`Project` · `Idea` · `Place` · `Object` · `Document` · `Decision` · `Evidence` · `Failure` · `Skill` · `Agent`

## Core relations
`INSPIRED_BY` · `BELONGS_TO` · `VISITED_AT` · `USES` · `PROVED_BY` · `FAILED_BECAUSE` · `CREATED_FROM` · `RELATED_TO`

## Storage approach
Start with SQLite tables or JSONL records; add a graph database only when graph traversal genuinely requires it.

## Privacy model
Every node receives a visibility class: `PRIVATE`, `PROJECT`, `PUBLIC`. Public exports must pass the Private/Public Gate.

## Example
```text
Thailand → Japanese Doll → Instagram Reel → Prompt → GitHub project → UK shop research
```

## Integrations
GeoMemory, Creative Object DNA, Decision Replay, Evidence Ledger, Project Memory, Life → System Compiler.
