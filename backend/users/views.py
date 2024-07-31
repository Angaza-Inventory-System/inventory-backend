from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend.authen.permissions import IsNotBlacklisted, IsSuperUser
from backend.devices.pagination import CustomPagination
from backend.users.decorators import permission_required

from .models import User
from .helpers import getValidPermissions, updatePermissions
from .serializers import UserPermissionsSerializer, UserSerializer
from django.core.exceptions import ValidationError

@permission_classes([AllowAny])
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes([IsNotBlacklisted])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "username": ["exact", "icontains"],
        "email": ["exact", "icontains"],
        "first_name": ["icontains"],
        "last_name": ["icontains"],
        "role": ["exact"],
    }
    ordering_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["username"]

    @permission_required("readUsers")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required("createUsers")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @permission_required("editUsers")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_required("editUsers")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @permission_required("deleteUsers")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@permission_classes([IsNotBlacklisted])
class UpdateUserPermissionsView(viewsets.GenericViewSet, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserPermissionsSerializer
    lookup_field = "username"

    @permission_required("editUsers")
    @action(detail=True, methods=['patch'])
    def add_permissions(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            new_permissions = getValidPermissions(request.data, existing_permissions=instance.permissions)
            updatePermissions(instance, new_permissions, operation='add')
            return Response({"permissions": instance.permissions}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @permission_required("editUsers")
    @action(detail=True, methods=['put'])
    def replace_permissions(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            new_permissions = getValidPermissions(request.data)
            updatePermissions(instance, new_permissions, operation='replace')
            return Response({"permissions": instance.permissions}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @permission_required("editUsers")
    @action(detail=True, methods=['delete'])
    def remove_permissions(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            permissions_to_remove = getValidPermissions(request.data, existing_permissions=instance.permissions)
            updatePermissions(instance, permissions_to_remove, operation='remove')
            return Response({"permissions": instance.permissions}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @permission_required("editUsers")
    @action(detail=True, methods=['delete'])
    def delete_all_permissions(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            updatePermissions(instance, [], operation='clear')
            return Response({"permissions": instance.permissions}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)