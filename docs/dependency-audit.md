# LeadScan AI Dependency Audit

This document verifies the package requirements, version locks, and vulnerability scanner reports.

---

## 1. Locked Package Dependencies
- **Python**: Version 3.12+ (target: Python 3.14).
- **FastAPI**: Main web framework.
- **SQLAlchemy 2.0 / Alembic**: Core async database toolkit.
- **Pydantic / Pydantic Settings v2**: Input validation and config loading.
- **Celery / Redis**: Async worker queue broker.

## 2. Vulnerability Management
- **GitHub Action Workflow**: `security.yml` runs `Bandit` on pushes and pull requests to scan python code for security issues.
- **Safety**: Analyzes installed packages against known vulnerability databases.
