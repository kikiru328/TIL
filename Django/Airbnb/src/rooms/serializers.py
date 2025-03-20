from rest_framework.serializers import ModelSerializer

from categories.serializers import CategorySerializer
from rooms.models import Room, Amenity
from users.serializers import TinyUserSerializer

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description"
        )

class RoomDetailSerializer(ModelSerializer):
    # model field = serializer
    owner = TinyUserSerializer() # related,
    amenities = AmenitySerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"
        depth = 1 # depth: api view 내에 id로 만 있는 것들을 object로
        # depth=1: expand All, (cant customize)

class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )


    # modelserializer: created_at, updated_at, id -- readonly in default