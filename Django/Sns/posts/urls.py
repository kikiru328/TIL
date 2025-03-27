from django.urls import path
from posts.views import Posts, PostDetail

urlpatterns = [
    path("", Posts.as_view()),
    path("<int:pk>", PostDetail.as_view())
    # path("<int:pk>/likes/",)
]