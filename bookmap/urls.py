from django.urls import path
from . import views

urlpatterns = [
    path('realmap/', views.realmap, name='realmap'),
    path('store/<int:bookstore_id>', views.detail, name='storedetail'),    
    path('scrap/<int:bookstore_id>', views.scrap, name='scrap'),
    path('reviewcreate/<int:bookstore_id>', views.reviewcreate, name='reviewcreate'),
    path('reviewdelete/<int:review_id>', views.reviewdelete, name='reviewdelete'),
    path('mapsearch/', views.mapsearch, name='mapsearch'),
    path('themamap/', views.themamap, name='themamap'),
    path('themadetail/<int:tag_id>', views.themadetail, name='themadetail'),
    path('thema_add', views.thema_add, name='thema_add'),
    path('thema_change/<int:tag_id>', views.thema_change, name='thema_change'),
    path('thema_delete/<int:tag_id>', views.thema_delete, name='thema_delete'),
    path('my_thema', views.my_thema, name='my_thema'),
    path('stamp/<int:bookstore_id>', views.stamp, name='stamp'),
    path('ranking/', views.ranking, name='ranking'),
    path('store_thema/<int:bookstore_id>/<int:tf>', views.store_thema, name='store_thema'),
    path('thema_like/<int:tag_id>/like', views.thema_like, name='thema_like'),
]