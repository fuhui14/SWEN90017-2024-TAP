from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),           # 核心 API 路由
    path('api/users/', include('users.urls')),    # 用户管理相关 API
    path('api/transcription/', include('transcription.urls')),  # 语音转录 API
]
