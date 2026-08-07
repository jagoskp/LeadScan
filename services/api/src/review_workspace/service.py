import uuid
from collections.abc import Sequence
from typing import Any

from services.api.src.review_workspace.enums import (
    ConfidenceLevel,
    ReviewApprovalStatus,
    ValidationIssueType,
)
from services.api.src.review_workspace.exceptions import (
    ReviewItemNotFoundException,
    ReviewSessionNotFoundException,
)
from services.api.src.review_workspace.interfaces import (
    IReviewService,
    IValidationChecker,
)
from services.api.src.review_workspace.models import (
    CorrectionHistory,
    ReviewItem,
    ReviewSession,
    ValidationIssue,
)
from services.api.src.review_workspace.repository import (
    ReviewItemRepository,
    ReviewSessionRepository,
)
from services.api.src.review_workspace.validators import (
    validate_email_format,
    validate_gst_format,
    validate_phone_format,
    validate_website_format,
)


class ReviewWorkspaceService(IReviewService, IValidationChecker):
    """Orchestrates manual edits, validation checks, and review sessions."""

    def __init__(
        self,
        session_repo: ReviewSessionRepository,
        item_repo: ReviewItemRepository,
    ) -> None:
        self.session_repo = session_repo
        self.item_repo = item_repo

    # ----------------------------------------------------
    # Session Ingestion & CRUD
    # ----------------------------------------------------

    async def create_session(self, document_id: uuid.UUID) -> ReviewSession:
        """Create a new review workspace session."""
        session = ReviewSession(
            document_id=document_id,
            status=ReviewApprovalStatus.PENDING.value,
        )
        await self.session_repo.create(session)

        # Seed items
        seed_data: list[dict[str, Any]] = [
            {
                "field": "company_name",
                "val": "LeadScan AI Corp.",
                "level": ConfidenceLevel.HIGH,
                "score": 0.99,
                "extra": False,
            },
            {
                "field": "contact_phone",
                "val": "+1-555-0199",
                "level": ConfidenceLevel.MEDIUM,
                "score": 0.85,
                "extra": False,
            },
            {
                "field": "contact_email",
                "val": "contact@leadscan",
                "level": ConfidenceLevel.LOW,
                "score": 0.65,
                "extra": False,
            },
            {
                "field": "gst_number",
                "val": "12345",
                "level": ConfidenceLevel.LOW,
                "score": 0.55,
                "extra": True,
            },
        ]

        for seed in seed_data:
            item = ReviewItem(
                session_id=session.id,
                field_name=seed["field"],
                original_value=seed["val"],
                current_value=seed["val"],
                confidence_score=seed["score"],
                confidence_level=seed["level"].value,
                is_extra_info=seed["extra"],
                status=ReviewApprovalStatus.PENDING.value,
                bounding_box={
                    "x": 0.1,
                    "y": 0.2,
                    "width": 0.3,
                    "height": 0.05,
                },
            )
            await self.item_repo.create_item(item)

        await self.re_evaluate_validation_issues(session.id)

        reloaded = await self.session_repo.get_by_id(session.id)
        if not reloaded:
            raise ReviewSessionNotFoundException()
        return reloaded

    async def list_active_sessions(self) -> Sequence[ReviewSession]:
        """List review sessions."""
        return await self.session_repo.list_sessions()

    # ----------------------------------------------------
    # IReviewService Implementation
    # ----------------------------------------------------

    async def get_session_details(self, session_id: uuid.UUID) -> dict[str, Any]:
        """Consolidate OCR, DOM, mapped values, and unmapped entities."""
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise ReviewSessionNotFoundException()

        items_list = []
        for item in session.items:
            items_list.append(
                {
                    "item_id": item.id,
                    "field_name": item.field_name,
                    "current_value": item.current_value,
                    "confidence_score": item.confidence_score,
                    "confidence_level": item.confidence_level,
                    "is_extra_info": item.is_extra_info,
                    "status": item.status,
                }
            )

        return {
            "session_id": session.id,
            "document_id": session.document_id,
            "status": session.status,
            "original_scan": "file:///path/to/mock/image.png",
            "ocr_result": (
                "LEADSCAN AI CORP. \n "
                "Phone: +1-555-0199 \n "
                "Email: contact@leadscan"
            ),
            "items": items_list,
            "validation_errors_count": len(session.validation_issues),
        }

    async def apply_manual_correction(
        self,
        item_id: uuid.UUID,
        corrector_id: uuid.UUID,
        new_value: str,
        reason: str | None,
    ) -> dict[str, Any]:
        """Save manual value overrides, tracking previous/updated properties."""
        item = await self.item_repo.get_item_by_id(item_id)
        if not item:
            raise ReviewItemNotFoundException()

        history = CorrectionHistory(
            item_id=item.id,
            reviewer_id=corrector_id,
            old_value=item.current_value,
            new_value=new_value,
            reason=reason,
        )
        await self.item_repo.create_correction(history)

        await self.item_repo.update_item_value(
            item_id=item.id,
            value=new_value,
            status=ReviewApprovalStatus.APPROVED.value,
        )

        await self.re_evaluate_validation_issues(item.session_id)

        updated_item = await self.item_repo.get_item_by_id(item_id)
        if not updated_item:
            raise ReviewItemNotFoundException()
        return {
            "item_id": updated_item.id,
            "field_name": updated_item.field_name,
            "current_value": updated_item.current_value,
            "status": updated_item.status,
        }

    async def submit_session_approval(
        self, session_id: uuid.UUID, reviewer_id: uuid.UUID
    ) -> bool:
        """Submit final approval of the review session."""
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise ReviewSessionNotFoundException()

        # Mark session approved
        await self.session_repo.update_session_status(
            session_id=session.id,
            status=ReviewApprovalStatus.APPROVED.value,
            reviewer_id=reviewer_id,
        )

        # Mark all pending items approved
        for item in session.items:
            await self.item_repo.update_item_value(
                item_id=item.id,
                value=item.current_value or "",
                status=ReviewApprovalStatus.APPROVED.value,
            )

        return True

    # ----------------------------------------------------
    # IValidationChecker Implementation
    # ----------------------------------------------------

    async def validate_session_items(
        self, items: Sequence[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Validate email format, phone format, and required fields."""
        issues = []
        for item in items:
            field = item.get("field_name", "")
            val = item.get("current_value")

            if not val:
                continue

            issue = self._check_item_issues(field, val)
            if issue:
                issues.append(issue)
        return issues

    def _check_item_issues(self, field: str, val: str) -> dict[str, Any] | None:
        """Perform validation format checks for email, phone, website, and GST."""
        if "email" in field.lower() and not validate_email_format(val):
            return {
                "field_name": field,
                "type": ValidationIssueType.INVALID_EMAIL,
                "msg": f"Email format '{val}' is invalid",
            }
        if "phone" in field.lower() and not validate_phone_format(val):
            return {
                "field_name": field,
                "type": ValidationIssueType.INVALID_PHONE,
                "msg": f"Phone format '{val}' is invalid",
            }
        if "website" in field.lower() and not validate_website_format(val):
            return {
                "field_name": field,
                "type": ValidationIssueType.INVALID_WEBSITE,
                "msg": f"Website format '{val}' is invalid",
            }
        if "gst" in field.lower() and not validate_gst_format(val):
            return {
                "field_name": field,
                "type": ValidationIssueType.INVALID_GST,
                "msg": f"GST format '{val}' is invalid",
            }
        return None

    # ----------------------------------------------------
    # Private Helpers
    # ----------------------------------------------------

    async def re_evaluate_validation_issues(self, session_id: uuid.UUID) -> None:
        """Run validation engine checks and persist issues list."""
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            return

        # 1. Clear old issues
        await self.item_repo.clear_validation_issues(session_id)

        # 2. Run validations
        items_dict = [
            {"field_name": item.field_name, "current_value": item.current_value}
            for item in session.items
        ]
        detected = await self.validate_session_items(items_dict)

        # 3. Save new issues
        for issue in detected:
            db_issue = ValidationIssue(
                session_id=session_id,
                field_name=issue["field_name"],
                issue_type=issue["type"].value,
                message=issue["msg"],
            )
            await self.item_repo.create_validation_issue(db_issue)
