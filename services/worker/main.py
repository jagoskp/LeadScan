import asyncio
import logging
from temporalio.client import Client
from leadscan_config import AppSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("leadscan-worker")
settings = AppSettings()


async def main() -> None:
    logger.info("Initializing LeadScan Temporal Worker...")
    try:
        # Establish connection to Temporal cluster
        # client = await Client.connect(settings.TEMPORAL_HOST_PORT, namespace=settings.TEMPORAL_NAMESPACE)
        # logger.info("Connected to Temporal Namespace: %s", settings.TEMPORAL_NAMESPACE)

        logger.info("Worker started successfully. Standing by for events...")
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        logger.info("Worker shutting down...")
    except Exception as e:
        logger.error("Failed to execute worker loop: %s", e)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker stopped by keyboard interrupt.")
