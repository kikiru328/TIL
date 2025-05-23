import uuid

import boto3
from django.conf import settings
from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError

from follows.models import Follow
from posts.models import Post
from posts.serializers import PostDetailSerializer, PostListSerializer
from posts.permission import IsAuthorOrReadOnly, IsCommentAuthorOrReadOnly

from likes.models import Like
from comments.models import Comment
from comments.serializers import CommentSerializer
from utils.redis import redis_client


# Create your views here.
class PostList(APIView):

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
        def distribute_to_followers(post):
            followers = Follow.objects.filter(following=post.author).values_list("follower_id", flat=True)
            for follower_id in followers:
                key = f"newsfeed:user:{follower_id}"
                redis_client.lpush(key, str(post.id))
                redis_client.ltrim(key, 0, 99)

        serializer = PostDetailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_post = serializer.save(author=request.user)

        distribute_to_followers(new_post)

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

class CommentList(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound("There is no Post")

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

class CommentDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]

    def get_object(self, post_pk, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk)
            if comment.post.pk != post_pk:
                raise NotFound("This comment is not include on this post")
            return comment
        except Comment.DoesNotExist:
            raise NotFound("There is No Comment")

    def get(self, request, post_pk, comment_pk):
        comment = self.get_object(post_pk=post_pk,
                                  comment_pk=comment_pk,
                                  )
        serializer = CommentSerializer(instance=comment)
        return Response(serializer.data)

    def patch(self, request, post_pk, comment_pk):
        comment = self.get_object(post_pk=post_pk,
                                  comment_pk=comment_pk,
                                  )
        serializer = CommentSerializer(
            instance=comment,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_comment = serializer.save()
        serializer = CommentSerializer(updated_comment)
        return Response(serializer.data)

    def delete(self, request, post_pk, comment_pk):
        comment = self.get_object(post_pk=post_pk,
                                  comment_pk=comment_pk,
                                  )
        comment.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class PresignedURL(APIView):
    def get(self, request):
        filename = request.query_params.get("filename")
        content_type = request.query_params.get("type")

        if not filename or not content_type:
            raise ParseError("Required filename & content type")

        extension = filename.split('.')[-1]
        key = f"posts/{uuid.uuid4()}.{extension}"


        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        upload_url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": key,
                "ContentType": content_type
            },
            ExpiresIn=300
        )

        s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{key}"

        return Response({
            "upload_url": upload_url,
            "s3_url": s3_url
        })

from django.shortcuts import render

def post_preview(request):
    return render(request, "post_preview.html")
