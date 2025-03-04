from django.contrib import admin
from .models import House
# Register your models here.

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display: List[str] = [
        "name",
        "price_per_night",
        "pets_allowed"
        "address",
    ]
