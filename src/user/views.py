from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from .serializer import UserSerializer


# Create your views here.
class UserListCreate(ListCreateAPIView):
    """
    API View that lists all users.

    get: Returns a list of  all users.

    """

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
