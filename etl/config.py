from pydantic_settings import BaseSettings, SettingsConfigDict


class ETLSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    etl_batch_size: int = 1000
    etl_log_level: str = "INFO"


settings = ETLSettings()
