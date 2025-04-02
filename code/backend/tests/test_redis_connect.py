import redis
from django.conf import settings

print("Trying to connect to:", settings.CELERY_BROKER_URL)

r = redis.from_url(settings.CELERY_BROKER_URL)
print("Ping result:", r.ping())