from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post

from users.serializers import DefaultUserSerializer

class PostListSerializer(ModelSerializer):
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "pk",
            "author",
            "title",
            "content",
            "image",
            "is_author",
            "created_at",
            "updated_at",
        )

    def get_is_author(self, post):
        request = self.context["request"]
        return post.author == request.user


class PostDetailSerializer(ModelSerializer):
    author = DefaultUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = (
            "author",
            "title",
            "content",
            "image",
        )
