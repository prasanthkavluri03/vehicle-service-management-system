from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('add/', views.service_create, name='service_create'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
    path('<int:pk>/edit/', views.service_update, name='service_update'),
    path('<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('<int:pk>/job-card/', views.job_card, name='job_card'),
    
    # Parts Usage URL Handlers
    path('<int:pk>/parts/add/', views.add_parts_usage, name='add_parts_usage'),
    path('parts/delete/<int:pk>/', views.delete_parts_usage, name='delete_parts_usage'),
]
