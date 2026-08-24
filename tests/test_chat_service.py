from unittest.mock import MagicMock, patch

from app.services.chat_service import ChatService


def test_chat_service_generates_answer_from_retrieved_context():
    fake_provider = MagicMock()
    fake_provider.generate.return_value = "MoinSystems AI provides AI services."

    fake_result = MagicMock()
    fake_result.category = "service"
    fake_result.intents = "service_discovery"
    fake_result.content = "MoinSystems AI provides AI chatbot services."

    with patch(
        "app.services.chat_service.retrieve_knowledge",
        return_value=[fake_result],
    ):
        with patch(
            "app.services.chat_service.build_context",
            return_value="Company provides AI chatbot services.",
        ):
            service = ChatService(fake_provider)

            result = service.answer(
                "What services does MoinSystems AI provide?"
            )

    assert result == "MoinSystems AI provides AI services."
    fake_provider.generate.assert_called_once()


def test_chat_service_handles_no_retrieved_context():
    fake_provider = MagicMock()

    with patch(
        "app.services.chat_service.retrieve_knowledge",
        return_value=[],
    ):
        service = ChatService(fake_provider)

        result = service.answer(
            "What is the weather in London today?"
        )

    assert "don't have enough information" in result
    fake_provider.generate.assert_not_called()
def test_chat_service_passes_system_prompt_to_llm():
    fake_provider = MagicMock()
    fake_provider.generate.return_value = "Test answer"

    fake_result = MagicMock()
    fake_result.category = "service"
    fake_result.intents = "service_discovery"
    fake_result.content = "MoinSystems AI provides AI services."

    with patch(
        "app.services.chat_service.retrieve_knowledge",
        return_value=[fake_result],
    ):
        with patch(
            "app.services.chat_service.build_context",
            return_value="Company provides AI services.",
        ):
            service = ChatService(fake_provider)

            service.answer("What services do you provide?")

    call_kwargs = fake_provider.generate.call_args.kwargs

    assert "system_prompt" in call_kwargs
    assert "MoinSystems AI assistant" in call_kwargs["system_prompt"]
    assert "Do not invent or guess information" in call_kwargs["system_prompt"]
def test_chat_service_end_to_end_flow():
    fake_provider = MagicMock()
    fake_provider.generate.return_value = (
        "MoinSystems AI provides AI chatbot services."
    )

    fake_result = MagicMock()
    fake_result.category = "service"
    fake_result.intents = "service_discovery"
    fake_result.content = (
        "MoinSystems AI provides AI chatbot services."
    )

    with patch(
        "app.services.chat_service.retrieve_knowledge",
        return_value=[fake_result],
    ) as mock_retriever:
        service = ChatService(fake_provider)

        result = service.answer(
            "What services does MoinSystems AI provide?"
        )

    assert result == (
        "MoinSystems AI provides AI chatbot services."
    )

    mock_retriever.assert_called_once_with(
        "What services does MoinSystems AI provide?"
    )

    fake_provider.generate.assert_called_once()   
def test_chat_service_returns_safe_response_when_no_context():
    fake_provider = MagicMock()

    with patch(
        "app.services.chat_service.retrieve_knowledge",
        return_value=[],
    ):
        service = ChatService(fake_provider)

        result = service.answer(
            "What is the weather in London today?"
        )

    assert result == (
        "I don't have enough information to answer "
        "that question."
    )

    fake_provider.generate.assert_not_called()

