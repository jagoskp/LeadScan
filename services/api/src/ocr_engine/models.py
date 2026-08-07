import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class OCRJob(Base):
    """Database model for tracking raw text extraction requests."""

    __tablename__ = "ocr_engine_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    input_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False,
    )
    languages: Mapped[list[str]] = mapped_column(
        JSON,
        default=lambda: ["en"],
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
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

    # Relationships
    pages: Mapped[list["OCRPage"]] = relationship(
        "OCRPage",
        back_populates="job",
        cascade="all, delete-orphan",
    )

    # Core relationship bindings
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="OCRJob.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="OCRJob.organization_id == Organization.id",
    )


class OCRPage(Base):
    """Database model for storing page-level extracted layout text."""

    __tablename__ = "ocr_pages"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ocr_engine_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    page_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    raw_text: Mapped[str] = mapped_column(
        nullable=False,
    )
    width: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    detected_language: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    job: Mapped["OCRJob"] = relationship(
        "OCRJob",
        back_populates="pages",
    )
    blocks: Mapped[list["OCRBlock"]] = relationship(
        "OCRBlock",
        back_populates="page",
        cascade="all, delete-orphan",
    )


class OCRBlock(Base):
    """Database model for structural paragraphs or text block zones."""

    __tablename__ = "ocr_blocks"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    page_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ocr_pages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    block_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    block_type: Mapped[str] = mapped_column(
        String(50),
        default="TEXT",
        nullable=False,
    )
    bounding_box: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    page: Mapped["OCRPage"] = relationship(
        "OCRPage",
        back_populates="blocks",
    )
    lines: Mapped[list["OCRLine"]] = relationship(
        "OCRLine",
        back_populates="block",
        cascade="all, delete-orphan",
    )


class OCRLine(Base):
    """Database model for individual lines of extracted text within a block."""

    __tablename__ = "ocr_lines"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    block_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ocr_blocks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    line_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    raw_text: Mapped[str] = mapped_column(
        nullable=False,
    )
    bounding_box: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    block: Mapped["OCRBlock"] = relationship(
        "OCRBlock",
        back_populates="lines",
    )
    words: Mapped[list["OCRWord"]] = relationship(
        "OCRWord",
        back_populates="line",
        cascade="all, delete-orphan",
    )


class OCRWord(Base):
    """Database model for specific parsed words with spacing boundaries."""

    __tablename__ = "ocr_words"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    line_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ocr_lines.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    word_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        nullable=False,
    )
    bounding_box: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    char_start: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    char_end: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    line: Mapped["OCRLine"] = relationship(
        "OCRLine",
        back_populates="words",
    )


class OCRMetadata(Base):
    """Database model for storing key-value latency or provider execution metrics."""

    __tablename__ = "ocr_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ocr_engine_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    value: Mapped[str] = mapped_column(
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationship bindings
    job: Mapped["OCRJob"] = relationship(
        "OCRJob",
        primaryjoin="OCRMetadata.job_id == OCRJob.id",
    )
