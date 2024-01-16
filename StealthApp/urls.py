from django import views
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('profile/<int:id>/', views.profile),
    path('login-history/<int:id>/', views.login_history),
    path('add-user/', views.add_user),
]