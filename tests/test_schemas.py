"""
test_schemas.py – Unit tests for Pydantic models in backend.schemas.
"""

from datetime import datetime

import pytest

from backend.schemas import (
    AnalysisResponse,
    ClaimRequest,
    EvidenceItem,
    HistoryItem,
)


class TestClaimRequest:
    def test_valid(self):
        req = ClaimRequest(claim="The sky is blue.")
        assert req.claim == "The sky is blue."

    def test_empty_claim_rejected(self):
        with pytest.raises(Exception):
            ClaimRequest(claim="")

    def test_missing_claim_rejected(self):
        with pytest.raises(Exception):
            ClaimRequest()  # type: ignore[call-arg]


class TestEvidenceItem:
    def test_defaults(self):
        item = EvidenceItem(text="Some evidence.")
        assert item.source == ""
        assert item.relevance_score == 0.0
        assert item.verdict == "NOT_ENOUGH_INFO"
        assert item.confidence == 0.0

    def test_full(self):
        item = EvidenceItem(
            text="Evidence text",
            source="Wikipedia",
            relevance_score=0.85,
            verdict="SUPPORTS",
            confidence=0.9,
        )
        assert item.relevance_score == 0.85
        assert item.verdict == "SUPPORTS"


class TestAnalysisResponse:
    def test_construction(self):
        resp = AnalysisResponse(
            claim="Test claim",
            verdict="SUPPORTS",
            confidence=0.9,
            evidence=[],
            explanation="Good.",
        )
        assert resp.claim == "Test claim"
        assert resp.verdict == "SUPPORTS"
        assert isinstance(resp.timestamp, datetime)
        assert resp.model_used == "demo"


class TestHistoryItem:
    def test_construction(self):
        item = HistoryItem(
            claim="Test",
            verdict="REFUTES",
            confidence=0.8,
            timestamp=datetime.utcnow(),
        )
        assert item.verdict == "REFUTES"
