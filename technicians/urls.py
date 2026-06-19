from django.urls import path
from . import views

app_name = 'technicians'

urlpatterns = [
    # Admin URLs
    path('', views.technician_list, name='technician_list'),
    path('add/', views.technician_create, name='technician_create'),
    path('<int:pk>/edit/', views.technician_update, name='technician_update'),
    path('<int:pk>/delete/', views.technician_delete, name='technician_delete'),
    
    # Technician Portal
    path('dashboard/', views.technician_dashboard, name='technician_dashboard'),
]
