from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.authen.permissions import IsBlacklisted, IsSuperUser
from backend.inventory.pagination import CustomPagination

from .helpers.permissionsHelpers import getValidPermissions, updatePermissions
from .models import User
from .serializers import (
    UserPasswordSerializer,
    UserPermissionsSerializer,
    UserSerializer,
)

@permission_classes([AllowAny])
class UserCreate(generics.CreateAPIView):
    """
    Endpoint for creating a new User.

    **Permissions:**
    - `AllowAny`
    """
    serializer_class = UserSerializer

@permission_classes([IsBlacklisted])
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing User records.

    Provides endpoints for listing, creating, updating, and deleting users.
    
    **Permissions:**
    - `GET`, `POST`, `PUT`, `PATCH`, `DELETE`: 'manageUsers'

    **Filtering:**
    - Fields: username, email, first_name, last_name, role
    
    **Ordering:**
    - Fields: username, email, first_name, last_name
    """
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

@permission_classes([IsBlacklisted])
class UserPasswordUpdateView(generics.UpdateAPIView):
    """
    Endpoint for updating a user's password.

    **Permissions:**
    - `IsBlacklisted`
    """
    serializer_class = UserPasswordSerializer

    def get_object(self):
        jwt_auth = JWTAuthentication()
        request = self.request
        auth_result = jwt_auth.authenticate(request)
        if auth_result is None:
            return Response(
                {"Error: Missing authentication token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user, _ = auth_result
        return user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response(
            {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
        )

@permission_classes([IsBlacklisted, IsSuperUser])
class UserPermissionsViewSet(viewsets.GenericViewSet):
    """
    ViewSet for managing user permissions.

    **Permissions:**
    - `GET`: 'managePermissions'
    - `PATCH`, `PUT`: 'managePermissions'
    - `DELETE`: 'managePermissions'

    **Actions:**
    - `retrieve`: Get current permissions
    - `partial_update`: Add permissions
    - `update`: Replace permissions
    - `destroy`: Remove permissions
    - `delete_all_permissions`: Clear all permissions
    """
    queryset = User.objects.all()
    serializer_class = UserPermissionsSerializer
    lookup_field = "username"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(
            {"permissions": instance.permissions}, status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            new_permissions = getValidPermissions(request.data)
            updatePermissions(instance, new_permissions, operation="add")
            return Response(
                {"permissions": instance.permissions}, status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            new_permissions = getValidPermissions(request.data)
            updatePermissions(instance, new_permissions, operation="replace")
            return Response(
                {"permissions": instance.permissions}, status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            permissions_to_remove = getValidPermissions(request.data)
            updatePermissions(instance, permissions_to_remove, operation="remove")
            return Response(
                {"permissions": instance.permissions}, status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def delete_all_permissions(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            updatePermissions(instance, [], operation="clear")
            return Response(
                {"permissions": instance.permissions}, status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
