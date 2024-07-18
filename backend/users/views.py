"""
API views and serializers for managing users.

Views:
- UserCreate: API endpoint to create a new user.
- UserList: API endpoint to list all users.
- UserRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete a user.

Serializers:
- UserSerializer: Serializes User model data for API interactions.
"""

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from backend.authen.permissions import IsNotBlacklisted, IsSuperUser
from .models import User
from rest_framework.response import Response
from .serializers import UserSerializer, UserPermissionsSerializer
from rest_framework import status


@permission_classes([AllowAny])
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes([IsNotBlacklisted])
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes([IsNotBlacklisted])
class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@permission_classes([IsNotBlacklisted, IsSuperUser])
class UpdateUserPermissionsView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPermissionsSerializer
    lookup_field = 'username'


@permission_classes([IsNotBlacklisted, IsSuperUser])
class UserPermissionsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPermissionsSerializer
    lookup_field = 'username'