from app.services.lead_validator import validate_email


def test_validate_email_accepts_valid_email():
    assert validate_email("ali@example.com") is True
    assert validate_email("john.doe@gmail.com") is True


def test_validate_email_rejects_invalid_email():
    assert validate_email("ali@") is False
    assert validate_email("ali@gmail") is False
    assert validate_email("ali example.com") is False
    assert validate_email("") is False


def test_validate_email_handles_whitespace():
    assert validate_email("  ali@example.com  ") is True