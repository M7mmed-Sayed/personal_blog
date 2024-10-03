from rest_framework import serializers
from .dynamic_serializer import DynamicFieldsModelSerializer
from ..models import Post, Like, Comment


class PostSerializer(DynamicFieldsModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = [
            'owner',
            'pk',
            'title',
            'content',
            'tags',
            'categories',
            'likes',
            'comments'
        ]

    def get_likes(self, obj):
        return Like.objects.filter(post=obj).count()

    def get_comments(self, obj):
        return Comment.objects.filter(post=obj).count()

    def validate_title(self, value):
        request = self.context.get('request')
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        # check if the post title is exist and not for the current one
        if request and request.method in ['PUT', 'PATCH']:
            post_id = self.instance.id if self.instance else None
            if Post.objects.filter(title=value).exclude(pk=post_id).exists():
                raise serializers.ValidationError("A post with this title already exists.")

        else:
            if Post.objects.filter(title=value).exists():
                raise serializers.ValidationError("A post with this title already exists.")

        return value

    def validate_categories(self, value):
        if not value:
            raise serializers.ValidationError("the post must be assigned to a category.")
        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("Content cannot be empty.")
        return value

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)
        categories_data = validated_data.pop('categories', None)
        validated_data['owner'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        if tags_data is not None:
            post.tags.set(tags_data)  #
        if categories_data is not None:
            post.categories.set(categories_data)  #
        return post

