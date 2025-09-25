from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.config import get_settings
from app.api.router import api_router
from app.db.session import async_engine

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    yield
    # Shutdown code
    await async_engine.dispose()


app = FastAPI(title=settings.PROJECT_NAME, docs_url="/docs", lifespan=lifespan)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/healthz", tags=["health"])
async def healthz():
    async with async_engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    return {"ok": True}
