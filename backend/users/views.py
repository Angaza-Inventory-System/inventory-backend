"""
API views and serializers for managing users.

Views:
- UserListCreate: API endpoint to list all users or create a new user.
- UserRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete a user.

Serializers:
- UserSerializer: Serializes User model data for API interactions.
"""

from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

@permission_classes([AllowAny])
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@permission_classes([AllowAny])
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@permission_classes([IsAuthenticated])
class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

