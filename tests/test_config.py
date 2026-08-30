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


def test_sensitive_settings_have_safe_empty_defaults(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("SMTP_USERNAME", raising=False)
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)
    monkeypatch.delenv("APP_SECRET", raising=False)

    settings = Settings(
        _env_file=None,
    )

    assert settings.openai_api_key == ""
    assert settings.smtp_password == ""
    assert settings.app_secret == ""