"""
API views and serializers for managing users.

Views:
- UserListCreate: API endpoint to list all users or create a new user.
- UserRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete a user.

Serializers:
- UserSerializer: Serializes User model data for API interactions.
"""

from rest_framework import generics
from .models import User
from .serializers import UserSerializer

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
