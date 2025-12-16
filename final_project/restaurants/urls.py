from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.restaurant_search, name='restaurant_search'),
    path('api/search/', views.search_api, name='search_api'),
    path('roulette/', views.roulette_view, name='roulette'),
    path('roulette/search/', views.roulette_search_api, name='roulette_search'),
    path('board/', views.board_list, name='board_list'),
    path('board/write/', views.board_write, name='board_write'),
    path('board/<int:pk>/', views.board_detail, name='board_detail'),
    path('board/api/search/', views.board_search_api, name='board_search_api'),
]
