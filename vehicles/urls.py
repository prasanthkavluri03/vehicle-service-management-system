from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    # Admin URLs
    path('', views.vehicle_list, name='vehicle_list'),
    path('add/', views.vehicle_create, name='vehicle_create'),
    path('<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('<int:pk>/edit/', views.vehicle_update, name='vehicle_update'),
    path('<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    
    # Customer URLs
    path('customer/add/', views.customer_vehicle_create, name='customer_vehicle_create'),
    path('customer/<int:pk>/', views.customer_vehicle_detail, name='customer_vehicle_detail'),
    path('customer/<int:pk>/edit/', views.customer_vehicle_update, name='customer_vehicle_update'),
    path('customer/<int:pk>/delete/', views.customer_vehicle_delete, name='customer_vehicle_delete'),
]
