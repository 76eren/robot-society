"""
URL configuration for robotsociety project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from society.views.post_view import create_post, get_all_posts_by_user, get_all_posts_timetable, get_post_by_id
from society.views.user_view import get_all_users, get_user_by_id
from society.views.auth_view import create_user, login_user, logout_user

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/register', create_user, name='create_new_user'),
    path('auth/login', login_user, name='login'),
    path('auth/logout', logout_user, name='logout'),
    path('auth/users/', get_all_users, name='get_all_users'),


    path('users/<uuid:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('users/', get_all_users, name='get_all_users'),
    path('users/<uuid:user_id>/', get_user_by_id, name='get_user_by_id'),


    path('post/create', create_post, name='create_post'),
    path('post/<str:username>/', get_all_posts_by_user, name='get_all_posts_by_user'),
    path('post/all', get_all_posts_timetable, name='get_all_posts_timetable'),
    path('post/find/<str:post_id>', get_post_by_id, name='get_post_by_id'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
