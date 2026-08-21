# DZAMBALA Community Compass — London + Merton MVP

A small, practical MVP for discovering **verified community, cultural, wellbeing and learning sources** in London, with a dedicated Merton view.

## What this MVP does

- switches between **London** and **Merton**;
- filters sources by category;
- shows a transparent **Trust Score**;
- links to the original/official source;
- records when each source was last checked;
- plots verified venues/sources that have coordinates on a map;
- separates verified source hubs from future live event ingestion.

## Trust Score

The score is deliberately simple and visible:

- source authority: up to 40 points;
- freshness of verification: up to 30 points;
- direct official/source link: up to 20 points;
- local relevance: up to 10 points.

This is **not** a rating of a religion, community, teacher or worldview. It is only a score for how confidently the listing itself can be verified.

## Current seed sources

The first seed uses primary or institutional sources, including Merton Council, Merton Connected, the High Commission of India / Nehru Centre and Bharatiya Vidya Bhavan.

## Run locally

Open `index.html` in a browser. For browsers that restrict local JSON loading, run a tiny local web server from this folder:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Status

`MVP v0.1` — verified-source navigator. Live event collection, AI matching, deduplication and automated re-verification are intentionally not claimed as implemented yet.
