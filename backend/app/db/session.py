import logging
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.db.base import Base
from app.models import PipelineRun, SampleEvent  # noqa: F401 — register models

logger = logging.getLogger(__name__)

# Render internal Postgres does not need forced SSL; Neon/external clouds do.
_connect_args: dict = {}
if "sslmode=require" in settings.database_url or "neon.tech" in settings.database_url:
    _connect_args["ssl"] = "require"

engine = create_async_engine(
    settings.database_url,
    echo=settings.app_env == "development",
    connect_args=_connect_args,
)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """Create schemas and tables if they do not exist (safe for Render deploys)."""
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS analytics"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS etl_metadata"))
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database schemas and tables are ready")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
