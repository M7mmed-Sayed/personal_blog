# Create your views here.
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from account.models import AppUser
from .models import Post, Tag, Like, Comment, Category
from .permissions import IsOwnerOrAdmin
from .serializers import PostSerializer, TagSerializer, CategorySerializer, CommentSerializer










