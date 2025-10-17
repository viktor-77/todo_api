import os
from enum import StrEnum
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppMode(StrEnum):
    development = "development"
    test = "test"
    production = "production"


# Fail fast if APP_MODE is not provided or invalid
try:
    _APP_MODE_RAW = os.environ["APP_MODE"]
except KeyError as e:
    raise RuntimeError("APP_MODE environment variable must be set.") from e

try:
    _APP_MODE = AppMode(_APP_MODE_RAW)
except ValueError as e:
    raise RuntimeError(
        "APP_MODE must be one of: development|test|production."
    ) from e


def _detect_env_file() -> str | None:
    """
    Load env/.env.<APP_MODE> for local dev/test convenience if it exists.
    In production, rely purely on environment variables (file may be absent).
    """
    candidate = Path(f"env/.env.{_APP_MODE}")
    return str(candidate) if candidate.exists() else None


class Settings(BaseSettings):
    # --- App ---
    app_mode: AppMode
    app_secret_key: SecretStr
    app_host: str
    app_port: int

    # --- MongoDB ---
    mongo_url: str
    mongo_db: str
    mongo_max_pool_size: int
    mongo_min_pool_size: int
    mongo_server_selection_timeout_ms: int
    mongo_connect_timeout_ms: int
    mongo_socket_timeout_ms: int
    mongo_max_connecting: int
    mongo_max_idle_time_ms: int
    mongo_compressors: str

    # --- Auth/JWT ---
    jwt_secret_key: SecretStr
    jwt_algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=_detect_env_file(),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
