from celery import Celery
from app.core.config import settings

# This file defines the central Celery application instance.
# It is the single entry point for the Celery system.
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    # This 'include' list is the key to decoupling. Celery will automatically
    # discover tasks within these modules.
    include=['app.ai.tasks']
)

celery_app.conf.update(
    task_track_started=True,
)