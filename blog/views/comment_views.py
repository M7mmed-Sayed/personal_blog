from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.models import Comment
from blog.permissions import IsOwnerOrAdmin
from blog.serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        p_pk = self.kwargs.get('p_pk', None)

        if p_pk:
            return Comment.objects.filter(post__pk=p_pk)
        else:
            return Comment.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['p_pk'] = self.kwargs.get('p_pk', None)
        context['owner'] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
