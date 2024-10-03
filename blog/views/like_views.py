from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from blog.models import Post, Like

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_or_unlike_post(request, pk):
    """
    un/like the post
    """
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    existing_like = Like.objects.filter(owner=user, post=post).first()
    if existing_like:
        existing_like.delete()
        return Response({'message': 'unliked'}, status=status.HTTP_200_OK)
    else:
        Like.objects.create(owner=user, post=post)
        return Response({'message': 'liked'}, status=status.HTTP_201_CREATED)