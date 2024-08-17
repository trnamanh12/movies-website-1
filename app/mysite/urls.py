"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Path: app/mysite/urls.py
from django.contrib import admin
from django.urls import path, include
from movies import views as movie_views
from user import views as user_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie_views.home, name='home'),
    path('movies/', include('movies.urls')),
    path('user/', include('user.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', user_views.user_login, name='login'),
    path('accounts/register/', user_views.register, name='register'),
    path('accounts/logout/', user_views.user_logout, name='logout'),
    path('accounts/profile/', user_views.view_profile, name='profile'),
    # path('home/', movie_views.home, name='home'),
    path('cart/', include('cart.urls')),
]
