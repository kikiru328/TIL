from typing import List, Tuple

from django.contrib import admin
from houses.models import House
# Register your models here.

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    list_display: Tuple[str] = (
        "name",
        "price_per_night",
        "pets_allowed",
        "address",
    )

    list_filter: Tuple[str] = (
        "price_per_night",
        "pets_allowed",
    )
