from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.dependencies import session_manager
from app.services.lead_capture import LeadCaptureService


router = APIRouter(
    prefix="/lead-capture",
    tags=["lead-capture"],
)

lead_capture_service = LeadCaptureService()


class LeadCaptureRequest(BaseModel):
    session_id: str
    field_name: str
    value: str


@router.post("")
def capture_lead(request: LeadCaptureRequest):
    session = session_manager.get_session(request.session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    try:
        next_field = lead_capture_service.capture(
            session.lead_state,
            request.field_name,
            request.value,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    return {
        "session_id": session.session_id,
        "next_required_field": next_field,
        "lead_complete": session.lead_state.is_complete(),
    }