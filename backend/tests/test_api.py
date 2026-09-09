import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "HandForge" in data["service"]

def test_gallery_top_endpoint():
    response = client.get("/api/v1/gallery/top?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] <= 3
    assert data["withinSla"] is True
    assert data["queryLatencyMs"] < 10.0

def test_obj_inspect_endpoint():
    raw_obj = """# Wavefront OBJ test
v 1.0 2.0 3.0
v 4.0 5.0 6.0
v 7.0 8.0 9.0
vn 0.0 1.0 0.0
f 1//1 2//1 3//1
"""
    response = client.post("/api/v1/projects/obj-inspect", json={"content": raw_obj})
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["vertices"] == 3
    assert data["summary"]["faces"] == 1
