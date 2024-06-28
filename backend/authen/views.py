"""
API views for managing authentication tokens.

Views:
- AuthListCreate: API endpoint to list all authentication tokens or create a new token.
- AuthRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete an authentication token.

Serializers:
- AuthSerializer: Serializes JWTToken model data for API interactions.
"""

from rest_framework import generics
from .models import JWTToken
from .serializers import AuthSerializer

class AuthListCreate(generics.ListCreateAPIView):
    queryset = JWTToken.objects.all()
    serializer_class = AuthSerializer

class AuthRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = JWTToken.objects.all()
    serializer_class = AuthSerializer

