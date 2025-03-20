from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from categories.models import Category
from categories.serializers import CategorySerializer

# Create your views here.

class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True,)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data) # Client's request
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_category = serializer.save()
        return Response(CategorySerializer(new_category).data,)

class CategoryDetail(APIView):
    def get_object(self, pk): # conventions: Django Restframework
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk),)
        return Response(serializer.data,)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True, # 부분 갱신
        )

        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_category = serializer.save() # --> update
        return Response(CategorySerializer(updated_category).data)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
