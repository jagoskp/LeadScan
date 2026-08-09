import logging
import time
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from leadscan_config import AppSettings

from services.api.src.ai.router import router as ai_router
from services.api.src.audit.router import router as audit_router
from services.api.src.auth.router import router as auth_router
from services.api.src.database import Base, async_engine
from services.api.src.documents.router import router as documents_router
from services.api.src.integration.router import router as integration_router
from services.api.src.monitoring.logging import (
    correlation_id_ctx,
    request_id_ctx,
    setup_json_logging,
    trace_id_ctx,
)
from services.api.src.monitoring.metrics import AppMetrics
from services.api.src.monitoring.router import router as monitoring_router
from services.api.src.notifications.router import router as notifications_router
from services.api.src.ocr.router import router as ocr_router
from services.api.src.organization.router import router as org_router
from services.api.src.reports.router import (
    jobs_router as report_jobs_router,
)
from services.api.src.reports.router import (
    reports_router,
)
from services.api.src.ai_understanding.router import router as ai_understanding_router
from services.api.src.camera.router import router as camera_router
from services.api.src.document_model.router import router as doc_model_router
from services.api.src.mapping.router import router as mapping_router
from services.api.src.mapping_studio.router import router as mapping_studio_router
from services.api.src.ocr_engine.router import router as ocr_engine_router
from services.api.src.review_workspace.router import router as review_workspace_router
from services.api.src.scanner.router import router as scanner_router
from services.api.src.sync_engine.router import router as sync_engine_router
from services.api.src.connectors.router import router as connectors_studio_router
from services.api.src.secret_vault.router import router as secret_vault_router
from services.api.src.google_connector.router import router as google_connector_router
from services.api.src.leads.router import router as leads_router
from services.api.src.assets.router import router as assets_router
from services.api.src.identity.router import router as identity_router
from services.api.src.search.router import router as search_router
from services.api.src.storage.router import router as storage_router
from services.api.src.workflow.router import (
    executions_router,
    templates_router,
    router as workflow_router,
)
from services.api.src.users.router import router as users_router
from services.api.src.dashboard.router import router as dashboard_router
from services.api.src.workspaces.router import router as workspaces_router
from services.api.src.release.router import router as release_router

settings = AppSettings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Initialize structured JSON logging
    setup_json_logging("DEBUG" if settings.DEBUG else "INFO")
    # Initial tables setup for development (Alembic will manage production migrations)
    if async_engine is not None:
        try:
            import_models()
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as exc:
            logger.warning(f"[DB INIT] Table creation notice: {exc}")

        try:
            from sqlalchemy import text
            async with async_engine.begin() as conn:
                logger.info("[DB MIGRATION] Executing DDL: ALTER TABLE refresh_tokens ALTER COLUMN token TYPE VARCHAR(512);")
                await conn.execute(text("ALTER TABLE refresh_tokens ALTER COLUMN token TYPE VARCHAR(512);"))
                logger.info("[DB MIGRATION] Migration successfully executed: refresh_tokens.token -> VARCHAR(512)")
        except Exception as alter_exc:
            logger.error(f"[DB MIGRATION ERROR] DDL execution failed: {alter_exc}", exc_info=True)
    from services.api.src.integration.service import register_mock_defaults
    register_mock_defaults()
    yield
    # Dispose of engine connection pools on shutdown
    if async_engine is not None:
        try:
            await async_engine.dispose()
        except Exception:
            pass



app = FastAPI(
    title="LeadScan AI API Gateway",
    description="Core backend API gateway service for LeadScan AI platform.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": "LeadScan AI API Gateway",
        "status": "online",
        "docs": "/docs",
        "health": "/health/live",
    }


# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production based on settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("api_gateway")


@app.middleware("http")
async def structured_logging_middleware(request: Any, call_next: Any) -> Any:
    corr_id = request.headers.get("X-Correlation-ID", uuid.uuid4().hex)
    req_id = uuid.uuid4().hex
    tr_id = uuid.uuid4().hex

    correlation_id_ctx.set(corr_id)
    request_id_ctx.set(req_id)
    trace_id_ctx.set(tr_id)

    start_time = time.perf_counter()
    logger.info(f"Incoming request: {request.method} {request.url.path}")

    try:
        response = await call_next(request)
    except Exception as exc:
        duration = (time.perf_counter() - start_time) * 1000.0
        AppMetrics.record_request(duration)
        logger.error(f"Request failed: {exc}", exc_info=True)
        raise

    duration = (time.perf_counter() - start_time) * 1000.0
    AppMetrics.record_request(duration)

    response.headers["X-Request-ID"] = req_id
    response.headers["X-Correlation-ID"] = corr_id

    logger.info(
        f"Completed request: {request.method} {request.url.path} "
        f"- Status: {response.status_code} - Latency: {duration:.2f}ms"
    )

    return response

from services.api.src.tracking.router import router as tracking_router

# Register routers
app.include_router(auth_router)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router)
app.include_router(users_router, prefix="/api/v1")
app.include_router(org_router)
app.include_router(documents_router)
app.include_router(ocr_router)
app.include_router(ai_router)
app.include_router(templates_router)
app.include_router(executions_router)
app.include_router(search_router)
app.include_router(report_jobs_router)
app.include_router(reports_router)
app.include_router(notifications_router)
app.include_router(audit_router)
app.include_router(storage_router)
app.include_router(scanner_router)
app.include_router(camera_router)
app.include_router(ocr_engine_router)
app.include_router(ai_understanding_router)
app.include_router(doc_model_router)
app.include_router(mapping_router)
app.include_router(mapping_studio_router)
app.include_router(review_workspace_router)
app.include_router(sync_engine_router)
app.include_router(connectors_studio_router)
app.include_router(secret_vault_router)
app.include_router(google_connector_router)
app.include_router(leads_router)
app.include_router(assets_router)
app.include_router(identity_router)
app.include_router(workflow_router)
app.include_router(dashboard_router)
app.include_router(workspaces_router)
app.include_router(release_router)
app.include_router(integration_router)
app.include_router(monitoring_router)
app.include_router(tracking_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("services.api.main:app", host="0.0.0.0", port=8000, reload=True)



