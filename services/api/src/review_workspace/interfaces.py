import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class IReviewService(ABC):
    """Interface orchestrating data reviews, manual edits, and approvals."""

    @abstractmethod
    async def get_session_details(self, session_id: uuid.UUID) -> dict[str, Any]:
        """Consolidate OCR, DOM, mapped values, and unmapped entities."""
        pass

    @abstractmethod
    async def apply_manual_correction(
        self,
        item_id: uuid.UUID,
        corrector_id: uuid.UUID,
        new_value: str,
        reason: str | None,
    ) -> dict[str, Any]:
        """Save manual value overrides, tracking previous/updated properties."""
        pass

    @abstractmethod
    async def submit_session_approval(
        self, session_id: uuid.UUID, reviewer_id: uuid.UUID
    ) -> bool:
        """Submit final approval of the review session."""
        pass


class IValidationChecker(ABC):
    """Interface executing standard validation runs on review item data."""

    @abstractmethod
    async def validate_session_items(
        self, items: Sequence[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Validate email format, phone format, and required fields."""
        pass
