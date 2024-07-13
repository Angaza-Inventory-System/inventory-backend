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
from rest_framework.decorators import permission_classes
from .models import User
from .serializers import UserSerializer
from backend.authen.permissions import IsNotBlacklisted
from rest_framework.permissions import AllowAny

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
