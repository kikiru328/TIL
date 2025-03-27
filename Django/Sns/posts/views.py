from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError

from posts.models import Post
from posts.serializers import PostDetailSerializer, PostListSerializer
from posts.permission import IsAuthorOrReadOnly

from likes.models import Like
from comments.models import Comment
from comments.serializers import CommentSerializer
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
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_post = serializer.save(author=request.user)
        serializer = PostDetailSerializer(new_post)
        return Response(serializer.data)

class PostDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound("There is no Post")

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

class Likes(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound("There is no Post")

    def get(self, request, pk):
        post = self.get_object(pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def post(self, request, pk):
        post = self.get_object(pk=pk)
        if Like.objects.filter(
            user=request.user,
            post=post
        ).exists():
            raise ParseError("Already Likes this post!")
        Like.objects.create(
            user=request.user,
            post=post,
        )
        updated_like_counts = post.likes.count()
        return Response({
            "message": "Success Likes",
            "likes_count": updated_like_counts},
            status=HTTP_201_CREATED)

    def delete(self, request, pk):
        post = self.get_object(pk=pk)
        like_to_delete = Like.objects.filter(
            user=request.user,
            post=post
        )
        if not like_to_delete.exists():
            raise NotFound("There is no Likes on this post!")
        like_to_delete.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class Comments(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size
        post = self.get_object(pk=pk)
        comments = post.comments.all().order_by("-created_at")[start:end]
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        post = self.get_object(pk=pk)
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_comment = serializer.save(
            user=request.user,
            post=post,
        )
        serializer = CommentSerializer(new_comment)
        return Response(serializer.data)