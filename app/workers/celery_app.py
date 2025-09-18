from celery import Celery  # type: ignore[import-untyped]
from app.config import get_settings

settings = get_settings()
celery = Celery(
    "simple_text_generation_tool",
    broker=settings.REDIS_URL + "/0",
    backend=settings.REDIS_URL + "/1",
)
celery.conf.task_routes = {"app.workers.tasks.*": {"queue": "generations"}}
celery.autodiscover_tasks(["app.workers"])
