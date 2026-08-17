from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class LeadSubmission(Base):
    __tablename__ = "lead_submission"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("chat_session.id"),
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
    )

    contact_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    company_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    project_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    service_interest: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    timeline: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    budget_range: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    source_page: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )