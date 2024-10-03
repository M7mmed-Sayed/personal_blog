from rest_framework import serializers

from ..models.comment import Comment
from ..models.post import Post


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'owner', 'post', 'content', 'created_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_post(self, obj):
        return obj.post.id

    def validate(self, data):
        p_pk = self.context.get('p_pk')
        # try -catch must be existed to check if it is valid, and we have a post
        try:
            Post.objects.get(pk=p_pk)
        except Post.DoesNotExist:
            raise serializers.ValidationError({"post": "Post not found ."})
        return data

    def create(self, validated_data):
        p_pk = self.context.get('p_pk')
        post = Post.objects.get(pk=p_pk)
        return Comment.objects.create(post=post, **validated_data)
