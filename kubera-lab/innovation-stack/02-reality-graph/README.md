# KUBERA Reality Graph

**Status:** `PROTOTYPE`  
**Layer:** Reality / Memory

## Purpose
Create a user-owned graph linking projects, ideas, places, files, decisions, events and evidence without mixing everything into one chat history.

## Prototype implementation
The public v0.1 reference runtime now includes an executable **SQLite-backed Reality Graph** with typed nodes, relations, metadata, explicit `PRIVATE / PROJECT / PUBLIC` visibility and a public exporter that excludes private nodes and edges touching them.

➡️ [Open the reference implementation](../reference-implementation/)

## Core entities
`Project` · `Idea` · `Place` · `Object` · `Document` · `Decision` · `Evidence` · `Failure` · `Skill` · `Agent`

## Core relations
`INSPIRED_BY` · `BELONGS_TO` · `VISITED_AT` · `USES` · `PROVED_BY` · `FAILED_BECAUSE` · `CREATED_FROM` · `RELATED_TO`

## Storage approach
The prototype begins with SQLite. A graph database is unnecessary until traversal complexity demonstrates a real need.

## Privacy model
Every node has a visibility class. Public export is deliberately narrower than the full graph.

## Integrations
GeoMemory, Creative Object DNA, Decision Replay, Evidence Ledger, Project Memory, Life → System Compiler.
