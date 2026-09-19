"""
URL configuration for vehicle_service_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('customers/', include('customers.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('appointments/', include('appointment.urls')),
    path('services/', include('services.urls')),
    path('technicians/', include('technicians.urls')),
    path('inventory/', include('inventory.urls')),
    path('billing/', include('billing.urls')),
    path('vehicles/', include('vehicles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
