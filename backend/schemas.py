"""
schemas.py – Pydantic models for the Fact-Sift API.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ClaimRequest(BaseModel):
    claim: str = Field(..., min_length=1, description="The factual claim to verify.")


class EvidenceItem(BaseModel):

    text: str = Field(..., description="The evidence passage text.")
    source: str = Field(default="", description="Source or origin of the evidence.")
    relevance_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="How relevant the passage is (0–1)."
    )
    verdict: str = Field(
        default="NOT_ENOUGH_INFO",
        description="Passage-level verdict: SUPPORTS / REFUTES / NOT_ENOUGH_INFO.",
    )
    confidence: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Confidence in the passage verdict."
    )


class AnalysisResponse(BaseModel):

    claim: str
    verdict: str = Field(
        ..., description="Overall verdict: SUPPORTS / REFUTES / NOT_ENOUGH_INFO."
    )
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence: List[EvidenceItem] = Field(default_factory=list)
    explanation: str = Field(default="", description="Human-readable explanation.")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_used: str = Field(
        default="demo", description="Which model produced the verdict."
    )


class HistoryItem(BaseModel):

    claim: str
    verdict: str
    confidence: float
    timestamp: datetime
