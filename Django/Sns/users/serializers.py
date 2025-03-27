from rest_framework.serializers import ModelSerializer

from users.models import User
class DefaultUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields=(
            "avatar",
            "username"
        )