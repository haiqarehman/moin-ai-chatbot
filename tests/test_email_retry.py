from app.services.email_retry import RetryingEmailService
from app.services.mock_email_service import MockEmailService


def test_email_retry_succeeds_after_temporary_failures():
    email_service = MockEmailService(
        failures_before_success=2,
    )

    retry_service = RetryingEmailService(
        email_service,
        max_attempts=3,
    )

    result = retry_service.send(
        "info@moinsystemsai.com",
        "New Lead",
        "Test lead",
    )

    assert result is True
    assert retry_service.attempts == 3
    assert email_service.attempts == 3
    assert len(email_service.sent_emails) == 1


def test_email_retry_stops_after_max_attempts():
    email_service = MockEmailService(
        should_succeed=False,
    )

    retry_service = RetryingEmailService(
        email_service,
        max_attempts=3,
    )

    result = retry_service.send(
        "info@moinsystemsai.com",
        "New Lead",
        "Test lead",
    )

    assert result is False
    assert retry_service.attempts == 3
    assert email_service.attempts == 3
    assert email_service.sent_emails == []