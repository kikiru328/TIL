from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from users.models import User
from users.permission import IsUserOrNothing
from users.serializers import UserDefaultSerializer, UserDetailSerializer

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

    permission_classes = [IsAuthenticated, IsUserOrNothing]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User Not Found")

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserDetailSerializer(instance=user)
        return Response(serializer.data)

