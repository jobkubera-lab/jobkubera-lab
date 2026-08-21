# Prompt Evolution Engine

**Status:** `CONCEPT`  
**Layer:** Translation / Experimentation

## Purpose
Treat prompts like versioned engineering artifacts rather than disposable text snippets.

## Experiment record
`prompt_id`, `version`, `model`, `task`, `variables`, `output_ref`, `evaluation`, `cost`, `latency`, `failure_tags`, `parent_version`.

## Workflow
```text
Prompt v1 → run → evaluate → change one hypothesis → Prompt v2 → compare → keep/reject
```

## Evaluation
Use task-specific rubrics. Visual-generation prompts should not be scored by the same metrics as research or code prompts.

## Output
A lineage showing which changes improved performance and under which model/settings.

## Integrations
Skill DNA, Agent Laboratory, Evidence Ledger, Model Router, Creative Object DNA.

## MVP
Store prompt versions as YAML/Markdown and generate a comparison report from manually recorded evaluations.
