from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "ai_curation_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    enable_utc=True,
    timezone="Asia/Seoul",
    result_serializer="json",
    task_serializer="json",
    accept_content=["json"]
)