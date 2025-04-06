from django.urls import path
from posts.views import PostList, PostDetail, Likes, CommentList, CommentDetail, PresignedURL

urlpatterns = [
    path("", PostList.as_view()),
    path("<int:pk>", PostDetail.as_view()),
    path("<int:pk>/likes/", Likes.as_view()),
    path("<int:pk>/comments/", CommentList.as_view()),
    path("<int:post_pk>/comments/<int:comment_pk>", CommentDetail.as_view()),
    path("presigned-url/", PresignedURL.as_view())
]