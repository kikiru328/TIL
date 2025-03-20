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
    owner = TinyUserSerializer(read_only=True) # related, # serializer doesn't ask owner data
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True,)

    class Meta:
        model = Room
        fields = "__all__"
        depth = 1 # depth: api view 내에 id로 만 있는 것들을 object로
        # depth=1: expand All, (cant customize)

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

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