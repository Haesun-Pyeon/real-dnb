from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('del_user/', views.del_user, name='del_user'),
    path('user_change/', views.user_change, name='user_change'),
    path('social/', views.social, name='social'),
]