from rest_framework.serializers import ModelSerializer

from posts.models import Post

from users.serializers import DefaultUserSerializer

class PostSerializer(ModelSerializer):
    user = DefaultUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = (
            "user",
            "title",
            "content",
            "image",
        )