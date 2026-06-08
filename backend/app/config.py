from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    database_url: str = (
        "postgresql+asyncpg://etl_user:change_me@localhost:5432/etl_analytics"
    )
    cors_origins: list[str] = ["http://localhost:3000"]
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    @property
    def database_url_sync(self) -> str:
        return self.database_url.replace("+asyncpg", "")


settings = Settings()
