# Enterprise Lead Repository & Contact Management Engine (BF-013) Documentation

## Overview
The Enterprise Lead Repository is the **master source of truth** for all lead, contact, and company records extracted across LeadScan AI. It ingests approved data from **BF-008 Review Workspace**, links to Google Sheets sync results (**BF-012**), and maintains full lineage to raw OCR/AI artifacts, original images, and DOM extractions.

---

## Domain Architecture
- `Lead`: Primary aggregate root containing title, status, priority, source, score, and owner.
- `Company`: Entity managing organization details (GST, industry, logo, address, employees, departments).
- `Contact`: Entity managing multiple contacts, phones, emails, websites, addresses, social profiles, and custom fields per lead.
- `LeadMetadata`: Lineage entity storing `original_image_url`, `ocr_raw_output`, `ai_understanding_output`, `dom_entity_snapshot`, `review_session_id`, and `google_sync_job_id`.
- `LeadTimeline`: Immutable audit logging for all lifecycle events (`Created`, `Updated`, `Scanned`, `Reviewed`, `Synced`, `Edited`, `Merged`, `Archived`, `Restored`).

---

## REST API Endpoints (`/api/v1/leads`)
- `GET /api/v1/leads`: Multi-field search and list active leads.
- `POST /api/v1/leads`: Ingest new lead from Review Workspace.
- `GET /api/v1/leads/{id}`: Fetch single lead details with lineage metadata.
- `PATCH /api/v1/leads/{id}`: Update lead attributes.
- `POST /api/v1/leads/{id}/archive`: Soft archive a lead.
- `POST /api/v1/leads/{id}/restore`: Restore an archived lead.
- `POST /api/v1/leads/merge`: Merge duplicate leads into a primary record.
- `GET /api/v1/leads/{id}/timeline`: Retrieve immutable audit log timeline.
