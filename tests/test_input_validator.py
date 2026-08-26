from app.services.input_validator import (
    MAX_LEAD_FIELD_LENGTH,
    MAX_MESSAGE_LENGTH,
    validate_lead_field_length,
    validate_message_length,
)


def test_valid_message_length_is_accepted():
    assert validate_message_length("Hello, I need information.") is True


def test_empty_message_is_rejected():
    assert validate_message_length("") is False
    assert validate_message_length("   ") is False


def test_oversized_message_is_rejected():
    message = "a" * (MAX_MESSAGE_LENGTH + 1)

    assert validate_message_length(message) is False


def test_valid_lead_field_is_accepted():
    assert validate_lead_field_length("Ali Khan") is True


def test_oversized_lead_field_is_rejected():
    value = "a" * (MAX_LEAD_FIELD_LENGTH + 1)

    assert validate_lead_field_length(value) is False


def test_empty_lead_field_is_rejected():
    assert validate_lead_field_length("") is False
    assert validate_lead_field_length("   ") is False