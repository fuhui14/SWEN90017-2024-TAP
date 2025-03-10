from django.urls import include, path

urlpatterns = [
    # Versioned API routes
    path('v1/transcription/', include('transcription.urls')),
    # path('v1/speaker-identify/', include('speaker_identify.urls')),
]
