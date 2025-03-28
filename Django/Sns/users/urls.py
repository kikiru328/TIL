from django.urls import path
from users.views import UserList, UserDetail, Follows
urlpatterns = [
    path("", UserList.as_view()),
    path("<int:pk>", UserDetail.as_view()),
    path("<int:pk>/follows/", Follows.as_view())
]