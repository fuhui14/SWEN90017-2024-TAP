# backend/config/celery.py

import os
from celery import Celery

# 设置环境变量，指向 Django 的 settings 模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 创建 Celery 实例，名字可自定义，一般与项目同名
app = Celery('config')

# 从 Django 的 settings.py 中加载以 CELERY_ 开头的配置
app.config_from_object('django.conf:settings', namespace='CELERY')

print("[CELERY INIT] Broker URL:", os.environ.get("CELERY_BROKER_URL"))
print("[CELERY INIT] From settings:", app.conf.broker_url)

# 自动发现各个 app 下的 tasks.py
app.autodiscover_tasks()

