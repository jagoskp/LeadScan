"""Enterprise Release Candidate (RC-1) Production Certification module."""

from services.api.src.release.router import router as release_router

__all__ = ["release_router"]
