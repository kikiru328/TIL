from rest_framework.serializers import ModelSerializer
from comments.models import Comment
from users.serializers import UserDefaultSerializer


class CommentSerializer(ModelSerializer):
    user = UserDefaultSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "pk",
            "user",
            "payload",
            "created_at"
        )