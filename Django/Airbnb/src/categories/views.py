from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from categories.models import Category
from categories.serializers import CategorySerializer

# Create your views here.

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer # require parameter
    queryset = Category.objects.all() # require
