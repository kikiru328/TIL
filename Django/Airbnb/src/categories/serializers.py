from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # fields = "__all__" # fields="__all__" : get all models
        fields = (
            "name",
            "kind",
        )
