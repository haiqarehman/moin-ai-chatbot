from app.services.chat_service import ChatService
from app.services.intent_router import IntentRouter
from app.services.lead_capture import LeadCaptureService
from app.services.session_manager import SessionManager
from app.services.llm.gemini_provider import GeminiProvider


class ChatFlow:
    def __init__(
        self,
        session_manager: SessionManager,
        intent_router: IntentRouter,
    ):
        self.session_manager = session_manager
        self.intent_router = intent_router
        self.lead_capture = LeadCaptureService()

        self.chat_service = ChatService(
            llm_provider=GeminiProvider(),
        )

    def process_message(
        self,
        session_id: str,
        message: str,
    ) -> str:
        session = self.session_manager.get_session(session_id)

        if session is None:
            raise ValueError("Session not found.")

        # -------------------------------------------------
        # If we are already collecting lead information,
        # process the user's message as the next lead field.
        # -------------------------------------------------
        if session.state == "lead_capture":
            field_name = session.lead_state.next_required_field()

            if field_name is None:
                return (
                    "Thank you. Your contact information has "
                    "already been captured."
                )

            try:
                next_field = self.lead_capture.capture(
                    session.lead_state,
                    field_name,
                    message,
                )
            except ValueError as exc:
                return str(exc)

            self.session_manager.add_message(
                session_id,
                "user",
                message,
            )

            if next_field == "email":
                return "Thank you. Please provide your email address."

            if next_field == "contact_number":
                return "Thank you. Please provide your contact number."

            if next_field is None:
                return (
                    "Thank you! Your contact information has been "
                    "captured successfully. Our team will get in touch "
                    "with you shortly."
                )

            return f"Please provide your {next_field.replace('_', ' ')}."

        # -------------------------------------------------
        # Normal intent detection
        # -------------------------------------------------
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

        # -------------------------------------------------
        # Start lead capture for buying / quotation intent
        # -------------------------------------------------
        if intent in {"quote_request", "buying_intent"}:
            self.session_manager.update_state(
                session_id,
                "lead_capture",
            )

            return (
                "I'd be happy to help. "
                "To discuss your project and provide the right guidance, "
                "I'll need your name, email, and contact number. "
                "Please start by providing your full name."
            )

        # -------------------------------------------------
        # Normal RAG + Gemini response
        # -------------------------------------------------
        return self.chat_service.answer(message)