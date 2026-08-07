from abc import ABC, abstractmethod
from typing import Any
import uuid

from services.api.src.workspaces.schemas import (
    InvitationCreateSchema,
    InvitationSchema,
    OrganizationCreateSchema,
    OrganizationSchema,
    SessionSchema,
    WorkspaceCreateSchema,
    WorkspaceSchema,
)


class IRBACEngine(ABC):

    @abstractmethod
    async def verify_permission(self, user_id: uuid.UUID, org_id: uuid.UUID, action: str) -> bool:
        pass


class ISessionManager(ABC):

    @abstractmethod
    async def force_logout_session(self, session_id: uuid.UUID) -> bool:
        pass
