from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer class for the User Model"""

    password = serializers.CharField(write_only=True, min_length=5)
    permissions = serializers.SerializerMethodField()

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
            "permissions",
        )
        read_only_fields = ("id",)

    def get_permissions(self, obj):
        # Retrieve the related permissions objects
        permissions = obj.permissions.all()

        # Extract the desired fields from each permission object
        permission_data = []
        for permission in permissions:
            permission_data.append(
                {
                    "permission_id": permission.id,
                    "type": permission.name,
                    "name": permission.description,
                }
            )

        return permission_data

    def create(self, validated_data):
        """Create a new user"""
        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
