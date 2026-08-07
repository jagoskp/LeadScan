# LeadScan AI Platform Limitations

Known capacity constraints and architectural bounds of the current version.

---

## 1. Database Connections Constraints
- The maximum pool size configuration of 50 connections allows up to 50 concurrent transactions per API gateway replica. Exceeding this triggers connection timeouts.

## 2. In-Memory Metrics Registry
- Metrics collected in `AppMetrics` are stored in-memory.
- In multi-replica deployments, each container reports its own individual counters.
- True aggregated metrics tracking requires configuring Prometheus target collectors to scrape individual replica IP endpoints.

## 3. Storage Quota Recalculations
- Folder quota realignments are calculated via periodic batch jobs instead of real-time transactional locks, creating brief updates delays on storage quotas.
