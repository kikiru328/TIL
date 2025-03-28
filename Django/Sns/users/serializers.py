from rest_framework.serializers import ModelSerializer

from users.models import User
class UserDefaultSerializer(ModelSerializer):
    class Meta:
        model = User
        fields=(
            "pk",
            "avatar",
            "username",
            "date_joined"
        )

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"