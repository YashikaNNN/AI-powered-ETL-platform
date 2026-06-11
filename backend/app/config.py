from typing import Annotated, Self

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

DEV_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    database_url: str = (
        "postgresql+asyncpg://etl_user:change_me@localhost:5432/etl_analytics"
    )
    cors_origins: Annotated[list[str], NoDecode] = DEV_CORS_ORIGINS.copy()
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    openrouter_api_key: str = ""

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        """Ensure async SQLAlchemy gets asyncpg; accept Render/Heroku postgres:// URLs."""
        url = value.strip()
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        if url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @model_validator(mode="after")
    def ensure_dev_cors_origins(self) -> Self:
        if self.app_env == "development":
            self.cors_origins = list(
                dict.fromkeys([*self.cors_origins, *DEV_CORS_ORIGINS])
            )
        return self

    @property
    def database_url_sync(self) -> str:
        """Sync URL for ETL/psycopg2 (strip asyncpg driver suffix)."""
        return self.database_url.replace("postgresql+asyncpg://", "postgresql://")

    @property
    def database_requires_ssl(self) -> bool:
        return "localhost" not in self.database_url and "127.0.0.1" not in self.database_url


settings = Settings()
