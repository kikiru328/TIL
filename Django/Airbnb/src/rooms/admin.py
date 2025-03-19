from django.contrib import admin
from .models import Room, Amenity
# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
        )

    search_fields = (
        # default: contains search string
        "^name", # ^{str}: startswith search string
        "=price", # ={str}: equal search string
        "owner__username" #{field}__{orm field}: searching by orm
    )

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )



@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name", "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at"
    )