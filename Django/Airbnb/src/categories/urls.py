from django.urls import path

from categories.views import Categories, CategoryDetail

urlpatterns = [
    path("", Categories.as_view()), # rule: Check and run api codes
    path("<int:pk>", CategoryDetail.as_view())
]