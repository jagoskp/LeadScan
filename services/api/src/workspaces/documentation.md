# Enterprise Multi-Workspace, Organization, Users, Roles & Permissions Platform (BF-019) Documentation

## Overview
The Enterprise Multi-Workspace Platform enables multiple organizations and workspaces to securely use the same LeadScan AI installation while guaranteeing strict data isolation across **BF-001 through BF-018**.

---

## Key Features
- **Multi-Tenant Organization Isolation**: Strict query isolation filtering by `organization_id` and `workspace_id`.
- **Role-Based Access Control (RBAC)**: Fine-grained permissions for `Owner`, `Admin`, `Manager`, `Operator`, `Reviewer`, and `Viewer`.
- **Tokenized Email Invitation System**: Secure token generation, 72-hour validity, accept/reject, and expiration tracking.
- **Active Session Security**: User active session listing, device tracking, and force logout capability.
- **Audit Logging**: Immutable security event logs.

---

## REST API Endpoints (`/api/v1/workspaces`)
- `GET /api/v1/workspaces/organizations`: List organizations.
- `POST /api/v1/workspaces/organizations`: Create organization.
- `GET /api/v1/workspaces`: List workspaces for an organization.
- `POST /api/v1/workspaces`: Create workspace.
- `POST /api/v1/workspaces/invite`: Send email invitation.
- `POST /api/v1/workspaces/accept-invitation`: Accept tokenized invitation.
- `GET /api/v1/workspaces/sessions`: List active login sessions.
- `POST /api/v1/workspaces/sessions/{id}/logout`: Force logout session.
