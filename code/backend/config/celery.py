import os
from celery import Celery

# Set environment variable to point to Django's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create a Celery instance; the name can be customized, typically matching the project name
app = Celery('config')

# Load configuration from Django's settings.py using the CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in all installed apps
app.autodiscover_tasks()

# Optional: a simple debug task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
