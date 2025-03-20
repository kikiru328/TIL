from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.Serializer):
    # how to "represent" to json
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Category.objects.create(
            **validated_data # get dictionary, whole validated data (a:b -> 'a'= 'b')
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name) # pack-unpack # 업다면 현재 정보
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance
