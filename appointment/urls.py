from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    # Admin URLs
    path('', views.appointment_list, name='appointment_list'),
    path('add/', views.appointment_create, name='appointment_create'),
    path('<int:pk>/edit/', views.appointment_update, name='appointment_update'),
    path('<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('<int:pk>/approve/', views.appointment_approve, name='appointment_approve'),
    
    # Customer URLs
    path('book/', views.customer_appointment_book, name='customer_appointment_book'),
    path('<int:pk>/cancel/', views.customer_appointment_cancel, name='customer_appointment_cancel'),
]
