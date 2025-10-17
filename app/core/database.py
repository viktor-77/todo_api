from typing import Optional
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

_DATABASE_URL: str = settings.mongo_url
_DATABASE_NAME: str = settings.mongo_db
_MAX_POOL_SIZE: int = settings.mongo_max_pool_size
_MIN_POOL_SIZE: int = settings.mongo_min_pool_size
_SERVER_SELECTION_TIMEOUT_MS: int = settings.mongo_server_selection_timeout_ms
_CONNECT_TIMEOUT_MS: int = settings.mongo_connect_timeout_ms
_SOCKET_TIMEOUT_MS: int = settings.mongo_socket_timeout_ms
_MAX_CONNECTING: int = settings.mongo_max_connecting
_MAX_IDLE_TIME_MS: int = settings.mongo_max_idle_time_ms
_COMPRESSORS: str = settings.mongo_compressors

_client: Optional[AsyncIOMotorClient] = None


def get_client() -> AsyncIOMotorClient:
    """
    Provide a singleton MongoDB client to avoid redundant TCP connections.
    """
    global _client
    if _client is None:
        kwargs = dict(
            maxPoolSize=_MAX_POOL_SIZE,
            minPoolSize=_MIN_POOL_SIZE,
            serverSelectionTimeoutMS=_SERVER_SELECTION_TIMEOUT_MS,
            connectTimeoutMS=_CONNECT_TIMEOUT_MS,
            socketTimeoutMS=_SOCKET_TIMEOUT_MS,
            maxConnecting=_MAX_CONNECTING,
            maxIdleTimeMS=_MAX_IDLE_TIME_MS,
            tz_aware=True,
            retryWrites=True,
            retryReads=True,
            uuidRepresentation="standard",
        )
        if _COMPRESSORS.strip():
            kwargs["compressors"] = _COMPRESSORS

        _client = AsyncIOMotorClient(_DATABASE_URL, **kwargs)
    return _client


def get_database(
    client: AsyncIOMotorClient = Depends(get_client)) -> AsyncIOMotorDatabase:
    """
    Provide the configured database via FastAPI dependency.
    """
    return client[_DATABASE_NAME]


def close_client() -> None:
    """
    Close the MongoDB client and reset the singleton.
    """
    global _client
    if _client is not None:
        _client.close()
        _client = None
