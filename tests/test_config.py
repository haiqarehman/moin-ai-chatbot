from app.core.config import Settings


def test_sensitive_settings_are_loaded_from_configuration():
    settings = Settings(
        database_url="postgresql://test",
        openai_api_key="test-openai-key",
        smtp_username="test-user",
        smtp_password="test-password",
        app_secret="test-secret",
    )

    assert settings.database_url == "postgresql://test"
    assert settings.openai_api_key == "test-openai-key"
    assert settings.smtp_username == "test-user"
    assert settings.smtp_password == "test-password"
    assert settings.app_secret == "test-secret"


def test_sensitive_settings_have_safe_empty_defaults():
    settings = Settings()

    assert settings.openai_api_key == ""
    assert settings.smtp_password == ""
    assert settings.app_secret == ""