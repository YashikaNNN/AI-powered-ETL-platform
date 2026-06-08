from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, etl, health
from app.config import settings
from app.db.session import init_db
from app.utils.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await init_db()
    yield


app = FastAPI(
    title="AI ETL Analytics API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(etl.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
