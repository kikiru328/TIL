from django.http import HttpResponse
from django.shortcuts import render

from rooms.models import Room


# Create your views here.
def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {
            "title": "Hello! This title comes from Django!",
            "rooms": rooms
        }, # render with html
    ) # request, template

def see_one_room(request, room_id): # {url parameter}
    return HttpResponse(f"see room with id: {room_id}")

