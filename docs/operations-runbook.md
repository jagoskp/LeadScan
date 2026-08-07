# LeadScan AI Operations Runbook

Playbook guidelines for managing production runtime incidents.

---

## 1. High CPU or Memory Utilization
### Symptoms
- Pod crashes, API latency spikes, or HPA triggers pod scaling to maximum replicas (10 pods).
### Resolution Actions
1. Identify the heavy pods:
   ```bash
   kubectl top pods -n leadscan
   ```
2. Inspect application logs:
   ```bash
   kubectl logs <pod-name> -n leadscan
   ```
3. Verify database locks or slow queries in postgres log traces.

## 2. Celery Worker Queue Backlog
### Symptoms
- OCR and AI analysis tasks remain in pending status.
### Resolution Actions
1. Query queue lengths via `/health/queues` or redis CLI:
   ```bash
   redis-cli -u $REDIS_URL LLEN ocr
   ```
2. Scale up Celery worker replicas:
   ```bash
   kubectl scale deployment/leadscan-worker --replicas=5 -n leadscan
   ```
3. Check for failed messages in the Dead Letter Queue (DLQ).
