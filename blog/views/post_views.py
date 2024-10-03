from django.conf import settings
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.models import Post
from blog.permissions import IsOwnerOrAdmin
from blog.serializers import PostSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

AppUser = settings.AUTH_USER_MODEL


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_posts(request, username=None):
    if username:
        print(username)
        try:
            user = AppUser.objects.get(username=username)
        except AppUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        user = request.user
    posts = Post.objects.filter(owner=user)
    serializer = PostSerializer(posts, many=True, fields=['pk', 'title', 'content'])
    return Response(serializer.data, status=status.HTTP_200_OK)
