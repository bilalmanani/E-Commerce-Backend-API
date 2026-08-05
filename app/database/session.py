from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# 1. Create the SQLAlchemy Async Engine
# The engine manages the pool of connections to the PostgreSQL database.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log generated SQL queries in debug mode
    future=True,
    pool_size=10,         # Maximum number of permanent connections in pool
    max_overflow=20,      # Additional burst connections allowed beyond pool_size
    pool_pre_ping=True    # Health check connections before returning from pool
)

# 2. Create the Async Session Maker Factory
# This factory produces new AsyncSession instances for each HTTP request.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit (prevents extra lazy-loading queries)
    autoflush=False,         # Disable automatic flush to control when data hits DB
    autocommit=False
)

# 3. Database Dependency Generator (yields DB session per request)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an AsyncSession per request.
    Automatically closes the session after the request finishes.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
