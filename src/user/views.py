from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from permission.models import Permission
from .serializer import UserSerializer


# Create your views here.
class UserListCreate(ListCreateAPIView):
    """
    API View that lists all users and Create a new User.
    get: Returns a list of  all users. Filter by passing a query string
    e.g: ?family_name=james
    post: Creates a new User
    """

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    filterset_fields = ("family_name",)


class UserRetrieveDelete(RetrieveDestroyAPIView):
    """
    API View that lists all users and Create a new User.
    get: Returns a user given their id.
    delete: Deletes a user given their id
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"


class UserGrantPermission(APIView):
    """
    API View that grants permission to a user
    """

    def post(self, request):
        """
        Grant New Permission to a user.
        In the URL, supply query parameters: user_id and permission_id
        """
        user_id = request.query_params.get("user_id")
        permission_id = request.query_params.get("permission_id")

        user = get_user_model().objects.filter(id=user_id).first()
        permission = Permission.objects.filter(id=permission_id).first()

        if not user or not permission:
            return Response(
                {"error": "User or permission not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.grant_permission(permission_id)
        user.save()
        serializer = UserSerializer(instance=user)

        return Response(
            {"message": "Permission granted successfully.", "user": serializer.data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        """
        Deletes a Permission from a user.
        In the URL, supply query parameters: user_id and permission_id
        """
        user_id = request.query_params.get("user_id")
        permission_id = request.query_params.get("permission_id")

        user = get_user_model().objects.filter(id=user_id).first()
        permission = Permission.objects.filter(id=permission_id).first()

        if not user or not permission:
            return Response(
                {"error": "User or permission not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.revoke_permission(permission_id)
        user.save()
        serializer = UserSerializer(instance=user)

        return Response(
            {"message": "Permission granted successfully.", "user": serializer.data},
            status=status.HTTP_200_OK,
        )
