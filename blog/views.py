# Create your views here.
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Post, Tag, Like, Comment, Category
from .permissions import IsOwnerOrAdmin
from .serializers import PostSerializer, TagSerializer, CategorySerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request, *args, **kwargs):
        qs = request.query_params.get('q', None)
        if qs:
            self.queryset = self.queryset.filter(Q(tags__name__icontains=qs)
                                                 | Q(categories__name__icontains=qs) | Q(
                title__icontains=qs)).distinct()

        serializer = self.get_serializer(self.get_queryset(), many=True,
                                         fields=['pk', 'title', 'content', 'owner', 'tags', 'tags2', 'categories',
                                                 'likes', 'comments'])
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer
    lookup_field = 'pk'


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        p_pk = self.kwargs['p_pk']
        return Comment.objects.filter(post__pk=p_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['p_pk'] = self.kwargs['p_pk']
        context['owner'] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
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
