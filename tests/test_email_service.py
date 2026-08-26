import pytest

from app.services.email_service import EmailService


def test_email_service_cannot_be_used_without_implementation():
    with pytest.raises(TypeError):
        EmailService()