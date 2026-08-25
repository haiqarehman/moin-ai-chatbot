from app.services.chat_flow import ChatFlow
from app.services.intent_router import IntentRouter
from app.services.session_manager import SessionManager


def test_pricing_message_updates_session_and_requests_lead_details():
    session_manager = SessionManager()
    intent_router = IntentRouter()
    chat_flow = ChatFlow(
        session_manager,
        intent_router,
    )

    session = session_manager.create_session()

    result = chat_flow.process_message(
        session.session_id,
        "How much does an AI chatbot cost?",
    )

    assert session.state == "quote_request"

    assert session.messages[-1] == {
        "role": "user",
        "content": "How much does an AI chatbot cost?",
    }

    assert "name" in result.lower()
    assert "email" in result.lower()
    assert "contact number" in result.lower()


def test_general_message_updates_state_and_saves_message():
    session_manager = SessionManager()
    intent_router = IntentRouter()
    chat_flow = ChatFlow(
        session_manager,
        intent_router,
    )

    session = session_manager.create_session()

    result = chat_flow.process_message(
        session.session_id,
        "Tell me about your company.",
    )

    assert session.state == "general_query"

    assert session.messages[-1] == {
        "role": "user",
        "content": "Tell me about your company.",
    }

    assert result == "general_query"
def test_pricing_flow_answers_before_lead_capture():
    session_manager = SessionManager()
    intent_router = IntentRouter()

    chat_flow = ChatFlow(
        session_manager,
        intent_router,
    )

    session = session_manager.create_session()

    response = chat_flow.process_message(
        session.session_id,
        "I want a quote for an AI chatbot.",
    )

    assert response
    assert "name" in response.lower()
    assert "email" in response.lower()
    assert "contact number" in response.lower()

    assert session.state == "quote_request"
    assert session.lead_state.next_required_field() == "full_name"    