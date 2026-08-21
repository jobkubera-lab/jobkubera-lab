# City DNA Packages

**Status:** `CONCEPT`  
**Layer:** Reality / Portable Local Knowledge

## Purpose
Represent a city as a portable, versioned knowledge package that an agent or map application can load.

## Proposed package
```text
city.yaml
places.geojson
services.json
transport.md
culture.md
field-notes.md
sources.json
CHANGELOG.md
```

## Rules
- stable IDs for places and services;
- timestamps for changing information;
- source/provenance fields;
- clear separation of first-hand notes and external facts;
- schema version for future migrations.

## Use cases
Local onboarding, travel planning, community maps, Geographic Intelligence Agent and offline/local AI context.

## Integrations
GeoMemory, Reality Graph, Kubera Guide, Public/Private Twin.

## MVP
Create one small test City DNA package from already-public community-map information.
