from django.urls import path, include

urlpatterns = [
    path('transcription/', include('transcription.urls')),
    path('history/', include('history.urls')),
    path('historylogin/', include('history_login.urls')),
    # path('speaker-identify/', include('speaker_identify.urls')),
]

