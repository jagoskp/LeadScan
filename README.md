# LeadScan AI Monorepo

Welcome to the enterprise monorepo for **LeadScan AI**, an enterprise SaaS platform for intelligent lead capture, extraction, and verification.

This repository is structured as a unified workspace containing multiple frontend applications, backend microservices, shared packages, and Infrastructure-as-Code definitions.

## Project Structure

```
LeadScan AI Monorepo
├── .github/             # GitHub templates and workflows
├── apps/                # Client applications (Web, Mobile, Admin)
├── docs/                # Product, design, and architecture documentation
├── infrastructure/      # Orchestration, container, and script templates
├── packages/            # Reusable libraries, config schemas, SDKs, and UIs
├── services/            # Backend API and engine microservices
├── tests/               # Global test suites (integration, E2E)
└── tools/               # Local developer utilities and scripting
```

## Technology Stack

- **Frontend:** React 19, Next.js 16, TypeScript, Tailwind CSS 4, shadcn/ui
- **Backend:** Python 3.14, FastAPI, SQLAlchemy 2, Alembic, Pydantic v2
- **Database / Cache:** PostgreSQL 18, Redis
- **Workflow Orchestration:** Temporal
- **OCR:** PaddleOCR, Tesseract (Fallback)
- **Storage:** S3 Compatible Storage
- **Mobile:** Flutter

## Getting Started

### Prerequisites

- Node.js (v20+ recommended)
- PNPM (v9+ recommended)
- Python (v3.14 recommended)
- Flutter SDK (v3+ recommended)
- Docker & Docker Compose

### Initial Setup

1. Clone the repository and navigate to the project root.
2. Install Javascript dependencies:
   ```bash
   pnpm install
   ```
3. Copy environment template and fill in local configurations:
   ```bash
   cp .env.example .env
   ```
4. Set up python virtual environment and verify dependencies (see service-specific READMEs).

## Coding Standards and Quality

This repository uses automated code quality tools to maintain high standard code consistency:

- **Python:** Managed with `Ruff` (linting/formatting) and `MyPy` (typing). Run:
  ```bash
  ruff check .
  mypy .
  ```
- **JavaScript / TypeScript:** Checked with `ESLint` and formatted with `Prettier`. Run:
  ```bash
  pnpm lint
  pnpm format:check
  ```

For detailed guides on contributing, please read [CONTRIBUTING.md](file:///e:/Antigravity/CONTRIBUTING.md).
