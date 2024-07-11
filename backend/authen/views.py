"""
API views for managing authentication tokens.

Views:
- AuthListCreate: API endpoint to list all authentication tokens or create a new token.
- AuthRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete an authentication token.

Serializers:
- AuthSerializer: Serializes JWTToken model data for API interactions.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import JWTToken
from .serializers import AuthSerializer
from backend.users.serializers import UserLoginSerializer


@permission_classes([IsAuthenticated])
class AuthListCreate(generics.ListCreateAPIView):
    queryset = JWTToken.objects.all()
    serializer_class = AuthSerializer

@permission_classes([IsAuthenticated])
class AuthRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = JWTToken.objects.all()
    serializer_class = AuthSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    response_data = serializer.validated_data
    return Response(response_data, status=status.HTTP_200_OK)


