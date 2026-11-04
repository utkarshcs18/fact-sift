"""
Implements a **DEMO MODE** that returns realistic mock responses with varied
verdicts based on simple keyword heuristics, so the frontend can connect and
see interesting data without any trained models.
"""

from __future__ import annotations

import hashlib
import random
from datetime import datetime
from typing import List

from backend.schemas import AnalysisResponse, EvidenceItem


_SUPPORTS_EVIDENCE = [
    EvidenceItem(
        text="According to multiple peer-reviewed studies published in Nature and Science, "
        "this claim is consistent with the current body of scientific evidence.",
        source="Nature / Science meta-analysis",
        relevance_score=0.95,
        verdict="SUPPORTS",
        confidence=0.92,
    ),
    EvidenceItem(
        text="Data from the World Health Organization confirms the statistical trends "
        "cited in the claim, with a 95% confidence interval.",
        source="WHO Global Health Observatory",
        relevance_score=0.91,
        verdict="SUPPORTS",
        confidence=0.89,
    ),
    EvidenceItem(
        text="Historical records from reputable archives corroborate the events "
        "described in the claim, with primary-source documentation.",
        source="National Archives & Records",
        relevance_score=0.87,
        verdict="SUPPORTS",
        confidence=0.85,
    ),
]

_REFUTES_EVIDENCE = [
    EvidenceItem(
        text="A comprehensive fact-check by Reuters found no credible evidence "
        "supporting this claim; the original source has been retracted.",
        source="Reuters Fact Check",
        relevance_score=0.94,
        verdict="REFUTES",
        confidence=0.93,
    ),
    EvidenceItem(
        text="Peer-reviewed research published in The Lancet directly contradicts "
        "the central premise of this claim with statistically significant results.",
        source="The Lancet, Vol. 401",
        relevance_score=0.90,
        verdict="REFUTES",
        confidence=0.91,
    ),
    EvidenceItem(
        text="Official government statistics show the numbers cited in the claim "
        "are inaccurate by a factor of ten.",
        source="Bureau of Labor Statistics",
        relevance_score=0.88,
        verdict="REFUTES",
        confidence=0.87,
    ),
]

_NEI_EVIDENCE = [
    EvidenceItem(
        text="While some anecdotal reports align with this claim, no large-scale "
        "study has been conducted to confirm or deny it.",
        source="PubMed search results",
        relevance_score=0.72,
        verdict="NOT_ENOUGH_INFO",
        confidence=0.65,
    ),
    EvidenceItem(
        text="The claim references events that are still under investigation; "
        "authoritative bodies have not yet released final findings.",
        source="Associated Press",
        relevance_score=0.68,
        verdict="NOT_ENOUGH_INFO",
        confidence=0.60,
    ),
    EvidenceItem(
        text="Experts in the field have expressed mixed opinions, with roughly "
        "equal numbers supporting and disputing the claim.",
        source="Expert panel survey",
        relevance_score=0.70,
        verdict="NOT_ENOUGH_INFO",
        confidence=0.58,
    ),
]


_REFUTE_KEYWORDS = {
    "flat earth", "moon landing fake", "hoax", "conspiracy", "fake",
    "never happened", "myth", "debunked", "false", "not true",
    "doesn't exist", "impossible", "aliens built",
}

_SUPPORT_KEYWORDS = {
    "earth is round", "water boils at 100", "gravity", "evolution",
    "climate change is real", "vaccines work", "sun is a star",
    "earth orbits the sun", "dna", "photosynthesis", "moon landing",
    "speed of light", "earth revolves", "humans need oxygen",
}


def _pick_verdict(claim: str) -> str:
    lower = claim.lower()
    for kw in _REFUTE_KEYWORDS:
        if kw in lower:
            return "REFUTES"
    for kw in _SUPPORT_KEYWORDS:
        if kw in lower:
            return "SUPPORTS"
    # Deterministic but varied fallback based on claim hash
    h = int(hashlib.md5(lower.encode()).hexdigest(), 16)
    choices = ["SUPPORTS", "REFUTES", "NOT_ENOUGH_INFO"]
    return choices[h % 3]


def _evidence_for(verdict: str) -> List[EvidenceItem]:
    if verdict == "SUPPORTS":
        return list(_SUPPORTS_EVIDENCE)
    elif verdict == "REFUTES":
        return list(_REFUTES_EVIDENCE)
    return list(_NEI_EVIDENCE)


def _confidence_for(verdict: str, claim: str) -> float:
    base = {"SUPPORTS": 0.88, "REFUTES": 0.90, "NOT_ENOUGH_INFO": 0.62}
    # Add a small deterministic jitter so different claims get different scores
    h = int(hashlib.md5(claim.lower().encode()).hexdigest()[:8], 16)
    jitter = (h % 100) / 1000  # 0.000 – 0.099
    return round(min(base.get(verdict, 0.70) + jitter, 0.99), 4)


def _explanation_for(verdict: str, claim: str) -> str:
    templates = {
        "SUPPORTS": (
            f'The claim "{claim}" is consistent with available evidence. '
            "Multiple high-quality sources corroborate the central assertion. "
            "Confidence is high based on cross-referenced data."
        ),
        "REFUTES": (
            f'The claim "{claim}" conflicts with authoritative evidence. '
            "Fact-checking organisations and peer-reviewed research contradict "
            "the core assertion. The original source appears unreliable."
        ),
        "NOT_ENOUGH_INFO": (
            f'The claim "{claim}" cannot be conclusively verified or refuted '
            "with currently available evidence. Further investigation or "
            "primary-source data is needed before a definitive judgement can be made."
        ),
    }
    return templates.get(verdict, "Analysis complete.")



def analyze_claim(claim: str) -> AnalysisResponse:
    verdict = _pick_verdict(claim)
    confidence = _confidence_for(verdict, claim)
    evidence = _evidence_for(verdict)
    explanation = _explanation_for(verdict, claim)

    return AnalysisResponse(
        claim=claim,
        verdict=verdict,
        confidence=confidence,
        evidence=evidence,
        explanation=explanation,
        timestamp=datetime.utcnow(),
        model_used="demo",
    )
