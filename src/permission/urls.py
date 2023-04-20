from django.urls import path

from .views import PermissionListCreate

app_name = "permission"

urlpatterns = [path("", PermissionListCreate.as_view(), name="permission-list-create")]
