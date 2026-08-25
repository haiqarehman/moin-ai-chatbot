from app.services.lead_capture import LeadCaptureService
from app.services.lead_state import LeadState


def test_capture_name_updates_lead_and_requests_email():
    lead = LeadState()
    service = LeadCaptureService()

    next_field = service.capture(
        lead,
        "full_name",
        "Ali Khan",
    )

    assert lead.full_name == "Ali Khan"
    assert next_field == "email"


def test_capture_email_updates_lead_and_requests_phone():
    lead = LeadState(
        full_name="Ali Khan",
    )
    service = LeadCaptureService()

    next_field = service.capture(
        lead,
        "email",
        "ali@example.com",
    )

    assert lead.email == "ali@example.com"
    assert next_field == "contact_number"


def test_capture_phone_completes_required_lead_fields():
    lead = LeadState(
        full_name="Ali Khan",
        email="ali@example.com",
    )
    service = LeadCaptureService()

    next_field = service.capture(
        lead,
        "contact_number",
        "+923001234567",
    )

    assert lead.contact_number == "+923001234567"
    assert next_field is None
    assert lead.is_complete() is True


def test_capture_rejects_invalid_email():
    lead = LeadState(
        full_name="Ali Khan",
    )
    service = LeadCaptureService()

    try:
        service.capture(
            lead,
            "email",
            "invalid-email",
        )
        assert False
    except ValueError as exc:
        assert "Invalid email address" in str(exc)

    assert lead.email is None