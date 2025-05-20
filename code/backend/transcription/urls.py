from django.urls import path
from . import views
from .views import transcription_history_by_token, task_status_view, transcription_stream

urlpatterns = [
    path('', views.transcribe, name='transcribe'),
    path('historylogin/', views.send_history_portal_link, name='history-login'),
    path('history/<str:token>/', transcription_history_by_token, name='transcription-history-by-token'),
    path('api/status/<uuid:task_id>/', task_status_view, name='task-status'),
    path('stream/', transcription_stream, name='transcription-stream'),
]
