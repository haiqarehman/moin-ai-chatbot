MAX_MESSAGE_LENGTH = 2000
MAX_LEAD_FIELD_LENGTH = 500


def validate_message_length(message: str) -> bool:
    if not isinstance(message, str):
        return False

    return 0 < len(message.strip()) <= MAX_MESSAGE_LENGTH


def validate_lead_field_length(value: str) -> bool:
    if not isinstance(value, str):
        return False

    return 0 < len(value.strip()) <= MAX_LEAD_FIELD_LENGTH