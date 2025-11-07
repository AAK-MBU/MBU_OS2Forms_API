"""Application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application settings
    APP_NAME: str = "MBU OS2Forms API"
    APP_VERSION: str = Field(default="0.0.1")
    APP_DESCRIPTION: str = "API for process dashboard and monitoring"
    DEBUG: bool = Field(default=False)

    # API settings
    API_V1_PREFIX: str = "/api/v1"

    # Database settings - Full connection string
    DATABASE_URL: str | None = Field(default=None, description="Full database connection URL")

    # Database settings - Individual components
    DATABASE_HOST: str = Field(default="localhost")
    DATABASE_PORT: int = Field(default=1433)
    DATABASE_NAME: str = Field(default="something_db_here")
    DATABASE_USER: str = Field(default="sa")
    DATABASE_PASSWORD: str = Field(default="YourStrong@Passw0rd")

    # CORS settings
    CORS_ORIGINS: list[str] = Field(default=["http://localhost:3000", "http://localhost:8080"])

    # Token Authentication
    API_TOKEN: str = Field(
        default="your-secret-token-change-in-production",
        description="Static API token for authentication",
    )


# Global settings instance
settings = Settings()
