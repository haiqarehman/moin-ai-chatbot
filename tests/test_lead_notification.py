from app.services.lead_notification import (
    NOTIFICATION_RECIPIENT,
    build_lead_notification,
)
from app.services.lead_state import LeadState


def test_build_lead_notification_contains_lead_information():
    lead = LeadState(
        full_name="Ali Khan",
        email="ali@example.com",
        contact_number="+923001234567",
        company_name="ABC Solutions",
        project_summary="AI chatbot development",
        service_interest="Chatbot",
        timeline="2 months",
        budget_range="$5,000-$10,000",
    )

    notification = build_lead_notification(lead)

    assert notification["recipient"] == NOTIFICATION_RECIPIENT
    assert notification["subject"] == "New Lead Captured"

    assert "Ali Khan" in notification["body"]
    assert "ali@example.com" in notification["body"]
    assert "+923001234567" in notification["body"]
    assert "ABC Solutions" in notification["body"]
    assert "AI chatbot development" in notification["body"]
    assert "Chatbot" in notification["body"]
    assert "2 months" in notification["body"]
    assert "$5,000-$10,000" in notification["body"]


def test_build_lead_notification_handles_missing_optional_fields():
    lead = LeadState(
        full_name="Ali Khan",
        email="ali@example.com",
        contact_number="+923001234567",
    )

    notification = build_lead_notification(lead)

    assert "Not provided" in notification["body"]