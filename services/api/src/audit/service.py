import uuid
from collections.abc import Sequence

from services.api.src.audit.exceptions import (
    AdminAccessRequiredException,
    AuditLogNotFoundException,
    InvalidEventValidationException,
)
from services.api.src.audit.models import ActivityLog, AuditLog, SecurityEvent
from services.api.src.audit.repository import (
    ActivityLogRepository,
    AuditLogRepository,
    SecurityEventRepository,
)
from services.api.src.audit.schemas import (
    ActivityLogCreate,
    AuditLogCreate,
    SecurityEventCreate,
)
from services.api.src.auth.models import User


class AuditService:
    """Service orchestrating the Audit & Activity timeline business logic."""

    def __init__(
        self,
        audit_repo: AuditLogRepository,
        activity_repo: ActivityLogRepository,
        security_repo: SecurityEventRepository,
    ) -> None:
        self.audit_repo = audit_repo
        self.activity_repo = activity_repo
        self.security_repo = security_repo

    async def _get_admin_org_ids(self, user: User) -> list[uuid.UUID]:
        """Helper to get organization IDs where the user has Admin/Owner privileges."""
        memberships = await self.audit_repo.get_user_memberships(user.id)
        return [
            m.organization_id
            for m in memberships
            if getattr(m, "role", "Member") in ("Owner", "Admin")
        ]

    async def _get_member_org_ids(self, user: User) -> list[uuid.UUID]:
        """Helper to get all organization IDs where the user is a member."""
        memberships = await self.audit_repo.get_user_memberships(user.id)
        return [m.organization_id for m in memberships]

    async def get_resource_organization_id(
        self, resource_type: str, resource_id: str
    ) -> uuid.UUID | None:
        """Resolve the organization ID associated with a resource dynamically."""
        try:
            res_uuid = uuid.UUID(resource_id)
        except ValueError:
            return None

        from sqlalchemy import select

        if resource_type.lower() == "document":
            from services.api.src.documents.models import Document

            stmt = select(Document.organization_id).where(Document.id == res_uuid)
            res = await self.audit_repo.session.execute(stmt)
            return res.scalar()
        elif resource_type.lower() == "ocrjob":
            from services.api.src.ocr.models import OCRJob

            stmt = select(OCRJob.organization_id).where(OCRJob.id == res_uuid)
            res = await self.audit_repo.session.execute(stmt)
            return res.scalar()
        elif resource_type.lower() == "aijob":
            from services.api.src.ai.models import AIJob

            stmt = select(AIJob.organization_id).where(AIJob.id == res_uuid)
            res = await self.audit_repo.session.execute(stmt)
            return res.scalar()
        elif resource_type.lower() == "workflow":
            from services.api.src.workflow.models import Workflow

            stmt = select(Workflow.organization_id).where(Workflow.id == res_uuid)
            res = await self.audit_repo.session.execute(stmt)
            return res.scalar()

        return None

    # ----------------------------------------------------
    # Audit Logs
    # ----------------------------------------------------

    async def create_audit_log(self, data: AuditLogCreate) -> AuditLog:
        """Persist a new system audit log."""
        log = AuditLog(
            user_id=data.user_id,
            organization_id=data.organization_id,
            event_type=data.event_type.value,
            severity=data.severity.value,
            action=data.action,
            resource_type=data.resource_type,
            resource_id=data.resource_id,
            document_id=data.document_id,
            ocr_job_id=data.ocr_job_id,
            ai_job_id=data.ai_job_id,
            workflow_id=data.workflow_id,
            status=data.status,
            ip_address=data.ip_address,
            user_agent=data.user_agent,
            details=data.details,
        )
        return await self.audit_repo.create(log)

    async def get_audit_log(self, log_id: uuid.UUID, user: User) -> AuditLog:
        """Retrieve a specific audit log, checking user/org access permissions."""
        log = await self.audit_repo.get_by_id(log_id)
        if not log:
            raise AuditLogNotFoundException()

        member_org_ids = await self._get_member_org_ids(user)

        # Allow if personal log, or user is a member of the log's organization
        if log.user_id != user.id:
            if not log.organization_id or log.organization_id not in member_org_ids:
                raise AuditLogNotFoundException()

        return log

    async def list_audit_logs(
        self,
        user: User,
        organization_id: uuid.UUID | None = None,
        event_type: str | None = None,
        severity: str | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[AuditLog], int]:
        """List audit logs, enforcing admin check for organization-wide queries."""
        admin_org_ids = await self._get_admin_org_ids(user)

        if organization_id:
            if organization_id not in admin_org_ids:
                raise AdminAccessRequiredException(
                    "Only organization administrators can view "
                    "organization-wide audit logs."
                )
            org_filters = [organization_id]
            user_filter_id = None
        else:
            # Fallback: personal logs + logs from orgs where they are admin
            org_filters = admin_org_ids
            user_filter_id = user.id

        return await self.audit_repo.list_logs(
            user_id=user_filter_id,
            organization_ids=org_filters,
            event_type=event_type,
            severity=severity,
            search=search,
            skip=skip,
            limit=limit,
        )

    # ----------------------------------------------------
    # Activity Logs
    # ----------------------------------------------------

    async def create_activity_log(self, data: ActivityLogCreate) -> ActivityLog:
        """Persist a new user activity log."""
        log = ActivityLog(
            user_id=data.user_id,
            organization_id=data.organization_id,
            action=data.action,
            resource_type=data.resource_type,
            resource_id=data.resource_id,
            document_id=data.document_id,
            ocr_job_id=data.ocr_job_id,
            ai_job_id=data.ai_job_id,
            workflow_id=data.workflow_id,
            details=data.details,
        )
        return await self.activity_repo.create(log)

    async def list_activity_logs(
        self,
        user: User,
        organization_id: uuid.UUID | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[ActivityLog], int]:
        """List activity logs, ensuring membership context alignment."""
        member_org_ids = await self._get_member_org_ids(user)

        if organization_id:
            if organization_id not in member_org_ids:
                raise AdminAccessRequiredException(
                    "User is not a member of the specified organization."
                )
            org_filters = [organization_id]
            user_filter_id = None
        else:
            org_filters = member_org_ids
            user_filter_id = user.id

        return await self.activity_repo.list_activities(
            user_id=user_filter_id,
            organization_ids=org_filters,
            resource_type=resource_type,
            resource_id=resource_id,
            skip=skip,
            limit=limit,
        )

    async def get_user_timeline(
        self, user: User, target_user_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[ActivityLog]:
        """Retrieve activity logs timeline for a user, enforcing security boundaries."""
        if target_user_id == user.id:
            return await self.activity_repo.get_user_timeline(
                target_user_id, skip, limit
            )

        # To access another user's timeline, caller must be admin
        # in a shared organization
        admin_org_ids = await self._get_admin_org_ids(user)
        if not admin_org_ids:
            raise AdminAccessRequiredException()

        # Check target user's memberships
        target_memberships = await self.audit_repo.get_user_memberships(target_user_id)
        target_org_ids = [m.organization_id for m in target_memberships]

        shared_admins = set(admin_org_ids).intersection(target_org_ids)
        if not shared_admins:
            raise AdminAccessRequiredException(
                "Cannot query target user timeline without administrative access."
            )

        return await self.activity_repo.get_user_timeline(target_user_id, skip, limit)

    async def get_resource_timeline(
        self,
        user: User,
        resource_type: str,
        resource_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ActivityLog]:
        """Retrieve resource activities chronologically, checking member access."""
        org_id = await self.get_resource_organization_id(resource_type, resource_id)
        if not org_id:
            raise InvalidEventValidationException(
                f"Resource of type '{resource_type}' with ID "
                f"'{resource_id}' does not exist."
            )

        member_org_ids = await self._get_member_org_ids(user)
        if org_id not in member_org_ids:
            raise AdminAccessRequiredException(
                "Access to target resource timeline is forbidden."
            )

        return await self.activity_repo.get_resource_timeline(
            resource_type=resource_type, resource_id=resource_id, skip=skip, limit=limit
        )

    # ----------------------------------------------------
    # Security Events
    # ----------------------------------------------------

    async def create_security_event(self, data: SecurityEventCreate) -> SecurityEvent:
        """Persist a new security or authentication event log."""
        event = SecurityEvent(
            user_id=data.user_id,
            organization_id=data.organization_id,
            event_type=data.event_type,
            severity=data.severity.value,
            ip_address=data.ip_address,
            user_agent=data.user_agent,
            metadata_log=data.metadata_log,
        )
        return await self.security_repo.create(event)

    async def list_security_events(
        self,
        user: User,
        organization_id: uuid.UUID | None = None,
        event_type: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[SecurityEvent], int]:
        """List security event records. Organization lookups require admin access."""
        admin_org_ids = await self._get_admin_org_ids(user)

        if organization_id:
            if organization_id not in admin_org_ids:
                raise AdminAccessRequiredException(
                    "Only organization administrators can view "
                    "organization-wide security events."
                )
            org_filters = [organization_id]
            user_filter_id = None
        else:
            org_filters = admin_org_ids
            user_filter_id = user.id

        return await self.security_repo.list_events(
            user_id=user_filter_id,
            organization_ids=org_filters,
            event_type=event_type,
            skip=skip,
            limit=limit,
        )
