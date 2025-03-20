from rest_framework.serializers import ModelSerializer

from rooms.models import Amenity


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"

    # modelserializer: created_at, updated_at, id -- readonly in default