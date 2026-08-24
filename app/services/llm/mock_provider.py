from app.services.llm.base import LLMProvider


class MockLLMProvider(LLMProvider):
    """
    Fake LLM provider for local development and testing.
    Does not require an API key.
    """

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        return (
            "This is a test response from the Mock LLM. "
            "The LLM integration flow is working correctly."
        )