# Enterprise Universal Search Engine (BF-014) Documentation

## Overview
The Enterprise Universal Search Engine provides unified global search across the entire LeadScan AI platform—indexing Lead Records, Contacts, Companies, Timelines, Notes, Tags, OCR Raw Text, AI Understanding Outputs, Document Object Models (DOM), Review Workspace histories, and Google Sheets Sync logs (**BF-001 through BF-013**).

---

## Architectural Components
- `indexer.py`: Incremental and background search index pipeline for platform entities.
- `query_parser.py`: Query parsing supporting Boolean operators (`AND`, `OR`, `NOT`), field specifiers (`gst:27AAAAA`, `company:Acme`), exact phrase matching (`"Global Logistics"`), and prefix matching.
- `ranking.py`: Multi-field relevance scoring engine combining exact match boosts, field weighting (Title/Company $3.0\times$, Email/Phone/GST $2.5\times$), and recency decay.
- `filters.py`: Multidimensional filtering for date ranges, status, tags, companies, and source types.

---

## REST API Endpoints (`/api/v1/search`)
- `POST /api/v1/search/universal`: Execute global multi-field search query.
- `GET /api/v1/search/suggestions`: Instant autocomplete suggestions for search bar.
- `POST /api/v1/search/saved-searches`: Bookmark search queries and filter configurations.
- `GET /api/v1/search/saved-searches`: Retrieve saved searches list.
- `GET /api/v1/search/recent`: Fetch recent search query history.
