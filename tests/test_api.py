"""Test the API endpoints of Bob's Brain v5"""

import pytest

from src.bob_brain_v5 import app


@pytest.fixture
def client():
    """Test client for Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "services" in data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "bobs-brain"
    assert data["version"] == "5.0"


def test_metrics_endpoint(client):
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.mimetype == "text/plain"


def test_api_auth_required(client):
    """Test that API endpoints require authentication"""
    response = client.post("/api/query", json={"query": "test"})
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "unauthorized"


def test_learn_auth_required(client):
    """Test that learn endpoint requires authentication"""
    response = client.post("/learn", json={"correction": "test"})
    assert response.status_code == 401


def test_api_query_with_key(client):
    """Test API query with valid API key"""
    response = client.post("/api/query", headers={"X-API-Key": "test"}, json={"query": "hello"})
    # Should work (200) or fail gracefully (500) but not auth error
    assert response.status_code in (200, 500)


def test_learn_with_key(client):
    """Test learn endpoint with valid API key"""
    response = client.post("/learn", headers={"X-API-Key": "test"}, json={"correction": "test correction"})
    # Should work (200) or fail gracefully (500) but not auth error
    assert response.status_code in (200, 500)


def test_slack_events_public(client):
    """Test that Slack events endpoint is public (no auth required)"""
    response = client.post("/slack/events", json={"type": "url_verification", "challenge": "test"})
    # Should process without auth error
    assert response.status_code != 401


def test_invalid_json_handling(client):
    """Test handling of invalid JSON"""
    response = client.post(
        "/api/query", headers={"X-API-Key": "test", "Content-Type": "application/json"}, data="invalid json"
    )
    assert response.status_code in (400, 500)


def test_col_metrics_endpoint(client):
    """Test Circle of Life metrics endpoint"""
    response = client.get("/circle-of-life/metrics", headers={"X-API-Key": "test"})
    assert response.status_code == 200
    data = response.get_json()
    assert "ready" in data
    assert "config" in data
