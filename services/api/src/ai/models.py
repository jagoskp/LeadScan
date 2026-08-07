import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.documents.models import Document
    from services.api.src.ocr.models import OCRResult
    from services.api.src.organization.models import Organization


class AIJob(Base):
    """AI Job model tracking analysis request configurations and states."""

    __tablename__ = "ai_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ocr_result_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ocr_results.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    prompt_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Unidirectional relationships
    document: Mapped["Document"] = relationship(
        "Document",
        foreign_keys=[document_id],
    )
    ocr_result: Mapped["OCRResult"] = relationship(
        "OCRResult",
        foreign_keys=[ocr_result_id],
    )
    organization: Mapped["Organization"] = relationship(
        "Organization",
        foreign_keys=[organization_id],
    )
    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=[owner_id],
    )

    # 1-to-1 relationship with result
    result: Mapped["AIResult | None"] = relationship(
        "AIResult",
        back_populates="job",
        cascade="all, delete-orphan",
        uselist=False,
    )


class AIResult(Base):
    """AI Result model tracking structured extractions and usage metrics."""

    __tablename__ = "ai_results"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    extracted_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    raw_response: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    tokens_used: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    ai_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Unidirectional/bidirectional relationships
    job: Mapped["AIJob"] = relationship(
        "AIJob",
        back_populates="result",
        foreign_keys=[job_id],
    )
    document: Mapped["Document"] = relationship(
        "Document",
        foreign_keys=[document_id],
    )
    organization: Mapped["Organization"] = relationship(
        "Organization",
        foreign_keys=[organization_id],
    )
