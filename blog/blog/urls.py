from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # allauth URLs (вход, регистрация, подтверждение email, выход)
    path('accounts/', include('allauth.urls')),  # ← ВАЖНО: должны быть до ваших маршрутов

    # Ваши маршруты
    path('', lambda request: redirect('games')),
    path('games/', include('games.urls')),
    path('users/', include('users.urls')),
    path('recommendations/', include('recommendations.urls')),
]

# Примечание: старые маршруты login/logout больше не нужны, их заменил allauth