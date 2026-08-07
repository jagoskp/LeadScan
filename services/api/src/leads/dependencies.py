from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.leads.service import LeadService


def get_lead_service(db: AsyncSession = Depends(get_db)) -> LeadService:
    """Dependency provider for LeadService instance."""
    return LeadService(db)
