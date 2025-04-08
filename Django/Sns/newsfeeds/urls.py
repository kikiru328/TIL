from newsfeeds.views import NewsFeeds
from django.urls import path
urlpatterns = [
    path("",NewsFeeds.as_view()),
    ]
