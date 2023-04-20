from django.urls import path

from .views import UserListCreate
from .views import UserGrantPermission

app_name = "user"

urlpatterns = [
    path("", UserListCreate.as_view(), name="user-list-create"),
    path("permission", UserGrantPermission.as_view(), name="user-permissions"),
]
