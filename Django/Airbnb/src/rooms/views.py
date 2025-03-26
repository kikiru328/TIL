from wsgiref.util import request_uri
from django.utils import timezone
from django.core.serializers import serialize
from django.db import transaction
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
from categories.models import Category
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bookings.models import Booking
# Create your views here.
class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:

                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic(): # Transaction: one fail, all roll backed.
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not Found ")
        else:
            return Response(serializer.errors)




class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk=pk)
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid(): # True, valid
            # update category: Foreign Key
            category_pk = request.data.get("category")
            if category_pk: # exists
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES: # Experiences
                        raise ParseError("Category should be 'room'")
                except Category.DoesNotExist:
                    raise ParseError("Category Not Found")


            try:
                with transaction.atomic(): # roll back when query fails
                    # Update Category
                    if category_pk: # category pk exists
                        room = serializer.save(category=category) #update
                    else:
                        room = serializer.save() # nothing to change

                    # update Amenities: ManytoMany
                    amenities = request.data.get("amenities")
                    if amenities: # exists
                        room.amenities.clear() # update: delete list (reset)
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity) # update: added amenities
                    else:
                        room.amenities.clear() # amenities == empty list, return same empty list
                    return Response(RoomDetailSerializer(room).data)
            except Exception as e:
                raise ParseError(f"Amenity Not Found\n error: {e}")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk=pk)
        # same user?
        if  room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


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

class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # print(request.query_params) # get url parameter
        try:
            page = request.query_params.get("page", 1) # default page=1 -> string
            page = int(page)
        except ValueError:
            page = 1 # back to default 1 * string convert error
        page_size = 3 # [start index from]
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk=pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end], #  query set
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(
            data=request.data
        )
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk=pk)
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomAmenities(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 2 # how many items will display
        start = (page -1 ) * page_size
        end = start + page_size
        room = self.get_object(pk=pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end], # limit:offset
            many=True,
        )
        return Response(serializer.data)

class RoomPhotos(APIView):
    # POST
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk=pk)

        if request.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        now = timezone.localtime(timezone.now()).date()

        bookings = Booking.objects.filter(room=room,
                                          kind=Booking.BookingKindChoices.ROOM,
                                          check_in__gt=now,)
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)
        # url pagination, by month

    def post(self, request, pk):
        room = self.get_object(pk=pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)