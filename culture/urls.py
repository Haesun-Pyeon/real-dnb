from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board, name='board'),
    path('board2/', views.board2, name='board2'),

]