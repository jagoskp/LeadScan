# Enterprise Workflow, Follow-up & Automation Engine (BF-017) Documentation

## Overview
The Enterprise Workflow Automation Engine acts as the execution layer for LeadScan AI across all post-lead creation activities (**BF-001 through BF-016**).

---

## Core Capabilities
- **Workflow Triggers**: Lead Created, Status Changed, Review Approved, Google Sync Completed, Duplicate Merged.
- **Task Management**: Task creation, assignment, priority levels (`High`, `Medium`, `Low`), and completion.
- **Follow-up Activities**: Structured logging for Calls, WhatsApp, Emails, Meetings, Proposals, and Quotations.
- **SLA Engine**: Automatic response/resolution target calculation and breach detection.
- **Outbound Notification Queue**: Multi-channel dispatching (`in_app`, `email`, `sms`, `whatsapp`).

---

## REST API Endpoints (`/api/v1/workflows`)
- `GET /api/v1/workflows`: List active workflow rules.
- `POST /api/v1/workflows`: Create workflow rule.
- `GET /api/v1/workflows/tasks`: List task items.
- `POST /api/v1/workflows/tasks`: Create task.
- `POST /api/v1/workflows/tasks/{task_id}/complete`: Complete task.
- `GET /api/v1/workflows/followups`: List follow-up communications.
- `POST /api/v1/workflows/followups`: Schedule follow-up communication.
- `POST /api/v1/workflows/sla`: Initialize SLA targets.
