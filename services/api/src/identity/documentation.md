# Enterprise Identity Resolution & Smart Duplicate Engine (BF-016) Documentation

## Overview
The Enterprise Identity Resolution Engine detects, scores, classifies, and safely merges duplicate people, companies, and organization records across LeadScan AI (**BF-001 through BF-015**).

---

## Key Principles & Core Rules
- **No Permanent Deletion**: Secondary duplicate records are soft-archived (`is_archived=True`) and linked via `MergeHistory`.
- **100% Lossless Rollback**: Pre-merge state snapshots are preserved in `RollbackHistory`, enabling full restoration at any time.
- **Multi-Dimensional Matching & Scoring**:
  - Exact Identifier Match (GST, Phone, Email) $\rightarrow$ $100\%$ Confidence Level.
  - Fuzzy Levenshtein Match $\rightarrow$ Duplicate Score & Similarity Score.
- **Configurable Conflict Resolution**: Policy selection (`keep_original`, `keep_latest`, `keep_highest_confidence`, `manual`).

---

## REST API Endpoints (`/api/v1/identity`)
- `GET /api/v1/identity/duplicates`: List pending duplicate match pairs.
- `POST /api/v1/identity/scan`: Trigger repository duplicate scan.
- `GET /api/v1/identity/merge-preview`: Preview field conflicts and differences.
- `POST /api/v1/identity/merge`: Execute safe merge with snapshot generation.
- `POST /api/v1/identity/rollback/{id}`: Rollback a previous merge and restore secondary lead.
