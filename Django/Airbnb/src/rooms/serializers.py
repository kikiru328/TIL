from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from rooms.models import Room, Amenity
from users.serializers import TinyUserSerializer
from wishlists.models import Wishlist
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
    rating = serializers.SerializerMethodField() # Method
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)
    # reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        depth = 1 # depth: api view 내에 id로 만 있는 것들을 object로
        # depth=1: expand All, (cant customize)

    def get_rating(self, room): # convertion: get_{field name}
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
        ).exists()




class RoomListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    # modelserializer: created_at, updated_at, id -- readonly in default