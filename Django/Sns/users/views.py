from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from users.models import User
from users.serializers import UserDefaultSerializer, UserDetailSerializer, UserFollowSerializer
from follows.models import Follow
# Create your views here.
class UserList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size

        all_users = User.objects.all()
        serializer = UserDefaultSerializer(
            instance=all_users,
            many=True,
            context={"request":request}
        )
        return Response({
            "total": all_users.count(),
            "page": page,
            "result": serializer.data
        })

class UserDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User Not Found")

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserDetailSerializer(instance=user)
        return Response(serializer.data)

class MyUserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(
            instance=request.user,
            context={"request":request}
        )
        return Response(serializer.data)

class Follows(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User Not Found")

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserDefaultSerializer(instance=user)
        return Response(serializer.data)

    def post(self, request, pk):
        target_user = self.get_object(pk=pk) # 팔로잉 할 user
        if request.user == target_user: # 자기자신
            return Response(status=HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(
            follower=request.user, # 현재 유저
            following=target_user, # 상대를 Following
        ).exists(): # 현재 유저 (request.user)가 target_user를 Following 중인지
            raise ParseError(f"Already Follows {target_user}!")

        Follow.objects.create(
            follower=request.user,
            following=target_user,
        )
        updated_follows = UserDefaultSerializer(instance=target_user)
        return Response(updated_follows.data)

    def delete(self, request, pk):
        target_user = self.get_object(pk=pk)
        to_delete_object = Follow.objects.filter(
            follower=request.user,
            following=target_user,
        )
        if not to_delete_object.exists():
            raise ParseError(f"You didn't follow {target_user}")
        to_delete_object.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class Followers(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User Not Found")

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size
        user = self.get_object(pk=pk)
        users_all_followers = Follow.objects.filter(following=user)[start:end]  # 해당 User를 follow 하는 사람들
        followers = [u.follower for u in users_all_followers]
        serializer = UserFollowSerializer(
            followers,
            many=True,
        )
        return Response(serializer.data)

class Followings(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User Not Found")

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size
        user = self.get_object(pk=pk)
        all_followings = Follow.objects.filter(follower=user)[start:end]
        followings = [u.following for u in all_followings]
        serializer = UserFollowSerializer(
            instance=followings,
            many=True,
        )
        return Response(serializer.data)

class MyFollowers(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # followings = Follow.objects.filter(follower=request.user)
        followers_queryset = Follow.objects.filter(following=request.user)
        my_followers = [q.following for q in followers_queryset]
        serializer = UserFollowSerializer(
            instance=my_followers,
            many=True,
            context={"request":request}
        )
        return Response(serializer.data)

class MyFollowings(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        followings_queryset = Follow.objects.filter(follower=request.user)
        my_followings = [q.follower for q in followings_queryset]
        serializer = UserFollowSerializer(
            instance=my_followings,
            many=True,
            context={"request":request}
        )
        return Response(serializer.data)

