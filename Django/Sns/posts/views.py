from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import PostSerializer


# Create your views here.
class Posts(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly] # readonly: get

    def get(self, request):
        return Response({"ok":True})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            new_post = serializer.save(user=request.user)
            print(new_post)
            serializer = PostSerializer(new_post)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
