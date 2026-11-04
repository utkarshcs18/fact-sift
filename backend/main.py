"""
GET  /         → health check
POST /analyze  → verify a factual claim (demo mode)
GET  /history  → recent analyses (in-memory list)
"""

from __future__ import annotations

from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import AnalysisResponse, ClaimRequest, HistoryItem
from backend.services import analyze_claim


app = FastAPI(
    title="Fact-Sift API",
    description="Evidence-based claim verification system.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


_history: List[HistoryItem] = []
_MAX_HISTORY = 100


@app.get("/")
def health_check():
    return {"status": "ok", "service": "fact-sift", "version": "0.1.0"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: ClaimRequest):
    result = analyze_claim(request.claim)

    # Persist to in-memory history
    _history.append(
        HistoryItem(
            claim=result.claim,
            verdict=result.verdict,
            confidence=result.confidence,
            timestamp=result.timestamp,
        )
    )
    # Keep history bounded
    if len(_history) > _MAX_HISTORY:
        _history.pop(0)

    return result


@app.get("/history", response_model=List[HistoryItem])
def history():
    return list(reversed(_history))
