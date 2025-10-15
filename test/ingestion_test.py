# to test, run this code
# $env:PYTHONPATH="app/backend"; pytest app/test/ingestion_test.py

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_submit_article():
    payload = {
        "user_id": "lim123",
        "content": "https://www.straitstimes.com/singapore/politics/first-mount-pleasant-bto-project-to-be-launched-in-october"
    }

    response = client.post("/api/submit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert "title" in data["metadata"]
    assert "summary" in data
    assert "topics" in data
test_submit_article()