from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # ← без next_page
    path('', lambda request: redirect('games')),
    path('games/', include('games.urls')),
    path('users/', include('users.urls')),
    path('recommendations/', include('recommendations.urls')),
]