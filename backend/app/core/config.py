"""Configuration settings for the VibeStack backend application.

This module uses Pydantic Settings to manage environment variables
and provide type-safe configuration throughout the application.
"""

import os
from typing import List, Optional

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "VibeStack API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = (
        "postgresql+asyncpg://vibestack:vibestack@localhost:5432/vibestack"
    )

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"

    # JWT Configuration
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Optional: SQLCipher (for encrypted SQLite)
    SQLCIPHER_KEY: Optional[str] = None

    # Optional: External Services
    REDIS_URL: Optional[str] = None
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # Production Database (optional)
    POSTGRES_DB: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None

    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validate environment setting."""
        allowed = ["development", "staging", "production", "testing"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v

    @validator("DEBUG")
    def validate_debug(cls, v, values):
        """Ensure DEBUG is False in production."""
        if values.get("ENVIRONMENT") == "production" and v:
            return False
        return v

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v, values):
        """Warn about weak secret keys in production."""
        if (
            values.get("ENVIRONMENT") == "production"
            and v == "your-super-secret-key-change-this-in-production"
        ):
            raise ValueError("SECRET_KEY must be changed in production")
        return v

    @validator("ALLOWED_HOSTS", pre=True)
    def validate_allowed_hosts(cls, v):
        """Parse ALLOWED_HOSTS from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    class Config:
        """Pydantic config for Settings class."""

        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Override settings for testing
if os.getenv("TESTING"):
    settings.DATABASE_URL = "sqlite+aiosqlite:///./test.db"
    settings.SECRET_KEY = "test-secret-key"
    settings.ENVIRONMENT = "testing"
