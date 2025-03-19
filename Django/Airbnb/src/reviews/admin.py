from django.contrib import admin

from reviews.models import Review

class WordFilter(admin.SimpleListFilter):
    title = "Filter by Words!"
    parameter_name = "word"
    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome")
        ]

    def queryset(self, request, reviews ):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        return reviews

# TODO: Bad and Good Review, Bad lt 3 good gt 3
class RatingFilter(admin.SimpleListFilter):
    title = "Filter by Ratings"
    parameter_name = "rating_score"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad")
        ]

    def queryset(self, request, reviews):
        rating_filters = {
            "good": reviews.filter(rating__gte=3),
            "bad": reviews.filter(rating__lt=3)
        }
        return rating_filters.get(self.value(), reviews)

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        RatingFilter,
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
    )