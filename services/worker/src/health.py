from datetime import UTC, datetime
from typing import Any

from services.worker.src.celery_app import celery_app


class WorkerHealthCheck:
    """Manages worker health checks, queue diagnostics, and heartbeats."""

    _heartbeats: dict[str, datetime] = {}

    @classmethod
    def register_heartbeat(cls, node_id: str) -> None:
        """Record a heartbeat timestamp checkpoint for a worker node."""
        cls._heartbeats[node_id] = datetime.now(UTC)

    @classmethod
    def get_heartbeats(cls) -> dict[str, str]:
        """Fetch recorded heartbeats formatted as ISO strings."""
        return {node: ts.isoformat() for node, ts in cls._heartbeats.items()}

    @classmethod
    async def inspect_worker_nodes(cls) -> dict[str, Any]:
        """Ping active Celery worker nodes and retrieve their status."""
        try:
            inspector = celery_app.control.inspect()
            pings = inspector.ping()
            if pings is None:
                return {"status": "UNHEALTHY", "active_nodes": {}}
            return {"status": "HEALTHY", "active_nodes": pings}
        except Exception as exc:
            return {"status": "UNHEALTHY", "error": str(exc)}

    @classmethod
    async def get_queue_sizes(cls) -> dict[str, int]:
        """Pings Redis to query lengths of configured queues."""
        try:
            import redis

            broker_url = celery_app.conf.broker_url
            if not broker_url or not broker_url.startswith("redis"):
                return {}

            client: redis.Redis = redis.from_url(broker_url)
            sizes = {}
            for queue_name in [
                "default",
                "ocr",
                "ai",
                "search",
                "report",
                "notification",
                "workflow",
                "maintenance",
                "dlq",
            ]:
                # LLEN queries the length of the list in Redis
                sizes[queue_name] = client.llen(queue_name)
            return sizes
        except Exception:
            # Fallback to zero if redis client isn't available
            return {}
