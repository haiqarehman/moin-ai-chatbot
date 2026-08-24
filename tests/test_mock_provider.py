from app.services.llm.mock_provider import MockLLMProvider


def test_mock_llm_returns_response():
    provider = MockLLMProvider()

    result = provider.generate("Hello")

    assert result
    assert "Mock LLM" in result