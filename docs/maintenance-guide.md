# LeadScan AI Platform Maintenance Guide

Standard procedures for ongoing systems maintenance and tasks cleanup.

---

## 1. Database Maintenance
- **VACUUM & ANALYZE**: Runs weekly to update query planner stats and reclaim space:
  ```sql
  VACUUM ANALYZE;
  ```
- **Index Rebuilds**: Run monthly to prevent index bloating:
  ```sql
  REINDEX DATABASE leadscan_db;
  ```

## 2. Periodic Cleanup Jobs
- **Celery Beat cleanups**:
  - `clean_old_notifications`: Purges notification log entries older than 30 days.
  - `purge_dlq_tasks`: Removes resolved DLQ message dumps older than 7 days.
  - `perform_storage_quota_realignments`: Recalculates storage folder sizes to align metadata usage quotas.
