from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    APP_NAME: str = "HRMS Lite API"

    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,https://darshilhrms.netlify.app"

    # Database - use DATABASE_URL or build from parts
    DATABASE_URL: str = "postgresql://hrms:hrms_secret@localhost:5432/hrms_lite"

    @property
    def async_database_url(self) -> str:
        """For async SQLAlchemy if needed later."""
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.DATABASE_URL


settings = Settings()
