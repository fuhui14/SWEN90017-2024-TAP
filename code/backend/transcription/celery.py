from celery import Celery
import os

app = Celery('transcription', broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'))

app.conf.update(
    result_backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
