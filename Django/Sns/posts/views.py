from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from posts.models import Post
from posts.serializers import PostDetailSerializer, PostListSerializer
from posts.permission import IsAuthorOrReadOnly

# Create your views here.
class Posts(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly] # readonly: get

    def get(self, request):
        """전체 게시물 목록 조회"""
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size

        users_all_posts = (Post.objects
                           .filter(author=request.user)
                           .order_by("-created_at")) #최신 순 적용
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
        """게시물 작성"""
        serializer = PostDetailSerializer(data=request.data)
        if serializer.is_valid():
            new_post = serializer.save(author=request.user)
            serializer = PostDetailSerializer(new_post)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class PostDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        """단일 게시물 조회"""
        post = self.get_object(pk=pk)
        serializer = PostDetailSerializer(
            instance=post,
            context={"request": request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk=pk)
        serializer = PostDetailSerializer(
            instance=post,
            data=request.data
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_whole_post = serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        post = self.get_object(pk=pk)
        serializer = PostDetailSerializer(
            instance=post,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_whole_post = serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        post = self.get_object(pk=pk)
        post.delete() #set permission, post.author==request.user
        return Response(status=HTTP_204_NO_CONTENT)