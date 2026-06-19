from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('add/', views.invoice_create, name='invoice_create'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('<int:pk>/pay/', views.invoice_pay, name='invoice_pay'),
    path('<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
]
