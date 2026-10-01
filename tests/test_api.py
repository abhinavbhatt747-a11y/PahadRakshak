import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "PahadRakshak"

def test_get_incidents():
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    incidents = response.json()
    assert isinstance(incidents, list)

def test_dashboard_stats():
    response = client.get("/api/v1/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_active" in data
    assert "critical_count" in data

def test_demo_simulation():
    response = client.post("/api/v1/demo/simulate")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "simulated_incident" in data
