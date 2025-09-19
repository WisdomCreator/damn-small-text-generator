from fastapi import APIRouter
from app.api.v1 import text_generations
from app.api.v1 import models

api_router = APIRouter()
api_router.include_router(text_generations.router)
api_router.include_router(models.router)
