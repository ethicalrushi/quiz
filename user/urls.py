from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views
urlpatterns = [
    path('login/', views.app_login, name='login'),
    path('register/', views.app_register, name='register'),
    path('logout/', views.app_logout, name='logout'),
]