# KUBERA Visual Systems Layer

**Status:** `PROTOTYPE CONTRACT`  
**Role:** Cross-cutting visualization capability for KUBERA LAB and KUBERA AGENT OS

## Purpose
Turn technical ideas, data and project structure into deliberate visual artifacts instead of generic diagrams.

KUBERA uses a model-agnostic `DiagramIntent` contract that can be handed to an external renderer/skill. The first supported upstream capability is **Diagram Design** by Cathryn Lavery.

## Verified upstream capability — 21 August 2026

The live upstream repository documents **39 editorial diagram types** and supports standalone **HTML / SVG / PNG** output. It also documents:

- architecture, flowchart, sequence, state, ER/data-model and timeline diagrams;
- swimlanes, radar, Sankey, Wardley maps, kanban and user journeys;
- deployment, dependency graph, UML class and database-schema diagrams;
- redraw/import workflows for Mermaid and draw.io sources;
- website-based brand onboarding using semantic color and typography roles;
- static output as the default, with optional accessible motion;
- contrast checks and explicit visual hierarchy;
- shared skill files usable by compatible agent environments including Claude Code, Codex, Factory Droid and Pi.

Upstream: https://github.com/cathrynlavery/diagram-design  
License: **MIT**  
Copyright: **Cathryn Lavery**

## KUBERA integration architecture

```text
Human idea / project data
        ↓
Life → System Compiler
        ↓
DiagramIntent contract
        ↓
Privacy / publication check
        ↓
Visual renderer capability
        ↓
HTML / SVG / PNG artifact
        ↓
Proof-of-Work Portfolio / docs / presentation
```

The KUBERA adapter does **not** copy or claim ownership of the external renderer. It validates intent, output format, detail level, source format and accessibility expectations, then produces a stable payload/instruction for a renderer.

## KUBERA DiagramIntent

Key fields:

- `diagram_type`
- `title`
- `purpose`
- `audience`
- `detail`
- `output_format`
- `theme`
- `brand_source`
- `source_format`
- `motion`

See [diagram-intent.example.yaml](diagram-intent.example.yaml) and the executable adapter in [reference-implementation](../reference-implementation/).

## High-value diagram types for KUBERA

Priority types for our projects:

- **architecture** — KUBERA AGENT OS and system layers;
- **flowchart / process** — agent decisions and workflows;
- **sequence** — tool calls and multi-agent interaction;
- **ER / database schema** — Reality Graph and Evidence Ledger;
- **timeline / Gantt** — project evolution and roadmap;
- **data flow** — privacy and evidence movement;
- **deployment** — local AI and server topology;
- **dependency graph** — skills/modules and service dependencies;
- **user journey** — civic-tech and newcomer tools;
- **Wardley map** — technology strategy;
- **Sankey** — resource/information flows;
- **radar** — technology or agent capability comparison;
- **kanban** — development state and project operations.

## Brand system

Visual renderers should map branding into semantic roles rather than hard-code random colors:

`paper` · `paper-2` · `ink` · `muted` · `accent` · `link` · `title-font` · `body-font` · `code-font`

KUBERA does not currently hard-code a public brand palette here. A brand source can be supplied when the official visual identity is finalized.

## Privacy rule

A diagram can reveal sensitive information even when source code is hidden. Therefore diagrams generated from private projects must pass the same Public / Private Twin and governance checks as text or code before publication.

## Attribution

See [THIRD_PARTY.md](../THIRD_PARTY.md). The external Diagram Design project remains under its original MIT copyright and license.
