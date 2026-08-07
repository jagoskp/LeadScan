# LeadScan AI Disaster Recovery Plan

Procedures for recovering from regional infrastructure outages.

---

## 1. Outage Detection
- Global DNS health pings check `/health/live` endpoints every 10 seconds.
- Primary region is declared down if health checks fail consecutively for 30 seconds.

## 2. Multi-Region Failover Steps
1. **Redirect Traffic**: Update DNS routing records (e.g. Cloudflare, Route53) to direct incoming API requests to the secondary standby region.
2. **Promote Standby Database**: Promote read-replica PostgreSQL database in the standby region to primary.
   ```bash
   pg_ctl promote -D /var/lib/postgresql/data
   ```
3. **Verify Ingress**: Test the standby API gateway using `bash scripts/healthcheck.sh` to ensure it resolves requests correctly.
