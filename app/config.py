from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "damn-small-text-generator"
    REDIS_URL: str
    SYNC_DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    DATABASE_ECHO: Optional[bool] = False


@lru_cache
def get_settings():
    return Settings()
