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
    path('addthema', views.addthema, name='addthema'),
    path('my_thema', views.my_thema, name='my_thema'),
    path('stamp/<int:bookstore_id>', views.stamp, name='stamp'),
    path('ranking/', views.ranking, name='ranking'),
]