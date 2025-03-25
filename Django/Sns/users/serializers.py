from rest_framework.serializers import Serializer, ModelSerializer

from users.models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )