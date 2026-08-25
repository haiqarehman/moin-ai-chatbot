from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_session_returns_session_id():
    response = client.post("/api/v1/sessions")

    assert response.status_code == 200

    data = response.json()

    assert "session_id" in data
    assert data["session_id"]


def test_create_session_returns_unique_ids():
    response1 = client.post("/api/v1/sessions")
    response2 = client.post("/api/v1/sessions")

    session1 = response1.json()["session_id"]
    session2 = response2.json()["session_id"]

    assert session1 != session2