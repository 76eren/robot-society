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

from society.views.post_view import create_post, get_all_posts_by_user
from society.views.user_view import create_user, get_all_users, get_user_by_id

urlpatterns = [
    path('users/register', create_user, name='create_new_user'),
    path('users/', get_all_users, name='get_all_users'),
    path('users/<uuid:user_id>/', get_user_by_id, name='get_user_by_id'),


    path('post/create', create_post, name='create_post'),
    path('post/<str:username>/', get_all_posts_by_user, name='get_all_posts_by_user')
]
