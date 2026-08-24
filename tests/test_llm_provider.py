import pytest

from app.services.llm.base import LLMProvider


def test_llm_provider_is_abstract():
    with pytest.raises(TypeError):
        LLMProvider()

from unittest.mock import MagicMock, patch

from app.services.llm.openai_provider import OpenAIProvider


def test_openai_provider_generates_response():
    fake_response = MagicMock()
    fake_response.choices[0].message.content = "Test response"

    with patch("app.services.llm.openai_provider.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value = (
            fake_response
        )

        with patch.dict(
            "os.environ",
            {"OPENAI_API_KEY": "test-key"},
        ):
            provider = OpenAIProvider()

            result = provider.generate(
                "Hello",
                system_prompt="You are a helpful assistant.",
            )

            assert result == "Test response"

            mock_openai.return_value.chat.completions.create.assert_called_once()        