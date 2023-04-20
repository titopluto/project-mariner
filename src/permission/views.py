from rest_framework.generics import ListCreateAPIView

from .models import Permission
from .serializer import PermissionSerializer


# Create your views here.
class PermissionListCreate(ListCreateAPIView):
    """
    API View that lists all Permissions and Create a new Permission.
    get: Returns a list of  all permissions.
    post: Create a new Permission
    """

    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
