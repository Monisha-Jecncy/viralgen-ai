from celery import Celery
from app.config import Config

celery_app = Celery(
    "worker",
    broker=Config.REDIS_URL,
    backend=Config.REDIS_URL,
)

celery_app.conf.task_routes = {"app.workers.generation_worker.*": {"queue": "default"}}
