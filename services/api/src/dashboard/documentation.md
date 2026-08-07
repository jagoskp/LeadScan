# Enterprise Command Center Dashboard & Analytics Platform (BF-018) Documentation

## Overview
The Enterprise Command Center serves as the **operational control center and main application UI** for LeadScan AI across all modules (**BF-001 through BF-016**).

---

## Key Features
- **Executive & Operations Dashboards**: KPI summary cards (Scans, Leads, Reviews, Workflows, Storage, Sync status).
- **Live Monitor**: Live scanning, OCR, AI processing, Review Queue, Sync Queue, and Workflow Queue.
- **Analytics Platform**: Lead Funnel, Conversion Rate, Review Statistics, Sync Success, and Duplicate Rate.
- **System Health Monitor**: Live telemetry for Database, Search Index, Asset Vault, Google Sync Engine, and Queues.
- **Command Palette (`Ctrl+K`)**: Keyboard-driven global search, navigation, and quick action runner.

---

## REST API Endpoints (`/api/v1/dashboard`)
- `GET /api/v1/dashboard/telemetry`: Control center live telemetry payload.
- `GET /api/v1/dashboard/analytics`: Analytical metrics and Lead Funnel.
- `GET /api/v1/dashboard/health`: Live system health checks.
- `GET /api/v1/dashboard/reports`: List saved report definitions.
- `POST /api/v1/dashboard/reports`: Create new report definition.
