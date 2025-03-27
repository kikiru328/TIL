from rest_framework.serializers import ModelSerializer
from comments.models import Comment
from users.serializers import DefaultUserSerializer


class CommentSerializer(ModelSerializer):
    user = DefaultUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "pk",
            "user",
            "payload",
            "created_at"
        )