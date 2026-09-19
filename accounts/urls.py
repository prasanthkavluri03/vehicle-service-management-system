from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('redirect/', views.login_redirect, name='login_redirect'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.user_list, name='user_list'),
]
