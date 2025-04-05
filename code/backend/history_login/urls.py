from django.urls import path
from .views import send_history_link

urlpatterns = [
    path('api/send-history-link/', send_history_link, name='send_history_link'),
]
