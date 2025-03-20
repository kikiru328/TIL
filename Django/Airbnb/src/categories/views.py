from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from categories.models import Category
from categories.serializers import CategorySerializer


# Create your views here.
@api_view(["GET", "POST"]) # Test
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(
            all_categories,
            many=True,
        )
        return Response(
            serializer.data
        )
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data) # Client's request
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_category = serializer.save()
        return Response(
            CategorySerializer(new_category).data,
        )



@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound
    if request.method == "GET":
        serializer = CategorySerializer(
                category,
        )
        return Response(
            serializer.data,
        )
    elif request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True, # 부분 갱신
        )

        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_category = serializer.save() # --> update
        return Response(CategorySerializer(updated_category).data)

    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)