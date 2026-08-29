from app.services.chat_service import ChatService
from app.services.intent_router import IntentRouter
from app.services.lead_capture import LeadCaptureService
from app.services.session_manager import SessionManager
from app.services.llm.gemini_provider import GeminiProvider
from app.services.notification_service import NotificationService
from app.services.email_retry import RetryingEmailService
from app.services.smtp_email_service import SMTPEmailService


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

        self.notification_service = NotificationService(
            email_service=RetryingEmailService(
                SMTPEmailService(),
                max_attempts=3,
            ),
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
                self.lead_capture.capture(
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

            # -------------------------------------------------
            # Lead collection is complete.
            # Send notification email.
            # -------------------------------------------------
            if session.lead_state.is_complete():
                self.notification_service.notify_lead(
                    session.lead_state
                )

                return (
                    "Thank you! Your contact information has been "
                    "captured successfully. Our team will get in touch "
                    "with you shortly."
                )

            next_field = session.lead_state.next_required_field()

            if next_field == "email":
                return (
                    "Thank you. Please provide your email address."
                )

            if next_field == "contact_number":
                return (
                    "Thank you. Please provide your contact number."
                )

            return (
                f"Please provide your "
                f"{next_field.replace('_', ' ')}."
            )

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