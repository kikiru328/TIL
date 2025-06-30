from rest_framework.serializers import ModelSerializer, SerializerMethodField

from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer
from .models import Perk, Experience


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"

class ExperienceListSerializer(ModelSerializer):
    is_host = SerializerMethodField()
    class Meta:
        model = Experience
        fields = (
            "id",
            "name",
            "category",
            "is_host",
        )
    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user


class ExperienceDetailSerializer(ModelSerializer):
    perks = PerkSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True
    )
    host = TinyUserSerializer(read_only=True)
    is_host = SerializerMethodField()
    class Meta:
        model = Experience
        exclude = (
            "created_at",
            "updated_at",
        )

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user
