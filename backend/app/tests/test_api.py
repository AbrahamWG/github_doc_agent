import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns basic info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Smart Documentation Agent API"


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "smart-docs-agent"


def test_generate_documentation_invalid_url():
    """Test that invalid URLs are rejected"""
    response = client.post(
        "/api/v1/generate", json={"repo_url": "https://example.com/not-github"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "Invalid GitHub URL" in data["detail"]


def test_generate_documentation_missing_url():
    """Test that missing URL returns validation error"""
    response = client.post("/api/v1/generate", json={})
    assert response.status_code == 422  # Unprocessable Entity


# Note: Full integration tests would require API keys and network access
# For CI/CD, you would mock the agents and MCP servers
