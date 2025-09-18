from fastapi import FastAPI
from app.config import get_settings
from app.api.router import api_router

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME, docs_url="/docs")
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/healthz")
def healthz():
    return {"ok": True}
