from django.conf import settings
from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.response import Response
from bookings.serializers import CreateExperienceBookingSerializer, PublicRoomBookingSerializer, \
    PublicExperienceBookingSerializer
from bookings.models import Booking
from categories.models import Category
from .models import Perk, Experience
from .serializers import PerkSerializer, ExperienceListSerializer, ExperienceDetailSerializer


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)

class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                PerkSerializer(updated_perk).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class Experiences(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
            experiences = Experience.objects.all()
            serializer = ExperienceListSerializer(
                experiences,
                many=True,
                context={"request": request}
            )
            return Response(serializer.data)


    def post(self, request):
        serializer = ExperienceDetailSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("Category kind should be Experience")
            except Category.DoesNotExist:
                raise ParseError("Category Not Found")

            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                    serializer = ExperienceDetailSerializer(
                        experience,
                        context={"request": request},
                    )
                    return Response(serializer.data)
            except Exception as e:
                raise ParseError(f"Something Wrong, {e}")
        else:
            return Response(serializer.errors)

class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = ExperienceDetailSerializer(
            experience,
            context={"request": request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk=pk)
        if experience.host != request.user:
            raise PermissionError

        serializer = ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("Category should be Experiences")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    if category_pk:
                        experience = serializer.save(category=category)
                    else:
                        experience = serializer.save()

                    perks = request.data.get("perks")
                    if perks:
                        experience.perks.clear()
                        for perk_pk in perks:
                            perk = Perk.objects.get(pk=perk_pk)
                            experience.perks.add(perk)
                    else:
                        experience.perks.clear()

                    return Response(ExperienceDetailSerializer(
                        experience,
                        context={"request": request},
                    ).data)

            except Exception as e:
                raise ParseError(f"Perk not found \n error: {e}")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk=pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class ExperiencePerks(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk=pk)
        print(experience.perks)
        serializer = PerkSerializer(
            experience.perks.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        bookings = Booking.objects.filter(experience=experience)
        serializer = PublicExperienceBookingSerializer(
            bookings,
            many=True
        )
        return Response(serializer.data)


    def post(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = CreateExperienceBookingSerializer(
            data=request.data,
            context={"experience": experience},
        )
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            return Response(status=HTTP_200_OK)
        else:
            return Response(serializer.errors)

class ExperienceBookingsDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_booking_object(self, ex_pk, bk_pk):
        try:
            experience = Experience.objects.get(pk=ex_pk)
        except Experience.DoesNotExist:
            raise NotFound

        try:
            return Booking.objects.get(pk=bk_pk, experience=experience)
        except Booking.DoesNotExist:
            raise NotFound


    def get_experience_object(self, ex_pk, bk_pk):
        try:
            return Experience.objects.get(pk=ex_pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, ex_pk, bk_pk):
        booking = self.get_booking_object(ex_pk, bk_pk)
        serializer = PublicExperienceBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, ex_pk, bk_pk):
        experience = self.get_experience_object(ex_pk, bk_pk)
        booking = self.get_booking_object(ex_pk, bk_pk)
        serializer = CreateExperienceBookingSerializer(
            booking,
            data = request.data,
            partial=True,
            context={"experience": experience}
        )
        if serializer.is_valid():
            booking = serializer.save()
            serializer = CreateExperienceBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, ex_pk, bk_pk):
        booking = self.get_booking_object(ex_pk, bk_pk)
        booking.delete()
        return Response(status=HTTP_204_NO_CONTENT)

