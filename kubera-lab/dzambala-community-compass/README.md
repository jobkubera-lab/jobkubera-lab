# DZAMBALA Community Compass — London + Merton

A small, practical city-discovery prototype for finding **verified community, cultural, wellbeing, learning, volunteering and sport sources/events** in London, with a dedicated Merton view.

## What v0.2 does

- switches between **London + Merton** and **Merton only**;
- shows a verified **upcoming-event layer** from official/institutional sources;
- filters events by **Today**, **Tomorrow**, **Weekend**, **Free only** and category;
- links every event to the original source and records when it was checked;
- keeps a separate verified-source directory with a transparent **Trust Score**;
- plots sources and events that have known coordinates on an OpenStreetMap/Leaflet map;
- validates event data, ISO timestamps, HTTPS provenance and deterministic duplicate fingerprints;
- runs the validators and event tests in GitHub Actions.

## Event verification

`events.json` is a **manually verified seed layer**, not an automated scraper. The current seed was checked on **30 August 2026** against primary or institutional pages, including Merton Council and Bharatiya Vidya Bhavan.

Each event stores:

- start/end time with timezone offset;
- area/borough, venue and address;
- category and price state (`FREE`, `PAID`, `UNKNOWN`);
- organiser;
- original source URL and source type;
- verification date and status.

The browser marks an event as needing a recheck when its `checked_at` date is more than seven days old. That is a freshness warning, not a claim that the event is cancelled.

## Trust Score for source hubs

The source-hub score is deliberately simple and visible:

- source authority: up to 40 points;
- freshness of verification: up to 30 points;
- direct official/source link: up to 20 points;
- local relevance: up to 10 points.

This is **not** a rating of a religion, community, teacher, organisation or worldview. It only describes how confidently the listing itself can be verified.

## Validation

From this folder:

```bash
python validate_data.py
python validate_events.py
python -m unittest -v test_events.py
```

## Run locally

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Status

`v0.2` implements a verified event layer and deterministic validation/deduplication. **Automatic event ingestion, automatic re-verification, personal profiles, AI ranking and notifications are not claimed as implemented yet.**
