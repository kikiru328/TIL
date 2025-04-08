from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from follows.models import Follow
from posts.models import Post
from posts.serializers import PostListSerializer
from utils.redis import redis_client


# Create your views here.
class NewsFeeds(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.query_params.get("page", 1))
        page_size = 10
        start = (page - 1) * page_size
        end = start + page_size - 1

        user = request.user
        key = f"newsfeed:user:{user.id}"
        post_ids = redis_client.lrange(key, start, end)
        posts = Post.objects.filter(id__in=post_ids).select_related("author")
        posts_dict = {str(post.id): post for post in posts}
        ordered_posts = [posts_dict[pid] for pid in post_ids if pid in posts_dict]
        serializer = PostListSerializer(ordered_posts, many=True, context={"request": request})
        return Response({
            "page": page,
            "result": serializer.data
        })

    def post(self, request):
        user = request.user
        followings = Follow.objects.filter(follower=user).values_list("following_id", flat=True)
        posts = Post.objects.filter(author__in=followings).order_by("-created_at")[:50]
        post_ids = [str(post.id) for post in posts]

        key = f"newsfeed:user:{user.id}"
        redis_client.delete(key)
        if post_ids:
            redis_client.rpush(key, *post_ids)
            redis_client.ltrim(key, 0, 49)
        return Response(status=HTTP_200_OK)



