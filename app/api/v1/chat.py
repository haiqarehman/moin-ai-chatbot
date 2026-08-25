from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.chat_flow import ChatFlow
from app.services.dependencies import session_manager
from app.services.intent_router import IntentRouter


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


chat_flow = ChatFlow(
    session_manager=session_manager,
    intent_router=IntentRouter(),
)


class ChatMessageRequest(BaseModel):
    session_id: str
    message: str


class ChatMessageResponse(BaseModel):
    session_id: str
    state: str
    response: str


@router.post("/messages", response_model=ChatMessageResponse)
def send_message(request: ChatMessageRequest):
    session = session_manager.get_session(request.session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    try:
        response = chat_flow.process_message(
            request.session_id,
            request.message,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    return ChatMessageResponse(
        session_id=session.session_id,
        state=session.state,
        response=response,
    )