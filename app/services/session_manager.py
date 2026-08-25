from dataclasses import dataclass, field
from uuid import uuid4

from app.services.lead_state import LeadState


@dataclass
class ChatSession:
    session_id: str
    state: str = "general_query"
    messages: list[dict] = field(default_factory=list)
    lead_state: LeadState = field(default_factory=LeadState)


class SessionManager:
    def __init__(self):
        self._sessions: dict[str, ChatSession] = {}

    def create_session(self) -> ChatSession:
        session = ChatSession(
            session_id=str(uuid4())
        )

        self._sessions[session.session_id] = session

        return session

    def get_session(self, session_id: str) -> ChatSession | None:
        return self._sessions.get(session_id)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> ChatSession | None:
        session = self.get_session(session_id)

        if session is None:
            return None

        session.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

        return session

    def update_state(
        self,
        session_id: str,
        state: str,
    ) -> ChatSession | None:
        session = self.get_session(session_id)

        if session is None:
            return None

        session.state = state

        return session