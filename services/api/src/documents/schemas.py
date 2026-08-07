import re
import uuid
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class DocumentResponse(BaseModel):
    """Document metadata details output representation."""

    id: uuid.UUID
    organization_id: uuid.UUID
    owner_id: uuid.UUID
    filename: str
    original_filename: str
    file_type: str
    mime_type: str
    file_size: int
    storage_path: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentCreate(BaseModel):
    """Document metadata creation input schema."""

    filename: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Sanitized filename on storage",
    )
    original_filename: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Original uploaded filename",
    )
    file_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="File extension type (e.g., PDF)",
    )
    mime_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="RFC 2045 Media MIME type",
    )
    file_size: int = Field(
        ...,
        gt=0,
        description="Size of the file in bytes",
    )
    storage_path: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description="Internal storage path URI",
    )

    @field_validator("filename", "original_filename")
    @classmethod
    def validate_filename_security(cls, v: str) -> str:
        """Prevent path traversal vulnerabilities in filenames."""
        if "/" in v or "\\" in v or ".." in v:
            raise ValueError(
                "Filename cannot contain slashes, backslashes, "
                "or path traversal sequences"
            )
        return v

    @field_validator("file_type")
    @classmethod
    def validate_and_normalize_file_type(cls, v: str) -> str:
        """Ensure file extension type is uppercase and alphanumeric."""
        cleaned = v.strip().upper()
        if not cleaned:
            raise ValueError("File type cannot be empty")
        if not re.match(r"^[A-Z0-9]+$", cleaned):
            raise ValueError("File type must contain only alphanumeric characters")
        return cleaned

    @field_validator("mime_type")
    @classmethod
    def validate_mime_type_format(cls, v: str) -> str:
        """Validate structure conforms to standard type/subtype syntax."""
        cleaned = v.strip().lower()
        if not re.match(r"^[a-z0-9.+-]+/[a-z0-9.+-]+$", cleaned):
            raise ValueError("MIME type must be in 'type/subtype' format")
        return cleaned


class DocumentUpdate(BaseModel):
    """Document metadata update input schema."""

    filename: str | None = Field(None, min_length=1, max_length=255)
    file_type: str | None = Field(None, min_length=1, max_length=50)
    mime_type: str | None = Field(None, min_length=1, max_length=100)

    @field_validator("filename")
    @classmethod
    def validate_filename_security(cls, v: str | None) -> str | None:
        """Prevent path traversal vulnerabilities if updating filename."""
        if v is None:
            return v
        if "/" in v or "\\" in v or ".." in v:
            raise ValueError(
                "Filename cannot contain slashes, backslashes, "
                "or path traversal sequences"
            )
        return v

    @field_validator("file_type")
    @classmethod
    def validate_and_normalize_file_type(cls, v: str | None) -> str | None:
        """Ensure updated file extension type is uppercase and alphanumeric."""
        if v is None:
            return v
        cleaned = v.strip().upper()
        if not cleaned:
            raise ValueError("File type cannot be empty")
        if not re.match(r"^[A-Z0-9]+$", cleaned):
            raise ValueError("File type must contain only alphanumeric characters")
        return cleaned

    @field_validator("mime_type")
    @classmethod
    def validate_mime_type_format(cls, v: str | None) -> str | None:
        """Validate structure conforms to standard type/subtype syntax if updated."""
        if v is None:
            return v
        cleaned = v.strip().lower()
        if not re.match(r"^[a-z0-9.+-]+/[a-z0-9.+-]+$", cleaned):
            raise ValueError("MIME type must be in 'type/subtype' format")
        return cleaned
