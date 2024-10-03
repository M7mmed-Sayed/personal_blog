from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from blog.models import Tag
from blog.serializers import TagSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'
