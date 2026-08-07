"""Enterprise Multi-Workspace, Organization, Users, Roles & Permissions Platform module."""

from services.api.src.workspaces.router import router as workspaces_router

__all__ = ["workspaces_router"]
