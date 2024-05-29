from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=False)
    birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["email", "name", "birth"]
        extra_kwargs = {"password": {"write_only": True}}

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)

        if request and request.method == "PATCH":
            self.fields["email"].required = False

    def validate(self, attrs):
        email = attrs.get("email", None)
        name = attrs.get("name", None)

        if email and not name:
            attrs["name"] = email.split("@")[0]

        return attrs

    def update(self, instance, validated_data):
        validated_data.pop("email", None)

        return super().update(instance, validated_data)
