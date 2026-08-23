# KUBERA Council AI Service Finder — Demo v1

A small, evidence-grounded prototype for UK local-government service discovery.

## What it demonstrates

Residents often describe a problem in everyday language instead of knowing the official council service name. This demo maps plain-language queries to a controlled catalogue of official services.

Examples:

- `my landlord wants me out`
- `I cannot pay council tax`
- `де знайти допомогу з житлом`
- `potrzebuję pomocy z podatkiem council tax`

The system returns only services present in `data/services.json`. If confidence is too low, it says it could not find a reliable match instead of inventing one.

## Safety / public-sector design principles

- no diagnosis or legal advice;
- no fabricated services;
- every result includes a source URL field;
- multilingual aliases are explicit and reviewable;
- low-confidence searches fail safely;
- can later be connected to LocalGov Drupal / Solr / an approved LLM provider.

## Run locally

```bash
cd council-ai-demo
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

## Run tests

```bash
pytest -q
```

## Architecture

```text
Resident query
    ↓
normalise text
    ↓
multilingual intent matching
    ↓
confidence threshold
    ↓
controlled council service catalogue
    ↓
result + official source
```

## Next integration steps

1. Replace demo catalogue with data exported from a LocalGov Drupal site.
2. Add Solr-backed retrieval.
3. Add an optional LLM intent layer with strict structured output.
4. Add evaluation cases for multilingual queries and accessibility.
5. Add analytics that record failed searches without storing sensitive user text.

This is a research prototype, not an official council product.