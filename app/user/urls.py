from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('', views.home),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.view_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('change_password/', views.change_password, name='change_password'),
]