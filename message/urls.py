from django.urls import path
from . import views

urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
    path('', views.chat_list, name='chat-list'),
    path('temp/<int:sb_id>/', views.temp, name='chat-temp'),
]