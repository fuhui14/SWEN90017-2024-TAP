from django.urls import path
from . import views
from .views import transcription_history_by_token

urlpatterns = [
    path('', views.transcribe, name='transcribe'),
    path('historylogin/', views.send_history_portal_link, name='history-login'),
    path('history/<str:token>/', transcription_history_by_token, name='transcription-history-by-token'),
]