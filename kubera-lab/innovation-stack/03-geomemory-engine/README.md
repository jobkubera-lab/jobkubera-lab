# GeoMemory Engine

**Status:** `CONCEPT`  
**Layer:** Reality / Geographic Memory

## Purpose
Convert travel and place knowledge into a structured, queryable geographic memory instead of leaving it scattered across map reviews, photos and notes.

## Record model
Each place may store:

- stable place ID;
- place name and category;
- coordinates and city/country;
- visit context;
- `provenance`: `first_hand`, `external_source` or `model_inference`;
- `source_platform` and public source URL;
- media references / capture type;
- notes and project connections;
- confidence;
- observed / published timestamps only when actually known.

## Kubera Guide bridge

Kubera Guide gives the GeoMemory design a concrete real-world source model: places are visited, photographed and published through Google Maps. The supplied public-profile screenshots confirm **1.1M views** and **1.8K profile impressions**, demonstrating that the map activity is not only stored data but publicly consumed geographic content.

The technical rule is more important than the metric: a Kubera Guide-derived record can be marked `provenance: first_hand`, while current operational facts from the web remain `external_source` and AI-created deductions remain `model_inference`.

## Key rule
Separate **observed first-hand data**, external sourced facts and model inference. They must never be silently merged.

## Outputs
- searchable place archive;
- GeoJSON exports;
- city knowledge packs;
- map layers;
- context for Geographic Intelligence Agent;
- structured inputs for visual maps and diagrams.

## Integrations
Kubera Guide, City DNA Packages, Reality Graph, Evidence Ledger, Visual Systems Layer, community maps.

## MVP
Import a small curated set of already-public Kubera Guide locations into a normalized GeoJSON/SQLite schema and query it locally.
