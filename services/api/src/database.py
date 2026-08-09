from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from leadscan_config import AppSettings

settings = AppSettings()

db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+asyncpg://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

try:
    # Create asynchronous engine for PostgreSQL 18
    async_engine = create_async_engine(
        db_url,
        echo=settings.DEBUG,
        future=True,
        pool_size=20,
        max_overflow=10,
    )

    # Async session maker
    async_session_maker = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
except Exception:
    async_engine = None
    async_session_maker = None


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for retrieving async database session."""
    if async_session_maker is None:
        raise RuntimeError("Database engine not initialized")
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            import logging
            logging.getLogger("leadscan-database").exception("DATABASE TRANSACTION COMMIT FAILED: %s", exc)
            from fastapi import HTTPException
            raise HTTPException(
                status_code=500,
                detail=f"DB_COMMIT_DIAGNOSTIC: {type(exc).__module__}.{type(exc).__name__}: {str(exc)}"
            ) from exc
        finally:
            await session.close()
