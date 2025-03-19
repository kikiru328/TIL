from django.urls import path
from rooms import views

# <{parameter}:{name parameter}>
# <int:room_id>/<str:room_name> ==> {int}/{str} ...


urlpatterns = [
    path("", views.see_all_rooms), # from rooms/
    path("<int:room_pk>", views.see_one_room),
]