import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class GoogleAccount(Base):
    """Database model for connected Google Accounts."""

    __tablename__ = "google_accounts"

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
    account_email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )
    account_label: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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
    tokens: Mapped[list["GoogleToken"]] = relationship(
        "GoogleToken",
        back_populates="account",
        cascade="all, delete-orphan",
    )
    spreadsheets: Mapped[list["Spreadsheet"]] = relationship(
        "Spreadsheet",
        back_populates="account",
        cascade="all, delete-orphan",
    )


class GoogleToken(Base):
    """Database model storing OAuth2 tokens and Secret Vault linkages."""

    __tablename__ = "google_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    google_account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("google_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    secret_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("secrets.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    access_token_enc: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    refresh_token_enc: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    token_type: Mapped[str] = mapped_column(
        String(50),
        default="Bearer",
        nullable=False,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    scopes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    is_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    last_validated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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

    # Relationships
    account: Mapped["GoogleAccount"] = relationship(
        "GoogleAccount",
        back_populates="tokens",
    )


class Spreadsheet(Base):
    """Database model representing discovered Google Spreadsheets."""

    __tablename__ = "google_spreadsheets"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    google_account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("google_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    spreadsheet_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_favorite: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
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
    account: Mapped["GoogleAccount"] = relationship(
        "GoogleAccount",
        back_populates="spreadsheets",
    )
    worksheets: Mapped[list["Worksheet"]] = relationship(
        "Worksheet",
        back_populates="spreadsheet",
        cascade="all, delete-orphan",
    )


class Worksheet(Base):
    """Database model representing individual worksheets inside a spreadsheet."""

    __tablename__ = "google_worksheets"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    spreadsheet_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("google_spreadsheets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    worksheet_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    index: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    row_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    column_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    is_favorite: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
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
    spreadsheet: Mapped["Spreadsheet"] = relationship(
        "Spreadsheet",
        back_populates="worksheets",
    )
    columns: Mapped[list["SpreadsheetColumn"]] = relationship(
        "SpreadsheetColumn",
        back_populates="worksheet",
        cascade="all, delete-orphan",
    )


class SpreadsheetColumn(Base):
    """Database model for discovered Google Sheet header columns."""

    __tablename__ = "google_spreadsheet_columns"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    worksheet_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("google_worksheets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    data_type: Mapped[str] = mapped_column(
        String(50),
        default="String",
        nullable=False,
    )
    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_custom: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
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
    worksheet: Mapped["Worksheet"] = relationship(
        "Worksheet",
        back_populates="columns",
    )


class GoogleSyncJob(Base):
    """Database model for Google Sheets synchronization job runs."""

    __tablename__ = "google_sync_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("connector_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    spreadsheet_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    worksheet_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    sync_mode: Mapped[str] = mapped_column(
        String(50),
        default="Manual",
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="Pending",
        nullable=False,
        index=True,
    )
    total_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    processed_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    success_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    failed_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    max_retries: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False,
    )
    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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

    # Relationships
    history_records: Mapped[list["GoogleSyncHistory"]] = relationship(
        "GoogleSyncHistory",
        back_populates="job",
        cascade="all, delete-orphan",
    )
    validations: Mapped[list["MappingValidation"]] = relationship(
        "MappingValidation",
        back_populates="job",
        cascade="all, delete-orphan",
    )


class GoogleSyncHistory(Base):
    """Database model logging sync outcome details, durations, and validation reports."""

    __tablename__ = "google_sync_histories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("google_sync_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    connector_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("connectors.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    spreadsheet_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    worksheet_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    rows_processed: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    duration_ms: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    retries: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    validation_result: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    job: Mapped["GoogleSyncJob"] = relationship(
        "GoogleSyncJob",
        back_populates="history_records",
    )


class MappingValidation(Base):
    """Database model for storing pre-sync mapping validation reports."""

    __tablename__ = "google_mapping_validations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("google_sync_jobs.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    profile_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("connector_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    sheet_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    worksheet_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="Valid",
        nullable=False,
    )
    missing_columns: Mapped[dict] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    new_columns: Mapped[dict] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    report_data: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    job: Mapped["GoogleSyncJob | None"] = relationship(
        "GoogleSyncJob",
        back_populates="validations",
    )
    suggestions: Mapped[list["RemappingSuggestion"]] = relationship(
        "RemappingSuggestion",
        back_populates="validation",
        cascade="all, delete-orphan",
    )


class RemappingSuggestion(Base):
    """Database model tracking intelligent auto-remapping suggestions."""

    __tablename__ = "google_remapping_suggestions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    validation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("google_mapping_validations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_column: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    target_entity_field: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    similarity_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    suggestion_reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="Pending",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    validation: Mapped["MappingValidation"] = relationship(
        "MappingValidation",
        back_populates="suggestions",
    )
