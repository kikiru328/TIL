from django.urls import path

from users.views import Me, Users

urlpatterns= [
    path("", Users.as_view()),
    path("me/", Me.as_view()),
]