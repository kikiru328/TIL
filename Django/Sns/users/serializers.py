from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import User
class UserDefaultSerializer(ModelSerializer):

    followings_count = SerializerMethodField() # user가 팔로잉 하는 수
    followers_count = SerializerMethodField() # user가 팔로우 당하는 수

    class Meta:
        model = User
        fields=(
            "pk",
            "avatar",
            "username",
            "followings_count",
            "followers_count",
            "date_joined"
        )

    def get_followings_count(self, user):
        return user.followings.count()

    def get_followers_count(self, user):
        return user.followers.count()

class UserDetailSerializer(ModelSerializer):

    followings_count = SerializerMethodField() # user가 팔로잉 하는 수
    followers_count = SerializerMethodField() # user가 팔로우 당하는 수

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("followings_count", "followers_count")

    def get_followings_count(self, user):
        return user.followings.count()

    def get_followers_count(self, user):
        return user.followers.count()

class UserFollowSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "avatar",
            "username",
        )

class LogInSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
        )