from contextlib import asynccontextmanager

from fastapi import FastAPI, status, HTTPException
from pymongo.errors import PyMongoError

from app.api.exception_handlers import register_exception_handlers
from app.api.v1.routers.task_router import router as task_router
from app.api.v1.routers.auth_router import router as auth_router
from app.core.config import settings
from app.core.database import get_client, close_client
from app.core.indexes import init_all_indexes
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    client = get_client()
    try:
        await client.admin.command("ping")
        db = client[settings.mongo_db]
        await init_all_indexes(db)
        yield
    finally:
        close_client()


def create_app() -> FastAPI:
    configure_logging("INFO")

    app = FastAPI(
        title="TODO API (FastAPI + MongoDB/Motor)",
        version="2.0.0",
        description="DDD layers, SOLID/KISS/DRY, strict settings (no defaults), JWT auth.",
        lifespan=lifespan,
    )

    register_exception_handlers(app)

    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
    app.include_router(task_router, prefix="/api/v1/tasks", tags=["Tasks"])

    @app.get("/", tags=["Root"], status_code=status.HTTP_200_OK)
    async def root():
        return {"status": "ok", "mode": settings.app_mode}

    @app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
    async def health():
        try:
            await get_client().admin.command("ping")
            return {"status": "healthy"}
        except PyMongoError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="degraded"
            )

    return app


app = create_app()
