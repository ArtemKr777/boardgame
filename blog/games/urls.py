from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='games'),
    path('add-to-collection/<int:game_id>/', views.add_to_collection, name='add_to_collection'),
    path('remove-from-collection/<int:game_id>/', views.remove_from_collection, name='remove_from_collection'),
]