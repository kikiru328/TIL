from django.utils import timezone
from rest_framework import serializers
from .models import Booking
from datetime import time

class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out."
            )
        if Booking.objects.filter(
                check_in__lte=data["check_out"],
                check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken."
            )
        return data

class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_time = serializers.TimeField()

    class Meta:
        model = Booking
        fields = ("experience_time", "guests")

    def validate_experience_time(self, value):
        now_time = timezone.localtime().time()
        if value < now_time:
            raise serializers.ValidationError("Can't book past time")
        return value

    def validate(self, value):

        experience_time = value.get("experience_time")
        experience = self.context["experience"]

        if experience_time is None:
            return value

        if experience:
            if not (experience.start <= experience_time < experience.end):
                raise serializers.ValidationError(
                    f"Can reservation from {experience.start.strftime('%H:%M')} to {experience.end.strftime('%H:%M')}."
                )
        else:
            raise serializers.ValidationError("There is no experience")

        if Booking.objects.filter(experience_time=experience_time).exists():
            raise serializers.ValidationError("This date & time already taken")

        return value

class PublicRoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )

class PublicExperienceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience_time",
            "guests",
        )