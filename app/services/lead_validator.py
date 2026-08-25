import re


EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


def validate_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False

    return bool(EMAIL_PATTERN.match(email.strip()))