from app.services.lead_state import LeadState


def test_new_lead_requires_full_name():
    lead = LeadState()

    assert lead.next_required_field() == "full_name"
    assert lead.is_complete() is False


def test_lead_requires_email_after_name():
    lead = LeadState(
        full_name="Ali Khan",
    )

    assert lead.next_required_field() == "email"
    assert lead.is_complete() is False


def test_lead_requires_phone_after_name_and_email():
    lead = LeadState(
        full_name="Ali Khan",
        email="ali@example.com",
    )

    assert lead.next_required_field() == "contact_number"
    assert lead.is_complete() is False


def test_lead_is_complete_when_required_fields_are_present():
    lead = LeadState(
        full_name="Ali Khan",
        email="ali@example.com",
        contact_number="+923001234567",
    )

    assert lead.next_required_field() is None
    assert lead.is_complete() is True
def test_update_field_updates_lead_information():
    lead = LeadState()

    lead.update_field("full_name", "Ali Khan")
    lead.update_field("email", "ali@example.com")

    assert lead.full_name == "Ali Khan"
    assert lead.email == "ali@example.com"
    assert lead.next_required_field() == "contact_number"


def test_update_field_rejects_unknown_field():
    lead = LeadState()

    try:
        lead.update_field("unknown_field", "some value")
        assert False
    except ValueError as exc:
        assert "Unknown lead field" in str(exc)    