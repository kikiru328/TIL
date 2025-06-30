from django.urls import path
from users.views import UserList, UserDetail, Follows, Followers, Followings, MyFollowers, MyFollowings, MyUserInfo, \
    SignUp

urlpatterns = [
    path("", UserList.as_view()),
    path("me/", MyUserInfo.as_view()),
    path("<int:pk>", UserDetail.as_view()),
    path("<int:pk>/follows/", Follows.as_view()),
    path("<int:pk>/follows/followers", Followers.as_view()),
    path("<int:pk>/follows/followings", Followings.as_view()),
    path("me/follows/followers", MyFollowers.as_view()),
    path("me/follows/followings", MyFollowings.as_view()),
    path("sign-up", SignUp.as_view()),
]