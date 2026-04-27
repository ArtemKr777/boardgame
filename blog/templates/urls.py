from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendations, name='recommendations'),
    path('create-request/', views.create_request, name='create_request'),
    path('respond/<int:request_id>/', views.respond_to_request, name='respond_request'),
]