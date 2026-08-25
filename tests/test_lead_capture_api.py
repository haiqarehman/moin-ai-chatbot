from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.api.v1.lead_capture import router
from app.services.dependencies import session_manager


app = FastAPI()
app.include_router(router, prefix="/api/v1")

client = TestClient(app)


def test_lead_capture_rejects_unknown_session():
    response = client.post(
        "/api/v1/lead-capture",
        json={
            "session_id": "unknown-session-id",
            "field_name": "full_name",
            "value": "Ali Khan",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found."


def test_lead_capture_rejects_invalid_email():
    session = session_manager.create_session()

    response = client.post(
        "/api/v1/lead-capture",
        json={
            "session_id": session.session_id,
            "field_name": "email",
            "value": "invalid-email",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid email address."


def test_lead_capture_accepts_valid_name():
    session = session_manager.create_session()

    response = client.post(
        "/api/v1/lead-capture",
        json={
            "session_id": session.session_id,
            "field_name": "full_name",
            "value": "Ali Khan",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"] == session.session_id
    assert data["next_required_field"] == "email"
    assert data["lead_complete"] is False
def test_lead_capture_completes_lead_over_multiple_turns():
    session = session_manager.create_session()

    name_response = client.post(
        "/api/v1/lead-capture",
        json={
            "session_id": session.session_id,
            "field_name": "full_name",
            "value": "Ali Khan",
        },
    )

    assert name_response.status_code == 200
    assert name_response.json()["next_required_field"] == "email"
    assert name_response.json()["lead_complete"] is False

    email_response = client.post(
        "/api/v1/lead-capture",
        json={
            "session_id": session.session_id,
            "field_name": "email",
            "value": "ali@example.com",
        },
    )

    assert email_response.status_code == 200
    assert email_response.json()["next_required_field"] == "contact_number"
    assert email_response.json()["lead_complete"] is False

    phone_response = client.post(
        "/api/v1/lead-capture",
        json={
            "session_id": session.session_id,
            "field_name": "contact_number",
            "value": "+923001234567",
        },
    )

    assert phone_response.status_code == 200
    assert phone_response.json()["next_required_field"] is None
    assert phone_response.json()["lead_complete"] is True

    assert session.lead_state.full_name == "Ali Khan"
    assert session.lead_state.email == "ali@example.com"
    assert session.lead_state.contact_number == "+923001234567"    