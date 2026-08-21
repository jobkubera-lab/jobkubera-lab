# GeoMemory Engine

**Status:** `CONCEPT`  
**Layer:** Reality / Geographic Memory

## Purpose
Convert travel and place knowledge into a structured, queryable geographic memory instead of leaving it scattered across map reviews, photos and notes.

## Record model
Each place may store: stable place ID, coordinates, city/country, category, visit context, public links, notes, media references, confidence and project connections.

## Key rule
Separate **observed first-hand data**, external sourced facts and model inference. They must never be silently merged.

## Outputs
- searchable place archive;
- GeoJSON exports;
- city knowledge packs;
- map layers;
- context for Geographic Intelligence Agent.

## Integrations
Kubera Guide, City DNA Packages, Reality Graph, Evidence Ledger, community maps.

## MVP
Import a small curated set of public Kubera Guide locations into a normalized GeoJSON/SQLite schema and query it locally.
