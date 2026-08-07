# Enterprise Digital Asset Management (DAM) Engine (BF-015) Documentation

## Overview
The Enterprise Digital Asset Management (DAM) Engine serves as the **single source of truth** for all binary assets across LeadScan AI—including Original Scan Images, Company Logos, Thumbnails, Preview Cache Images, OCR Overlays, and future document attachments.

---

## Key Principles & Features
- **Immutable Lossless Preservation**: Original Scan Images are saved losslessly and marked as immutable. Modification or overwrite attempts raise an `ImmutableAssetModificationException`.
- **Derivative Thumbnails & Previews**: Derivative small, medium, and web preview images are generated without altering the original binary payload.
- **SHA-256 Checksum Integrity**: Checks file hashes against expected values to detect missing or corrupted assets.
- **Company Default Logo Rule**: If a company lacks a custom uploaded logo asset, the DAM automatically assigns and serves the default system fallback logo.

---

## REST API Endpoints (`/api/v1/assets`)
- `POST /api/v1/assets/upload`: Upload raw file payload with metadata & derivative generation.
- `GET /api/v1/assets`: List digital assets.
- `GET /api/v1/assets/{id}`: Fetch single asset metadata, versions, and integrity status.
- `POST /api/v1/assets/{id}/verify-integrity`: Perform SHA256 file checksum verification.
- `POST /api/v1/assets/{id}/rollback`: Rollback non-immutable asset version.
- `GET /api/v1/assets/company-logo/{company_id}`: Fetch company logo with automatic system default fallback.
