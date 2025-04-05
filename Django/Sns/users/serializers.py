from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
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

class UserSignUpSerializer(ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email"
        )
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Already exists username")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must at least 8 digits")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user