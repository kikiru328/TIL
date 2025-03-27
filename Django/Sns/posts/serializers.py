from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from posts.models import Post

from users.serializers import DefaultUserSerializer


class PostListSerializer(ModelSerializer):
    is_author = SerializerMethodField()
    likes_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_is_author(self, post):
        request = self.context["request"]
        return post.author == request.user

    def get_likes_count(self, post):
        return post.likes.count()


class PostDetailSerializer(ModelSerializer):
    author = DefaultUserSerializer(read_only=True)
    likes_count = SerializerMethodField()
    class Meta:
        model = Post
        fields = "__all__"
        depth = 1

    def get_likes_count(self, post):
        return post.likes.count()