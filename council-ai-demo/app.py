from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "services.json"
STOPWORDS = {
    "i", "me", "my", "we", "our", "the", "a", "an", "to", "for", "at", "in",
    "on", "with", "and", "or", "is", "are", "was", "were", "want", "need",
    "please", "help", "can", "could", "would"
}

app = FastAPI(title="KUBERA Council AI Service Finder", version="0.1.1")


def load_services() -> list[dict[str, Any]]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalise(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s'-]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text)


def meaningful_tokens(text: str) -> set[str]:
    return {token for token in normalise(text).split() if token not in STOPWORDS and len(token) > 1}


def score_query(query: str, service: dict[str, Any]) -> tuple[int, list[str]]:
    q = normalise(query)
    candidates: list[str] = []
    candidates.extend(service.get("keywords", []))
    for aliases in service.get("aliases", {}).values():
        candidates.extend(aliases)

    matched: list[str] = []
    score = 0
    q_tokens = meaningful_tokens(q)

    for phrase in candidates:
        p = normalise(phrase)
        if not p:
            continue

        if p in q:
            matched.append(phrase)
            score += 4 + len(meaningful_tokens(p))
            continue

        p_tokens = meaningful_tokens(p)
        if not p_tokens:
            continue

        overlap = len(q_tokens & p_tokens)
        if overlap >= 2 or (len(p_tokens) == 1 and overlap == 1):
            score += overlap
            matched.append(phrase)

    return score, matched[:5]


def find_service(query: str) -> dict[str, Any]:
    services = load_services()
    ranked = []

    for service in services:
        score, matched = score_query(query, service)
        ranked.append((score, matched, service))

    ranked.sort(key=lambda item: item[0], reverse=True)
    best_score, matched, best = ranked[0]

    if best_score < 2:
        return {
            "matched": False,
            "message": "No reliable service match was found. Try different wording or use the council's official service directory.",
            "query": query,
        }

    confidence = "high" if best_score >= 6 else "medium"
    return {
        "matched": True,
        "query": query,
        "confidence": confidence,
        "score": best_score,
        "matched_terms": matched,
        "service": {
            "id": best["id"],
            "title": best["title"],
            "description": best["description"],
            "source_url": best["source_url"],
        },
        "notice": "Prototype result. Always confirm details on the official source page.",
    }


@app.get("/api/search")
def search(q: str = Query(min_length=2, max_length=300)) -> dict[str, Any]:
    return find_service(q)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>KUBERA Council AI Service Finder</title>
  <style>
    body{font-family:Arial,sans-serif;max-width:760px;margin:40px auto;padding:0 18px;line-height:1.5}
    input,button{font-size:1rem;padding:12px} input{width:70%} button{cursor:pointer}
    .result{margin-top:24px;padding:18px;border:1px solid #bbb;border-radius:8px}
    .meta{font-size:.9rem;color:#555} a{font-weight:bold}
  </style>
</head>
<body>
  <h1>KUBERA Council AI Service Finder</h1>
  <p>Describe your problem in ordinary language. The prototype returns only a service from its controlled catalogue and links to an official source.</p>
  <input id="q" aria-label="Describe what you need help with" placeholder="e.g. my landlord wants me out">
  <button onclick="runSearch()">Find service</button>
  <div id="result"></div>
  <script>
    async function runSearch(){
      const q=document.getElementById('q').value;
      const el=document.getElementById('result');
      if(q.trim().length<2){el.innerHTML='<div class="result">Please enter a longer query.</div>';return;}
      el.innerHTML='<div class="result">Searching…</div>';
      const r=await fetch('/api/search?q='+encodeURIComponent(q));
      const d=await r.json();
      if(!d.matched){el.innerHTML='<div class="result"><strong>No reliable match.</strong><p>'+d.message+'</p></div>';return;}
      const s=d.service;
      el.innerHTML='<div class="result"><h2>'+s.title+'</h2><p>'+s.description+'</p><p><a href="'+s.source_url+'" target="_blank" rel="noopener">Open official source</a></p><div class="meta">Confidence: '+d.confidence+' · Prototype only</div></div>';
    }
  </script>
</body>
</html>
"""
