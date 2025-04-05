from django.urls import path, include

urlpatterns = [
    path('transcription/', include('transcription.urls')),
    path('history/', include('history.urls')),
    # path('speaker-identify/', include('speaker_identify.urls')),
]

