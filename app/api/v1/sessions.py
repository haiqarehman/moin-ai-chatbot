from fastapi import APIRouter

from app.services.dependencies import session_manager


router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
)


@router.post("")
def create_session():
    session = session_manager.create_session()

    return {
        "session_id": session.session_id,
    }