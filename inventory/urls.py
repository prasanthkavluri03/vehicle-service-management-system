from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.part_list, name='part_list'),
    path('add/', views.part_create, name='part_create'),
    path('<int:pk>/edit/', views.part_update, name='part_update'),
    path('<int:pk>/delete/', views.part_delete, name='part_delete'),
    path('usage-history/', views.parts_usage_history, name='parts_usage_history'),
]
