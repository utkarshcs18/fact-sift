"""
test_api.py – Integration tests for the FastAPI endpoints.
Uses httpx AsyncClient with ASGITransport for Starlette 1.6+ compatibility.
"""

import pytest
import httpx

from backend.main import app


@pytest.fixture()
def client():
    """Synchronous test client using httpx ASGITransport."""
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    with httpx.Client(transport=transport, base_url="http://testserver") as c:
        yield c


class TestHealthCheck:
    def test_root_returns_ok(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["service"] == "fact-sift"


class TestAnalyze:
    def test_valid_claim(self, client):
        resp = client.post("/analyze", json={"claim": "The Earth is round."})
        assert resp.status_code == 200
        data = resp.json()
        assert data["claim"] == "The Earth is round."
        assert data["verdict"] in {"SUPPORTS", "REFUTES", "NOT_ENOUGH_INFO"}
        assert 0.0 <= data["confidence"] <= 1.0
        assert isinstance(data["evidence"], list)
        assert len(data["evidence"]) > 0
        assert "explanation" in data

    def test_refute_keyword(self, client):
        resp = client.post(
            "/analyze", json={"claim": "The moon landing was a hoax."}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["verdict"] == "REFUTES"

    def test_support_keyword(self, client):
        resp = client.post(
            "/analyze", json={"claim": "Gravity causes objects to fall."}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["verdict"] == "SUPPORTS"

    def test_empty_claim_rejected(self, client):
        resp = client.post("/analyze", json={"claim": ""})
        assert resp.status_code == 422  # validation error

    def test_missing_claim_rejected(self, client):
        resp = client.post("/analyze", json={})
        assert resp.status_code == 422


class TestHistory:
    def test_history_returns_list(self, client):
        # Ensure at least one analysis exists
        client.post("/analyze", json={"claim": "Test claim for history."})
        resp = client.get("/history")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "claim" in data[0]
        assert "verdict" in data[0]
