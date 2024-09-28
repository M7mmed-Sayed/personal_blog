"""
URL configuration for personal_blog project.

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

from . import views

urlpatterns = [
    # Post Urls
    path('posts/', views.PostViewSet.as_view({
        'get': 'list'
        , 'post': 'create',  # Create
    }), name='post-list'),
    path('posts/<int:pk>/', views.PostViewSet.as_view({
        'get': 'retrieve',  # get
        'put': 'update',  # Update
        'delete': 'destroy'  # Delete
    }), name='post-detail'),

    # Categories Url
    path('category/', views.CategoryViewSet.as_view({
        'get': 'list'
        , 'post': 'create',  # Create
    }), name='category-list'),
    path('category/<int:pk>/', views.CategoryViewSet.as_view({
        'get': 'retrieve',  # get
        'put': 'update',  # Update
        'delete': 'destroy'  # Delete
    }), name='category-detail'),
    # Tag Url
    path('tags/', views.TagViewSet.as_view({
        'get': 'list'
        , 'post': 'create',  # Create
    }), name='tags-list'),
    path('tags/<int:pk>/', views.TagViewSet.as_view({
        'get': 'retrieve',  # get
        'put': 'update',  # Update
        'delete': 'destroy'  # Delete
    }), name='tag-detail'),
    path('posts/<int:pk>/like/', views.like_or_unlike_post, name='like-or-unlike-post'),
    path('posts/<int:p_pk>/comment/', views.CommentViewSet.as_view({
        'post': 'create',
        'get': 'list',
    }), name='comment-post'),
    path('posts/comment/<int:pk>/', views.CommentViewSet.as_view({
        'get': 'retrieve',  # get
        'delete': 'destroy'  # Delete
    }), name='comment-post-datial'),
]
