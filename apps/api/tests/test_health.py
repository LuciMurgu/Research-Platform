"""Tests for the health endpoint."""

from fastapi.testclient import TestClient

from workbench.main import app

client = TestClient(app)


def test_health_returns_200() -> None:
    """GET /health returns 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_body() -> None:
    """GET /health returns expected JSON."""
    response = client.get("/health")
    assert response.json() == {
        "status": "ok",
        "service": "research-workbench-api",
        "mode": "local",
    }
