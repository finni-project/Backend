from rest_framework import serializers

from .models import Allowance, AllowanceCategory


class AllowanceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AllowanceCategory
        fields = ["name", "icon"]


class AllowanceSerializer(serializers.ModelSerializer):
    allowance_categories = AllowanceCategorySerializer(many=True, required=True)

    class Meta:
        model = Allowance
        fields = ["user", "cycle", "amount", "allowance_categories"]

    def create(self, validated_data):
        allowance_categories = validated_data.pop('allowance_categories', [])
        allowance = Allowance.objects.create(**validated_data)

        for category in allowance_categories:
            AllowanceCategory.objects.create(allowance=allowance, **category)

        return allowance
