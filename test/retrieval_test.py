# tests/test_ingest.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_article():
    response = client.get("/api/retrieve")
    assert response.status_code == 200
    data = response.json()
    assert data
test_get_article()