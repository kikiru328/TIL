from django.urls import path
from .views import PerkDetail, Perks, Experiences, ExperienceDetail, ExperiencePerks, ExperienceBookings, \
    ExperienceBookingsDetail

urlpatterns = [
    path("", Experiences.as_view()),
    path("<int:pk>", ExperienceDetail.as_view()),
    path("<int:pk>/perks/", ExperiencePerks.as_view()),
    path("<int:pk>/bookings/", ExperienceBookings.as_view()),
    path("<int:ex_pk>/bookings/<int:bk_pk>",ExperienceBookingsDetail.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]