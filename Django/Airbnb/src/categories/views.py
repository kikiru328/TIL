from rest_framework.decorators import api_view
from rest_framework.response import Response
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
        print(f"User Data Validator: {serializer.is_valid()}") # check
        print(f"Error: {serializer.errors}")
        if not serializer.is_valid():
            return Response(serializer.errors)
        return Response({"created_at" : True})



@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(
        category,
    )
    return Response(
            serializer.data,
    )