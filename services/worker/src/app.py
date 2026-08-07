# ruff: noqa: B008
from typing import Any

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel, Field

from services.worker.src.dependencies import get_worker_health_check
from services.worker.src.health import WorkerHealthCheck

app = FastAPI(title="LeadScan Background Worker Control API")


class HeartbeatRequest(BaseModel):
    node_id: str = Field(..., min_length=1, max_length=100)


# ----------------------------------------------------
# Worker Diagnostics Endpoints
# ----------------------------------------------------


@app.get("/health", status_code=status.HTTP_200_OK)
async def get_worker_health(
    health_check: type[WorkerHealthCheck] = Depends(get_worker_health_check),
) -> dict[str, Any]:
    """Retrieve Celery worker node health status."""
    node_status = await health_check.inspect_worker_nodes()
    return {
        "service": "LeadScan Worker Ingress",
        "health": node_status.get("status", "UNHEALTHY"),
        "active_nodes": node_status.get("active_nodes", {}),
        "heartbeats": health_check.get_heartbeats(),
    }


@app.get("/queues", status_code=status.HTTP_200_OK)
async def get_queues_status(
    health_check: type[WorkerHealthCheck] = Depends(get_worker_health_check),
) -> dict[str, Any]:
    """Retrieve message count lengths across all queues."""
    sizes = await health_check.get_queue_sizes()
    return {
        "queues": sizes,
    }


@app.post("/heartbeat", status_code=status.HTTP_204_NO_CONTENT)
async def register_node_heartbeat(
    data: HeartbeatRequest,
    health_check: type[WorkerHealthCheck] = Depends(get_worker_health_check),
) -> None:
    """Register a heartbeat timestamp checkpoint for a worker node."""
    health_check.register_heartbeat(data.node_id)
