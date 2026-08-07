import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class MappingProfile(Base):
    """Database model storing dynamic mapping configurations."""

    __tablename__ = "mapping_profiles"

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
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
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
    rules: Mapped[list["MappingRule"]] = relationship(
        "MappingRule",
        back_populates="profile",
        cascade="all, delete-orphan",
    )
    targets: Mapped[list["MappingTarget"]] = relationship(
        "MappingTarget",
        back_populates="profile",
        cascade="all, delete-orphan",
    )
    history: Mapped[list["MappingHistory"]] = relationship(
        "MappingHistory",
        back_populates="profile",
        cascade="all, delete-orphan",
    )

    # Bindings
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="MappingProfile.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="MappingProfile.organization_id == Organization.id",
    )


class MappingRule(Base):
    """Database model representing a single key-to-key mapping instruction."""

    __tablename__ = "mapping_rules"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("mapping_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    source_entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    field_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    is_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    default_value: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    profile: Mapped["MappingProfile"] = relationship(
        "MappingProfile",
        back_populates="rules",
    )
    transformations: Mapped[list["TransformationRule"]] = relationship(
        "TransformationRule",
        back_populates="rule",
        cascade="all, delete-orphan",
    )
    validations: Mapped[list["ValidationRule"]] = relationship(
        "ValidationRule",
        back_populates="rule",
        cascade="all, delete-orphan",
    )


class MappingTarget(Base):
    """Database model configuring target integration destinations."""

    __tablename__ = "mapping_targets"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("mapping_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    configuration: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    profile: Mapped["MappingProfile"] = relationship(
        "MappingProfile",
        back_populates="targets",
    )


class MappedField(Base):
    """Database model representing mapped field outcomes."""

    __tablename__ = "mapped_fields"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
        index=True,
    )
    profile_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("mapping_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    rule_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("mapping_rules.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    value: Mapped[str] = mapped_column(
        nullable=False,
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

    # Bindings
    profile: Mapped["MappingProfile | None"] = relationship(
        "MappingProfile",
        primaryjoin="MappedField.profile_id == MappingProfile.id",
    )
    rule: Mapped["MappingRule | None"] = relationship(
        "MappingRule",
        primaryjoin="MappedField.rule_id == MappingRule.id",
    )


class TransformationRule(Base):
    """Database model representing string conversions rules linked to rules."""

    __tablename__ = "transformation_rules"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    rule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("mapping_rules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    transformation_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    parameters: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    sequence_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    rule: Mapped["MappingRule"] = relationship(
        "MappingRule",
        back_populates="transformations",
    )


class ValidationRule(Base):
    """Database model holding validation checks linked to mapping rules."""

    __tablename__ = "validation_rules"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    rule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("mapping_rules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    validation_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    parameters: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    rule: Mapped["MappingRule"] = relationship(
        "MappingRule",
        back_populates="validations",
    )


class UnmappedField(Base):
    """Database model preserving unmapped elements to prevent data loss."""

    __tablename__ = "unmapped_fields"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
        index=True,
    )
    profile_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("mapping_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    raw_text: Mapped[str] = mapped_column(
        nullable=False,
    )
    bounding_box: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Bindings
    profile: Mapped["MappingProfile | None"] = relationship(
        "MappingProfile",
        primaryjoin="UnmappedField.profile_id == MappingProfile.id",
    )


class MappingHistory(Base):
    """Database model storing historic revision snapshots of mapping profiles."""

    __tablename__ = "mapping_history"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("mapping_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    author_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    change_summary: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    snapshot: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    profile: Mapped["MappingProfile"] = relationship(
        "MappingProfile",
        back_populates="history",
    )

    # Bindings
    author: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="MappingHistory.author_id == User.id",
    )
