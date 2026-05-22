from django.urls import path
from . import views

urlpatterns = [
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    #path('register/', views.register, name='register'),
    path('add-played-game/<int:game_id>/', views.add_played_game, name='add_played_game'),
    path('', views.user_list, name='user_list'),           # ← /users/ - список пользователей
    path('<int:user_id>/', views.user_profile_detail, name='user_profile_detail'),  # ← /users/1/
]