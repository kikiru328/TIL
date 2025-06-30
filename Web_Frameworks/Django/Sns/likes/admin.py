from django.contrib import admin
from likes.models import Like
# Register your models here.
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "post",
    )