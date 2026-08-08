"""Application settings, loaded from environment variables via pydantic-settings.

Never read os.environ directly in this project — settings live here.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CACHE_ROOT = PROJECT_ROOT / ".cache"


class Settings(BaseSettings):
    """All configuration, with safe defaults for local development."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = ""
    embedding_provider: str = "local"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "f1rag"
    postgres_password: str = "f1rag"
    postgres_db: str = "f1rag"


settings = Settings()
