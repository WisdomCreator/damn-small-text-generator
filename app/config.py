from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "damn-small-text-generator"
    REDIS_URL: str
    DATABASE_URL: str


@lru_cache
def get_settings():
    return Settings()
