from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_audio_file, name='upload_audio_file'),
    path('history/', views.get_transcription_history, name='get_transcription_history'),
    path('hello/', views.hello_world, name='hello_world'),
]
