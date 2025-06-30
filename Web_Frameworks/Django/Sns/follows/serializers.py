from rest_framework.serializers import ModelSerializer
from follows.models import Follow
from users.serializers import UserFollowSerializer
class FollowerSerializer(ModelSerializer):

    user = UserFollowSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = (
            "pk",
            "user",
            "follower",
        )