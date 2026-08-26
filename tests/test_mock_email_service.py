from app.services.mock_email_service import MockEmailService


def test_mock_email_service_sends_successfully():
    service = MockEmailService()

    result = service.send(
        "info@moinsystemsai.com",
        "New Lead",
        "Ali Khan has submitted a new lead.",
    )

    assert result is True
    assert len(service.sent_emails) == 1

    assert service.sent_emails[0] == {
        "recipient": "info@moinsystemsai.com",
        "subject": "New Lead",
        "body": "Ali Khan has submitted a new lead.",
    }


def test_mock_email_service_can_simulate_failure():
    service = MockEmailService(should_succeed=False)

    result = service.send(
        "info@moinsystemsai.com",
        "New Lead",
        "Ali Khan has submitted a new lead.",
    )

    assert result is False
    assert service.sent_emails == []