from django.urls import path, include

urlpatterns = [
    path('transcription/', include('transcription.urls')),
    # path('speaker-identify/', include('speaker_identify.urls')),
    path('emails/', include('emails.urls')),
]

