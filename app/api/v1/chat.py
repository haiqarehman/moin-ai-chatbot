import time
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.logging import get_logger
from app.services.chat_flow import ChatFlow
from app.services.dependencies import session_manager
from app.services.intent_router import IntentRouter
from app.services.rate_limiter import RateLimiter


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

logger = get_logger("chat")

chat_flow = ChatFlow(
    session_manager=session_manager,
    intent_router=IntentRouter(),
)

rate_limiter = RateLimiter(
    max_requests=60,
    window_seconds=60,
)


class ChatMessageRequest(BaseModel):
    session_id: str
    message: str


class ChatMessageResponse(BaseModel):
    session_id: str
    state: str
    response: str


@router.post("/messages", response_model=ChatMessageResponse)
def send_message(
    request: Request,
    body: ChatMessageRequest,
):
    client_id = request.client.host if request.client else "unknown"

    if not rate_limiter.allow(client_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded.",
        )

    request_id = str(uuid4())
    start_time = time.perf_counter()

    session = session_manager.get_session(body.session_id)

    if session is None:
        logger.warning(
            "request_id=%s session_id=%s event=session_not_found",
            request_id,
            body.session_id,
        )

        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    try:
        response = chat_flow.process_message(
            body.session_id,
            body.message,
        )
    except ValueError as exc:
        logger.error(
            "request_id=%s session_id=%s event=chat_error error=%s",
            request_id,
            body.session_id,
            str(exc),
        )

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    elapsed_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2,
    )

    logger.info(
        "request_id=%s session_id=%s state=%s "
        "message_length=%s latency_ms=%s event=chat_completed",
        request_id,
        session.session_id,
        session.state,
        len(body.message),
        elapsed_ms,
    )

    return ChatMessageResponse(
        session_id=session.session_id,
        state=session.state,
        response=response,
    )