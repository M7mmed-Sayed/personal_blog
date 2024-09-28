from rest_framework import serializers

from .DynamicSerializer import DynamicFieldsModelSerializer
from .models import Post, Category, Tag, Comment, Like


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


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
