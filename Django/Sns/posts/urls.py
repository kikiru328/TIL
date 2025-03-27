from django.urls import path
from posts.views import Posts, PostDetail, Likes, Comments, CommentDetail

urlpatterns = [
    path("", Posts.as_view()),
    path("<int:pk>", PostDetail.as_view()),
    path("<int:pk>/likes/", Likes.as_view()),
    path("<int:pk>/comments/", Comments.as_view()),
    path("<int:post_pk>/comments/<int:comment_pk>", CommentDetail.as_view()),
]