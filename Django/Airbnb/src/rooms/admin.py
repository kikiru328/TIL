from django.contrib import admin
from .models import Room, Amenity
# Register your models here.

@admin.action(description="Set all Prices to Zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (
        reset_prices,
    )

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