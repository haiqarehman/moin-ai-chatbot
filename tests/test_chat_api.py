from fastapi.testclient import TestClient

from app.main import app
from app.services.dependencies import session_manager


client = TestClient(app)


def test_chat_api_rejects_unknown_session():
    response = client.post(
        "/api/v1/chat/messages",
        json={
            "session_id": "unknown-session-id",
            "message": "Hello",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found."


def test_chat_api_handles_pricing_message():
    session = session_manager.create_session()

    response = client.post(
        "/api/v1/chat/messages",
        json={
            "session_id": session.session_id,
            "message": "How much does your software cost?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"] == session.session_id
    assert data["state"] == "quote_request"
    assert "name" in data["response"].lower()
    assert "email" in data["response"].lower()
    assert "contact number" in data["response"].lower()


def test_chat_api_handles_general_message():
    session = session_manager.create_session()

    response = client.post(
        "/api/v1/chat/messages",
        json={
            "session_id": session.session_id,
            "message": "Tell me about your company.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"] == session.session_id
    assert data["state"] == "general_query"
    assert data["response"] == "general_query"
def test_chat_api_rate_limit_blocks_excessive_requests():
    from app.api.v1 import chat

    original_limiter = getattr(chat, "rate_limiter", None)

    class TestRateLimiter:
        def allow(self, client_id: str) -> bool:
            return False

    chat.rate_limiter = TestRateLimiter()

    try:
        session = session_manager.create_session()

        response = client.post(
            "/api/v1/chat/messages",
            json={
                "session_id": session.session_id,
                "message": "Hello",
            },
        )

        assert response.status_code == 429
        assert response.json()["detail"] == "Rate limit exceeded."
    finally:
        if original_limiter is None:
            delattr(chat, "rate_limiter")
        else:
            chat.rate_limiter = original_limiter    