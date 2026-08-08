import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import UTC, datetime

from services.api.src.workspaces.invitations import InvitationEngine
from services.api.src.workspaces.models import Invitation, Role, Session, TenantOrganization, Workspace
from services.api.src.workspaces.organization import OrganizationManager
from services.api.src.workspaces.permissions import RBACEngine
from services.api.src.workspaces.schemas import InvitationCreateSchema, OrganizationCreateSchema, WorkspaceCreateSchema
from services.api.src.workspaces.service import WorkspacePlatformService
from services.api.src.workspaces.validators import validate_role_name
from services.api.src.workspaces.workspace import WorkspaceManager


def test_role_validator():
    assert validate_role_name("Owner") == "Owner"
    assert validate_role_name("Admin") == "Admin"
    assert validate_role_name("Viewer") == "Viewer"
    with pytest.raises(Exception):
        validate_role_name("INVALID_ROLE")


@pytest.fixture
def mock_db():
    db = AsyncMock()
    now = datetime.now(UTC)
    org_id = uuid.uuid4()
    user_id = uuid.uuid4()

    mock_org = TenantOrganization(
        id=org_id,
        name="Acme Enterprise Corp",
        logo_url=None,
        timezone="UTC",
        status="active",
        created_at=now,
        updated_at=now,
    )

    mock_ws = Workspace(
        id=uuid.uuid4(),
        organization_id=org_id,
        name="Sales Workspace",
        is_default=True,
        created_at=now,
    )

    mock_inv = Invitation(
        id=uuid.uuid4(),
        organization_id=org_id,
        email="operator@acme.com",
        role_name="Operator",
        token="token_abc_123",
        status="pending",
        expires_at=now,
        created_at=now,
    )

    mock_session = Session(
        id=uuid.uuid4(),
        user_id=user_id,
        device_info="Chrome 120 (Windows)",
        ip_address="127.0.0.1",
        is_active=True,
        last_active_at=now,
        created_at=now,
    )

    async def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        res.scalars.return_value.first.return_value = mock_inv
        res.scalars.return_value.all.return_value = [mock_org]
        return res

    async def mock_get(entity_cls, entity_id):
        if entity_cls == TenantOrganization:
            return mock_org
        if entity_cls == Session:
            return mock_session
        return mock_org

    db.execute.side_effect = mock_execute
    db.get.side_effect = mock_get
    return db, org_id, user_id, mock_inv, mock_session


@pytest.mark.asyncio
async def test_organization_and_workspace_lifecycle(mock_db):
    db, org_id, _, _, _ = mock_db
    service = WorkspacePlatformService(db)

    org_req = OrganizationCreateSchema(name="Acme Enterprise Corp")
    org = await service.create_organization(org_req)
    assert org.name == "Acme Enterprise Corp"

    ws_req = WorkspaceCreateSchema(organization_id=org_id, name="Sales Workspace")
    ws = await service.create_workspace(ws_req)
    assert ws.name == "Sales Workspace"


@pytest.mark.asyncio
async def test_invitation_engine_and_session_logout(mock_db):
    db, org_id, user_id, mock_inv, mock_session = mock_db
    service = WorkspacePlatformService(db)

    inv_req = InvitationCreateSchema(organization_id=org_id, email="operator@acme.com", role_name="Operator")
    inv = await service.invite_user(inv_req)
    assert inv.email == "operator@acme.com"

    success = await service.force_logout_session(mock_session.id)
    assert success is True
