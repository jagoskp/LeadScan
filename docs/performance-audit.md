# LeadScan AI Performance Audit

This document evaluates the scalability parameters of database connections, workers concurrency, and cluster scaling thresholds.

---

## 1. Database Connection Tuning
- **SQLAlchemy Async Pools**: Tuned to prevent connection exhaustion.
- **Settings**:
  - `DB_POOL_SIZE`: Defaults to 20 connections in development, and 50 in production.
  - `DB_MAX_OVERFLOW`: Defaults to 10 connections in development, and 20 in production.

## 2. Worker Concurrency Segregation
- **Queue Segregation**: Worker container instances run with queue parameter scopes.
- **OCR/AI Nodes**: Deployed on dedicated pods (using `ocr.Dockerfile`) to handle heavy image processing without resource-starving api processes.

## 3. Horizontal Pod Autoscaling (HPA)
- **HPA Thresholds**: Programmed to trigger pod scaling when average CPU utilization exceeds 75%.
- **Scale Rules**: Min replicas set to 3, max replicas set to 10.
