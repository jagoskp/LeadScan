from abc import ABC, abstractmethod
from typing import Any
import uuid

from services.api.src.identity.schemas import (
    DuplicateMatchSchema,
    MergeExecuteRequest,
    MergeHistorySchema,
    MergePreviewResponse,
    RollbackHistorySchema,
)


class IIdentityMatcher(ABC):
    """Abstract interface for multi-rule identity matching."""

    @abstractmethod
    def evaluate_match(self, lead_a: Any, lead_b: Any) -> dict[str, Any]:
        pass


class IIdentityScorer(ABC):
    """Abstract interface for identity & confidence scoring."""

    @abstractmethod
    def compute_scores(self, match_eval: dict[str, Any]) -> dict[str, Any]:
        pass


class IMergeEngine(ABC):
    """Abstract interface for safe merge execution."""

    @abstractmethod
    async def execute_merge(
        self, request: MergeExecuteRequest, actor_id: uuid.UUID | None = None
    ) -> MergeHistorySchema:
        pass


class IRollbackEngine(ABC):
    """Abstract interface for merge rollback operations."""

    @abstractmethod
    async def rollback_merge(self, merge_history_id: uuid.UUID) -> RollbackHistorySchema:
        pass
