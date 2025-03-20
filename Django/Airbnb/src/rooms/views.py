from django.core.serializers import serialize
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from categories.models import Category
from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer


# Create your views here.
class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError
                    raise ParseError("Category not found")
                room = serializer.save(
                    owner=request.user,
                    category=category,
                )
                amenities = request.data.get("amenities")
                for amenity_pk in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                    except Amenity.DoesNotExist:
                        room.delete()
                        raise ParseError(f"Amenity with id {amenity_pk} not found")
                    room.amenities.add(amenity)
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated




class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        amenity = serializer.save()
        return Response(AmenitySerializer(amenity).data)

class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk=pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk=pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_amenity = serializer.save()
        return Response(
            AmenitySerializer(updated_amenity).data
        )

    def delete(self, request, pk):
        amenity = self.get_object(pk=pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)