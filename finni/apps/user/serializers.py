from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=False)
    birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["email", "name", "birth"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs.get('email')
        name = attrs.get('name')

        if not name:
            attrs["name"] = email.split("@")[0]

        return attrs
