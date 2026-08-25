from app.services.intent_router import IntentRouter
from app.services.session_manager import SessionManager


class ChatFlow:
    def __init__(
        self,
        session_manager: SessionManager,
        intent_router: IntentRouter,
    ):
        self.session_manager = session_manager
        self.intent_router = intent_router

    def process_message(
        self,
        session_id: str,
        message: str,
    ) -> str:
        session = self.session_manager.get_session(session_id)

        if session is None:
            raise ValueError("Session not found.")

        intent = self.intent_router.route(message)

        self.session_manager.update_state(
            session_id,
            intent,
        )

        self.session_manager.add_message(
            session_id,
            "user",
            message,
        )

        if intent in {"quote_request", "buying_intent"}:
            return (
                "I'd be happy to help. "
                "To discuss your project and provide the right guidance, "
                "I'll need your name, email, and contact number."
            )

        return intent