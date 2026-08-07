# LeadScan AI Backup & Recovery Guide

Guidelines for PostgreSQL database backups and restoral procedures.

---

## 1. Objectives (RPO & RTO)
- **Recovery Point Objective (RPO)**: Maximum 1 hour of data loss. Daily snapshots + hourly WAL archiving.
- **Recovery Time Objective (RTO)**: Under 30 minutes to restore service.

## 2. PostgreSQL Backup Procedures
- Run regular database dumps:
  ```bash
  pg_dump -h <host> -U <user> -F c -b -v -f "/backups/leadscan_db_$(date +%F).dump" leadscan_db
  ```

## 3. Recovery Procedures
1. Terminate active database connections.
2. Drop and recreate target database:
   ```sql
   DROP DATABASE leadscan_db;
   CREATE DATABASE leadscan_db;
   ```
3. Restore using pg_restore:
   ```bash
   pg_restore -h <host> -U <user> -d leadscan_db -v "/backups/leadscan_db_<date>.dump"
   ```
