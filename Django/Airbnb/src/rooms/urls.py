from django.urls import path

from rooms.views import Rooms, Amenities, AmenityDetail, RoomDetail, RoomReviews

# <{parameter}:{name parameter}>
# <int:room_id>/<str:room_name> ==> {int}/{str} ...


urlpatterns = [
    path("", Rooms.as_view()),
    path("<int:pk>", RoomDetail.as_view()),
    path("<int:pk>/reviews", RoomReviews.as_view()),
    path("amenities/", Amenities.as_view()),
    path("amenities/<int:pk>", AmenityDetail.as_view()),
]