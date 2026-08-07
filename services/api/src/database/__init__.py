from collections.abc import AsyncGenerator

from leadscan_config import AppSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

settings = AppSettings()

try:
    # Create asynchronous engine for PostgreSQL 18
    async_engine = create_async_engine(
        settings.DATABASE_URL,
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
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
