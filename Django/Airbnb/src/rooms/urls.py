from django.urls import path

from rooms.views import Amenities, AmenityDetail

# <{parameter}:{name parameter}>
# <int:room_id>/<str:room_name> ==> {int}/{str} ...


urlpatterns = [
    path("amenities/", Amenities.as_view()),
    path("amenities/<int:pk>", AmenityDetail.as_view()),
]