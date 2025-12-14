from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('search/', views.restaurant_search, name='restaurant_search'),
    path('map/', views.map_demo, name='map_demo'),
    path('nearby/', views.nearby_restaurants, name='nearby_restaurants')

]
