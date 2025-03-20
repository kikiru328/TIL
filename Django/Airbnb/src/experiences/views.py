from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from experiences.models import Perk
from experiences.serializers import PerkSerializer


# Create your views here.
class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors
        perk = serializer.save()
        return Response(PerkSerializer(perk).data)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk=pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk=pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_perk = serializer.save()
        return Response(
            PerkSerializer(updated_perk).data
        )

    def delete(self, request, pk):
        perk = self.get_object(pk=pk)
        perk.delete()
        return Response(HTTP_204_NO_CONTENT)

