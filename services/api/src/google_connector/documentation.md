# Google Sheets Production Connector (Enterprise Edition) Documentation

## Overview
The Google Sheets Production Connector enables real-time and batch synchronization of extracted, approved Document Object Model (DOM) entities from **BF-008 Review Workspace** to Google Sheets using dynamic column mapping (**BF-006 / BF-007**), credentials in **BF-011 Secret Vault**, and job tracking in **BF-009 Universal Sync Engine**.

---

## Key Modules Architecture
- `oauth.py`: Google OAuth2 authorization code flow with automatic token refresh.
- `sheets.py`: Low-level Google Sheets REST API v4 wrapper with exponential backoff & rate limit handling.
- `column_discovery.py`: Dynamic header discovery engine detecting renames, duplicates, and new columns.
- `remapping_assistant.py`: Intelligent auto-remapping assistant with Levenshtein string matching & synonym dictionaries.
- `mapping_validator.py`: Pre-sync schema validator enforcing mapping profile compliance.
- `sync.py`: Synchronization engine executing Append, Update, Upsert, and Batch operations.
- `repository.py`: Persistence layer for accounts, spreadsheets, worksheets, columns, jobs, and history.

---

## Operational Workflows

### 1. OAuth Authentication
1. Redirect user to Google Authorization endpoint.
2. Receive OAuth code via callback.
3. Exchange code for access & refresh tokens.
4. Encrypt and store tokens safely in Secret Vault.

### 2. Pre-Sync Check & Dynamic Mapping
1. Fetch live headers from target worksheet.
2. Compare against active mapping profile.
3. If columns match, grant sync authorization.
4. If missing/renamed columns detected, generate auto-remapping suggestions for user confirmation.

### 3. Sync Execution
1. Transform approved DOM rows into header-ordered array.
2. Post payload using Google Sheets API `append` or `update`.
3. Log duration, row count, and validation outcome in `GoogleSyncHistory`.

### 4. Exponential Backoff & Retry Strategy
On HTTP 429 (Rate Limit) or HTTP 503 (Service Unavailable), delay retries using:
$$\text{Delay} = \text{Base} \times 2^{(\text{attempt} - 1)}$$
Up to maximum retry limit (default: 3 attempts).
