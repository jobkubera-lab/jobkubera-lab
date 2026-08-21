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
- links to evidence and later implementation;
- optional `diagram-intent.yaml` when a visual explanation will improve understanding.

## Pipeline
```text
Experience → clarify intent → extract entities → define mechanics → architecture → visual intent → tasks → prototype record
```

## Visual Systems connection

The compiler should not directly hard-code a rendering engine. When a diagram is useful, it emits a structured `DiagramIntent` describing the visual type, purpose, audience, detail and output requirements. That intent can then be routed to the KUBERA Visual Systems Layer.

This makes diagram generation replaceable in the same way models are replaceable.

## Distinctive angle
The compiler preserves the **origin story of the system**: a technical design remains linked to the real situation that caused it, rather than becoming an isolated specification.

## Integrations
Reality Graph, Project Memory, Personal AI Constitution, Proof-of-Work Portfolio, KUBERA Visual Systems Layer.

## MVP
A CLI or agent skill that accepts a scenario and emits `project.yaml`, `architecture.md`, `issues.json`, `risk.md` and, when needed, `diagram-intent.yaml`.
