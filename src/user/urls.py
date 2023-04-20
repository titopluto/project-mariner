from django.urls import path

from .views import UserListCreate, UserRetrieveDelete, UserGrantPermission

app_name = "user"

urlpatterns = [
    path("", UserListCreate.as_view(), name="user-list-create"),
    path("<uuid:id>", UserRetrieveDelete.as_view(), name="user-retrieve-delete"),
    path("permission", UserGrantPermission.as_view(), name="user-permissions"),
]
