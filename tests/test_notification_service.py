from app.services.mock_email_service import MockEmailService
from app.services.notification_service import NotificationService
from app.services.lead_state import LeadState


def test_notification_service_sends_lead_successfully():
    email_service = MockEmailService()
    notification_service = NotificationService(email_service)

    lead = LeadState(
        full_name="Ali Khan",
        email="ali@example.com",
        contact_number="+923001234567",
    )

    result = notification_service.notify_lead(lead)

    assert result is True
    assert len(email_service.sent_emails) == 1
    assert email_service.sent_emails[0]["recipient"] == (
        "info@moinsystemsai.com"
    )

    assert notification_service.last_delivery_status is not None
    assert notification_service.last_delivery_status.status == "sent"


def test_notification_service_returns_failure_when_email_fails():
    email_service = MockEmailService(
        should_succeed=False
    )
    notification_service = NotificationService(email_service)

    lead = LeadState(
        full_name="Ali Khan",
        email="ali@example.com",
        contact_number="+923001234567",
    )

    result = notification_service.notify_lead(lead)

    assert result is False
    assert email_service.sent_emails == []

    assert notification_service.last_delivery_status is not None
    assert notification_service.last_delivery_status.status == "failed"