from fastapi import APIRouter
from app.api.v1 import text_generations

api_router = APIRouter()
api_router.include_router(text_generations.router)
