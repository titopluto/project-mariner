from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer class designed to create a new user model"""

    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "password",
            "given_name",
            "family_name",
            "birthdate",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):

        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
