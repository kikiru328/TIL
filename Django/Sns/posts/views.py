from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from posts.serializers import PostDetailSerializer, PostListSerializer


# Create your views here.
class Posts(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly] # readonly: get

    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size

        users_all_posts = Post.objects.filter(author=request.user)
        pagination_posts = users_all_posts[start:end]
        serializer = PostListSerializer(
            instance=pagination_posts,
            many=True,
            context={"request": request},
        )
        return Response({
            "total": users_all_posts.count(),
            "page": page,
            "result": serializer.data
        })

    def post(self, request):
        serializer = PostDetailSerializer(data=request.data)
        if serializer.is_valid():
            new_post = serializer.save(author=request.user)
            serializer = PostDetailSerializer(new_post)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
