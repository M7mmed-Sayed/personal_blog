from rest_framework.viewsets import ModelViewSet

from blog.models import Category
from rest_framework.permissions import IsAdminUser

from blog.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    lookup_field = 'pk'
