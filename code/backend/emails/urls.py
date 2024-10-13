from django.urls import path
from . import views

urlpatterns = [
    path('', views.download_file, name='download_file')
]
