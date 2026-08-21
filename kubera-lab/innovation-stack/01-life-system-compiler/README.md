# Life → System Compiler

**Status:** `CONCEPT`  
**Layer:** Translation

## Purpose
Turn an unstructured real-world problem into a traceable technical project without requiring the person to speak like a software architect.

## Input
A situation in natural language: problem, goal, constraints, available resources and desired outcome.

## Output
- problem statement;
- actors and constraints;
- proposed system architecture;
- GitHub issues / milestones;
- data model candidates;
- MVP plan;
- risk and privacy notes;
- links to evidence and later implementation.

## Pipeline
```text
Experience → clarify intent → extract entities → define mechanics → architecture → tasks → prototype record
```

## Distinctive angle
The compiler preserves the **origin story of the system**: a technical design remains linked to the real situation that caused it, rather than becoming an isolated specification.

## Integrations
Reality Graph, Project Memory, Personal AI Constitution, Proof-of-Work Portfolio, Diagram Design.

## MVP
A CLI or agent skill that accepts a scenario and emits `project.yaml`, `architecture.md`, `issues.json` and `risk.md`.
