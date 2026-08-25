from app.services.session_manager import SessionManager


def test_create_session_returns_unique_session():
    manager = SessionManager()

    session1 = manager.create_session()
    session2 = manager.create_session()

    assert session1.session_id
    assert session2.session_id
    assert session1.session_id != session2.session_id
    assert session1.state == "general_query"
    assert session1.messages == []


def test_get_session_returns_created_session():
    manager = SessionManager()

    session = manager.create_session()

    result = manager.get_session(session.session_id)

    assert result is session


def test_get_session_returns_none_for_unknown_session():
    manager = SessionManager()

    result = manager.get_session("unknown-session-id")

    assert result is None


def test_add_message_persists_message_in_session():
    manager = SessionManager()

    session = manager.create_session()

    result = manager.add_message(
        session.session_id,
        "user",
        "What services do you provide?",
    )

    assert result is session
    assert len(session.messages) == 1
    assert session.messages[0] == {
        "role": "user",
        "content": "What services do you provide?",
    }
def test_update_state_changes_session_state():
    manager = SessionManager()

    session = manager.create_session()

    result = manager.update_state(
        session.session_id,
        "quote_request",
    )

    assert result is session
    assert session.state == "quote_request"


def test_update_state_returns_none_for_unknown_session():
    manager = SessionManager()

    result = manager.update_state(
        "unknown-session-id",
        "quote_request",
    )

    assert result is None    