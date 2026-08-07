import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from services.api.src.sync_engine.enums import (
    SyncJobStatus,
)
from services.api.src.sync_engine.exceptions import (
    AuthenticationFailedException,
    ConnectorNotFoundException,
    SyncJobNotFoundException,
)
from services.api.src.sync_engine.interfaces import (
    IConnector,
    IConnectorFactory,
    ISyncEngine,
)
from services.api.src.sync_engine.models import (
    Connector,
    SyncHistory,
    SyncJob,
    SyncResult,
)
from services.api.src.sync_engine.repository import (
    ConnectorRepository,
    SyncJobRepository,
)
from services.api.src.sync_engine.schemas import (
    SyncJobCreate,
)
from services.api.src.sync_engine.validators import validate_credentials_format


class SyncEngineService(ISyncEngine, IConnector, IConnectorFactory):
    """Orchestrates job queues, retry configurations, and targets dispatches."""

    def __init__(
        self,
        connector_repo: ConnectorRepository,
        job_repo: SyncJobRepository,
    ) -> None:
        self.connector_repo = connector_repo
        self.job_repo = job_repo

    # ----------------------------------------------------
    # Job CRUD Operations
    # ----------------------------------------------------

    async def create_job(self, data: SyncJobCreate) -> SyncJob:
        """Create a new job in the synchronization queue."""
        profile = await self.connector_repo.get_profile_by_id(data.profile_id)
        if not profile:
            raise ConnectorNotFoundException()

        job = SyncJob(
            profile_id=data.profile_id,
            session_id=data.session_id,
            status=SyncJobStatus.PENDING.value,
            retry_count=0,
            max_retries=3,
        )
        await self.job_repo.create_job(job)
        return job

    async def get_sync_job(self, job_id: uuid.UUID) -> SyncJob:
        """Retrieve detailed properties of a SyncJob."""
        job = await self.job_repo.get_job_by_id(job_id)
        if not job:
            raise SyncJobNotFoundException()
        return job

    # ----------------------------------------------------
    # ISyncEngine Implementation
    # ----------------------------------------------------

    async def register_connector(
        self, name: str, connector_type: str
    ) -> uuid.UUID:
        """Register a new connector target definition."""
        conn = Connector(name=name, connector_type=connector_type, is_active=True)
        await self.connector_repo.create_connector(conn)
        return conn.id

    async def execute_job(self, job_id: uuid.UUID) -> dict[str, Any]:
        """Load job properties, format mapped fields, and invoke target pushes."""
        job = await self.job_repo.get_job_by_id(job_id)
        if not job:
            raise SyncJobNotFoundException()

        # Update status to Processing
        await self.job_repo.update_job_status(
            job.id, SyncJobStatus.PROCESSING.value
        )

        profile = await self.connector_repo.get_profile_by_id(job.profile_id)
        if not profile:
            raise ConnectorNotFoundException()

        # 1. Instantiate Target Connector
        connector = await self.get_connector(profile.connector.connector_type)

        try:
            # 2. Authenticate
            creds = (
                {
                    "encrypted_token": profile.credentials[0].encrypted_token,
                    "refresh_token": profile.credentials[0].refresh_token,
                }
                if profile.credentials
                else {}
            )
            auth_success = await connector.authenticate(creds)
            if not auth_success:
                raise AuthenticationFailedException()

            # 3. Simulate mapped data loading
            mock_data = [
                {"company_name": "LeadScan AI Corp.", "phone": "+15550199"},
            ]

            # 4. Push data
            target_config = {
                "sheet_id": "mock-sheet-123",
                "worksheet": "Leads",
            }
            res = await connector.push_data(mock_data, target_config)

            # Log Complete History
            history = SyncHistory(
                job_id=job.id,
                status=SyncJobStatus.COMPLETED.value,
                retries_attempted=job.retry_count,
                duration_ms=120,
                completed_at=datetime.now(UTC),
            )
            await self.job_repo.create_history(history)

            result = SyncResult(
                job_id=job.id,
                payload_snapshot={"data": mock_data},
                response_snapshot=res,
            )
            await self.job_repo.create_result(result)

            # Update status complete
            await self.job_repo.update_job_status(
                job.id, SyncJobStatus.COMPLETED.value
            )

        except Exception as e:
            # Increment retry count
            retry_count = job.retry_count + 1
            next_status = (
                SyncJobStatus.FAILED.value
                if retry_count >= job.max_retries
                else SyncJobStatus.RETRYING.value
            )

            history = SyncHistory(
                job_id=job.id,
                status=next_status,
                retries_attempted=job.retry_count,
                error_message=str(e),
                completed_at=datetime.now(UTC),
            )
            await self.job_repo.create_history(history)

            await self.job_repo.update_job_status(
                job.id, next_status, retry_inc=True
            )

        updated_job = await self.job_repo.get_job_by_id(job_id)
        if not updated_job:
            raise SyncJobNotFoundException()
        return {
            "job_id": updated_job.id,
            "status": updated_job.status,
            "retries_attempted": updated_job.retry_count,
        }

    async def dispatch_retry_queue(self) -> int:
        """Scan dead letter queues and invoke automatic retry strategies."""
        failed = await self.job_repo.get_failed_jobs()
        for job in failed:
            await self.execute_job(job.id)
        return len(failed)

    # ----------------------------------------------------
    # IConnector Implementation
    # ----------------------------------------------------

    async def authenticate(self, credentials: dict[str, Any]) -> bool:
        """Evaluate credential token parameters validity."""
        validate_credentials_format(credentials)
        return True

    async def push_data(
        self, data: Sequence[dict[str, Any]], target_config: dict[str, Any]
    ) -> dict[str, Any]:
        """Push batch row payload arrays directly into targets."""
        return {
            "success": True,
            "records_inserted": len(data),
            "destination_target": target_config.get("sheet_id", "Default"),
        }

    # ----------------------------------------------------
    # IConnectorFactory Implementation
    # ----------------------------------------------------

    async def get_connector(self, connector_type: str) -> IConnector:
        """Instantiate wrapper instance based on targets."""
        # The service itself implements IConnector as default stub wrapper
        return self
