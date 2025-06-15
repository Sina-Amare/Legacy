from celery import Celery
from app.core.config import settings

# Initialize Celery
# This creates a Celery instance that will connect to our Redis broker.
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Optional: configure Celery further if needed
celery_app.conf.update(
    task_track_started=True,
)