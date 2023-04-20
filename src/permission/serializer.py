from rest_framework import serializers

from permission.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer class for the Permission Model"""

    class Meta:
        model = Permission
        fields = "__all__"
