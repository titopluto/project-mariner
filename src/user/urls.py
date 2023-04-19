from django.urls import path

from .views import UserListCreate

app_name = "user"

urlpatterns = [path("", UserListCreate.as_view(), name="user-list-create")]
