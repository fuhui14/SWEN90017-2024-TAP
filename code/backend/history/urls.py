# history/urls.py

from django.urls import path
from .views import admin_history,download_history

urlpatterns = [
    path('api/admin/history/', admin_history, name='admin_history'),
    path('api/download/', download_history, name='admin_history'),

]
